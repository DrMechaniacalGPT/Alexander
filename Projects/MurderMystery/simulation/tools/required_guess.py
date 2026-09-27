"""Bounded required-choice probes on saved player contexts; no new evidence."""
import copy, hashlib, json, time
from pathlib import Path
from dojo.models import Ollama
from dojo.audit import violations
from dojo.runner import dump

def require_guess(original, candidates):
    p=copy.deepcopy(original)
    v=json.loads(p['messages'][-1]['content'])
    if not v.get('final_assessment'): raise ValueError('Expected final assessment')
    v['instruction']='The party ends with everyone making a guess. Choose exactly one most likely suspect from the candidate list using only your own card and what you actually heard. Even if several remain possible, make your best guess. Do not abstain. Briefly explain your choice without inventing evidence or claiming certainty. Candidate names: '+', '.join(candidates)+'. Return the chosen name in suspect and make conclusion consistent with that choice.'
    v['next_turn']='Make your private required guess now.'
    p['messages'][-1]['content']=json.dumps(v,ensure_ascii=False)
    p['format']['properties']['suspect']={'type':'string','enum':list(candidates)}
    p['format']['required'].append('suspect')
    return p

def main():
    out=Path('local-private/movie/required-guess');out.mkdir(mode=0o700)
    case=json.loads(Path('local-private/movie/adapted.json').read_text())
    names=[p['name'] for p in case['players'].values()]
    sources=['iteration-open-gemma','iteration-clarify-gemma-large']
    dump(out/'plan.json',{'method':'Same saved evidence, model, seed, thinking, budgets; replace final instruction and require enumerated suspect field. No abstention; culprit excluded.','sources':sources,'max_calls':14,'max_seconds':1800,'per_call_seconds':180,'candidates':names})
    start=time.monotonic();summary=[]
    for run in sources:
      for source in sorted((Path('local-private/movie')/run/'turns').glob('*.json')):
        d=json.loads(source.read_text());p=d.get('request',{});v=json.loads(p['messages'][-1]['content'])
        if not v.get('final_assessment') or v['self']=='p1':continue
        request=require_guess(p,names);path=out/f'{run}-{v["self"]}.json'
        record={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'request':request};dump(path,record)
        remaining=1800-(time.monotonic()-start)
        if remaining<=0:raise RuntimeError('Batch time budget exhausted')
        try:
          record['result']=Ollama().complete(request,timeout=min(180,remaining));record['violations']=violations(request,record['result'])
        except Exception as e:record['error']=str(e)
        dump(path,record);path.chmod(0o600)
        raw=record.get('result',{}).get('response',{});content=raw.get('message',{}).get('content','')
        try:action=json.loads(content)
        except Exception:action={}
        row={'run':run,'player':v['self'],'suspect':action.get('suspect'),'conclusion':action.get('conclusion'),'violations':record.get('violations'), 'error':record.get('error'),'seconds':record.get('result',{}).get('wall_seconds')}
        summary.append(row);dump(out/'summary.json',summary);print(json.dumps(row),flush=True)
if __name__=='__main__':main()
