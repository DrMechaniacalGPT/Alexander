"""Bounded frozen-turn comparisons. Source-derived inputs/outputs must stay private."""
import argparse
import copy
import hashlib
import json
import time
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dojo.audit import violations
from dojo.core import dialogue_messages
from dojo.models import Ollama
from dojo.runner import dump


def render(messages, variant):
    if variant == 'original': return copy.deepcopy(messages)
    if variant == 'integrated': return dialogue_messages(messages)
    if variant not in ('readable', 'chat'): raise ValueError('Unknown rendering')
    view=json.loads(messages[-1]['content']);context=copy.deepcopy(view)
    events=context.pop('observations');instruction=context.pop('instruction');context.pop('cast',None)
    header=f"You are a person playing {view['self_name']} at a murder mystery party. Continue your own next turn; earlier lines are already spoken.\n"
    header+='CHARACTER AND CURRENT GAME CONTEXT\n'+json.dumps(context,ensure_ascii=False,indent=2)+'\nPUBLIC CAST\n'+json.dumps(view['cast'],ensure_ascii=False)
    def line(e):
        return f"[{e['id']}; scene {e['scene']}; heard by {', '.join(e['recipients'])}] {e.get('actor_name',e['actor'])}: {e['content']}"
    result=[copy.deepcopy(messages[0]),{'role':'user','content':header}]
    if variant=='readable':
        result[-1]['content']+='\nCHRONOLOGICAL OBSERVATIONS\n'+'\n'.join(line(e) for e in events)+f"\nNEXT TURN: {view['self_name']} speaks to {', '.join(view['audience_names'].values())}. {instruction}"
    else:
        for e in events:
            result.append({'role':'assistant' if e['actor']==view['self'] else 'user','content':line(e)})
        result.append({'role':'user','content':f"Continue as {view['self_name']} with your next reply in the current encounter. {instruction}"})
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source_run',type=Path);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--cases',nargs='+',required=True)
    p.add_argument('--variants',nargs='+',choices=['original','readable','chat','integrated'],default=['original','integrated'])
    p.add_argument('--model',help='Optional installed local model override')
    p.add_argument('--seeds',nargs='+',type=int,default=[17,23]);p.add_argument('--max-calls',type=int,default=18)
    p.add_argument('--max-seconds',type=float,default=600)
    a=p.parse_args()
    if a.out.exists(): raise ValueError('Use a new output directory; no silent retries')
    total=len(a.cases)*len(a.variants)*len(a.seeds)
    if total>a.max_calls or a.max_seconds<=0: raise ValueError('Comparison exceeds declared budget')
    if any(not c.startswith('t') or not c[1:].isdigit() for c in a.cases): raise ValueError('Expected turn IDs')
    a.out.mkdir(parents=True,mode=0o700)
    dump(a.out/'plan.json',{'cases':a.cases,'variants':a.variants,'seeds':a.seeds,'model':a.model,'max_calls':a.max_calls,'max_seconds':a.max_seconds,
                          'limitation':'Rendering treatments also add explicit party/continuation framing. Pilot chat is experimental; production uses integrated role-aware rendering.'})
    start=time.monotonic()
    for case in a.cases:
        source=a.source_run/'turns'/f'{case}.json';canonical=json.loads(source.read_text())['request']
        for seed in a.seeds:
            for variant in a.variants:
                remaining=a.max_seconds-(time.monotonic()-start)
                if remaining<=0: raise RuntimeError('Time budget exhausted')
                payload=copy.deepcopy(canonical);payload['options']['seed']=seed
                if a.model: payload['model']=a.model
                payload['messages']=render(canonical['messages'],variant)
                upper=sum(len(m['content'].encode()) for m in payload['messages'])+len(json.dumps(payload['format']).encode())+512+payload['options']['num_predict']
                if upper>payload['options']['num_ctx']: raise ValueError('Conservative context limit exceeded')
                record={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'variant':variant,'seed':seed,'request':payload}
                path=a.out/f'{case}-{seed}-{variant}.json';dump(path,record);path.chmod(0o600)
                try:
                    record['result']=Ollama().complete(payload,timeout=min(120,remaining))
                    # The original phase and schema are unchanged. Pilot text-only final
                    # instructions are not the JSON envelope expected by the old auditor.
                    record['contract_violations']=violations(canonical,record['result'])
                except Exception as exc: record['error']=str(exc)
                dump(path,record);path.chmod(0o600)
                print(path.name, 'error' if record.get('error') else 'recorded',flush=True)

if __name__=='__main__':main()
