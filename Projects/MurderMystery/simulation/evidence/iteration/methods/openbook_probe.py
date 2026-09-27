import json,copy,time,sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from dojo.models import Ollama
from dojo.audit import violations
from dojo.runner import dump
root=Path('local-private/movie');out=root/'iteration-openbook';out.mkdir(mode=0o700)
case=json.loads((root/'iteration-clarify-party.json').read_text());inventory=json.loads((root/'movie-trait-baseline.json').read_text())
# Public Personality Traits only: no other character's brief, motive or culprit assignment.
board={case['players'][pid]['name']:[a['fact'] for a in row['inventory']] for pid,row in inventory['players'].items()}
clues=list(dict.fromkeys(c['text'] for cards in case['provenance']['hunt_assignment'].values() for c in cards))
source=root/'iteration-clarify-gemma-large/turns/t00149.json';old=json.loads(source.read_text())['request'];v=json.loads(old['messages'][1]['content']);v.update(json.loads(old['messages'][-1]['content']));v['observations']=[]
v['public_reference']={'status':'Open-book diagnostic: these printed public character attributes are authoritative scenario facts. No other private brief or culprit assignment is included. The clue list contains only card types actually collected by this party.','character_attributes':board,'collected_clue_cards':clues}
v['instruction']='Using the authoritative public reference, identify the best-supported murderer by comparing all candidates with the collected clue constraints. Name a single candidate if supported, otherwise explain what remains unresolved. Explain the relevant matches or exclusions briefly. Unknown is not a contradiction; one confirmed contradiction excludes a candidate.'
messages=[old['messages'][0],{'role':'user','content':json.dumps(v,ensure_ascii=False)}]
plan={'models':['gemma4:e4b-it-qat','qwen3.5:9b'],'seed':23,'thinking':False,'context':32768,'tokens':768,'max_calls':2,'max_seconds':300,'per_call_seconds':150,'method':'Best-case diagnostic with all shareable personality attributes and the union of actually collected clues supplied as an explicit public printed reference. Private roles and evaluator answer excluded. Dialogue history removed; this is not a conversation-success result.','sources_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,root/'movie-trait-baseline.json',root/'iteration-clarify-party.json']}};dump(out/'plan.json',plan);start=time.monotonic()
for model in plan['models']:
 backend=Ollama(model,context=32768,tokens=768,seed=23,thinking=False,strict_output=True);payload=backend.payload(messages);record={'request':payload};dest=out/(model.split(':')[0]+'.json');dump(dest,record)
 remaining=300-(time.monotonic()-start)
 if remaining<=0:raise RuntimeError('time budget exhausted')
 try:record['result']=backend.complete(payload,timeout=min(150,remaining));record['contract_violations']=violations(payload,record['result'])
 except Exception as e:record['error']=str(e)
 dump(dest,record);dest.chmod(0o600)
 print(dest.name,json.dumps({'content':record.get('result',{}).get('response',{}).get('message',{}).get('content'),'error':record.get('error'),'contract':record.get('contract_violations'),'seconds':record.get('result',{}).get('wall_seconds')}),flush=True)
