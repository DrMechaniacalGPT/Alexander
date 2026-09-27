"""Frozen single-turn probes. Rubrics are for human review, never model input."""
import argparse
import hashlib
import fcntl
import json
from pathlib import Path
from .core import State, messages_for
from .models import Ollama
from .runner import dump

def request(row, profile, backend):
    case = {'id':'probe','public':'A fictional social mystery.', 'truth':{},
            'players':{'p1':{'name':'Cal','brief':row['brief']},
                       'p2':{'name':'Bea','brief':'PRIVATE OTHER ROLE'},
                       'p3':{'name':'Ari','brief':'PRIVATE OTHER ROLE'}}, 'scenes':[]}
    for pid,name in row.get('names', {}).items():
        case['players'][pid]['name'] = name
    state = State(case)
    for i,(actor,text) in enumerate(row['events']):
        state.emit(str(i),actor,['p1'],'%s'%text,'s1')
    return backend.payload(messages_for(state,'p1',['p1'],'assessment',row['question'],True,prompt_profile=profile))

def collect(rows, out, backend, profiles=('legacy', 'grounded-v1')):
    """No retries: preserve failures and unfinished reservations for inspection."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    specification = {'cases': rows, 'profiles': list(profiles)}
    ids = [row['id'] for row in rows]
    if len(ids) != len(set(ids)) or any(not key.replace('-', '').replace('_', '').isalnum() for key in ids):
        raise ValueError('Case IDs must be unique safe filenames')
    with (out/'.run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest = out/'evaluation.json'
        if manifest.exists() and json.loads(manifest.read_text()) != specification:
            raise ValueError('Evaluation specification changed; use a new output directory')
        if not manifest.exists() and list(out.glob('*.json')):
            raise ValueError('Historical output lacks evaluator manifest; preserve it and use a new directory')
        dump(manifest, specification)
        for row in rows:
            for profile in profiles:
                payload=request(row,profile,backend)
                path=out/(row['id']+'-'+profile+'.json')
                digest=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
                if path.exists():
                    prior=json.loads(path.read_text())
                    if prior['request_sha256']!=digest:
                        raise ValueError('Existing request differs; use a new output directory')
                    if 'result' not in prior:
                        raise RuntimeError('Unfinished or failed request retained at '+str(path)+'; inspect it and use a new output directory')
                    continue
                record={'case':row['id'],'profile':profile,'request_sha256':digest,'request':payload}
                # Reserve before generation: an interrupted request is not silently repeated.
                dump(path, record)
                try:
                    record['result']=backend.complete(payload)
                except Exception as e:
                    record['error']=str(e)
                    dump(path, record)
                    raise
                dump(path, record)
                print(row['id'],profile,'recorded',flush=True)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('cases',type=Path); p.add_argument('--out',type=Path,required=True)
    p.add_argument('--model',required=True); p.add_argument('--seed',type=int,default=1)
    p.add_argument('--profiles',nargs='+',choices=['legacy','grounded-v1','grounded-v2'],default=['legacy','grounded-v1'])
    a=p.parse_args()
    backend=Ollama(a.model,context=8192,tokens=768,seed=a.seed)
    collect(json.loads(a.cases.read_text()), a.out, backend, a.profiles)
if __name__=='__main__': main()
