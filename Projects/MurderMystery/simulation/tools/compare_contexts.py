"""Four local diagnostic calls on a frozen synthetic assessment and no-report control.

No conversation regeneration, prompt optimization, or claim of model ranking.
Run from the simulation directory with PYTHONPATH=. python3 tools/compare_contexts.py.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from dojo.models import Ollama
from dojo.runner import dump


def compare(record, out):
    out=Path(out)
    if out.exists(): raise ValueError('Use a new output file; diagnostic records are not overwritten')
    base=json.loads(Path(record).read_text())['request']
    view=json.loads(base['messages'][-1]['content'])
    if not view['final_assessment']: raise ValueError('Requires a final assessment record')
    variants={'delivered':copy.deepcopy(base['messages']), 'no_report':copy.deepcopy(base['messages'])}
    control=copy.deepcopy(view)
    # Keep only the observer's own utterances: remove other-player reports.
    control['observations']=[e for e in control['observations'] if e['actor']==view['self']]
    variants['no_report'][-1]['content']=json.dumps(control,ensure_ascii=False)
    results=[]
    for model in ['qwen3.5:9b','gemma4:e4b-it-qat']:
        backend=Ollama(model,context=8192,tokens=384,seed=1)
        for label,messages in variants.items():
            payload=backend.payload(messages)
            entry={'model':model,'condition':label,'request':payload,
                   'source_record_sha256':hashlib.sha256(Path(record).read_bytes()).hexdigest()}
            results.append(entry);dump(out,results)
            try:
                entry['result']=backend.complete(payload,timeout=120)
                raw=entry['result']['response']
                action=json.loads(raw['message']['content'])
                allowed={e['id'] for e in json.loads(messages[-1]['content'])['observations']}
                entry['protocol_ok']=(raw.get('done_reason')!='length' and bool(action['conclusion'].strip())
                                      and set(action['evidence'])<=allowed)
            except Exception as exc:
                entry['error']=str(exc);entry['protocol_ok']=False
            dump(out,results)
            print(json.dumps({'model':model,'condition':label,'protocol_ok':entry['protocol_ok']}),flush=True)
    return results

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('record');p.add_argument('out');a=p.parse_args()
    compare(a.record,a.out)
