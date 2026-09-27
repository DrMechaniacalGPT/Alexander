import copy,json,time,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from dojo.models import Ollama
from dojo.audit import violations
from dojo.runner import dump
out=Path('local-private/movie/iteration-exclusion');out.mkdir(mode=0o700)
plan={'sources':['t00148','t00149'],'seeds':[17,23],'model':'gemma4:e4b-it-qat','context':49152,'tokens':8192,'thinking':True,'max_calls':4,'max_seconds':900,'per_call_seconds':300,'method':'Same received context and output schema; append a generic all-clue exclusion procedure to the final question. No specific attribute, candidate or hidden fact is supplied.'};dump(out/'plan.json',plan);start=time.monotonic()
for turn in plan['sources']:
 p=Path('local-private/movie/iteration-clarify-gemma-large/turns')/(turn+'.json');d=json.loads(p.read_text())
 for seed in plan['seeds']:
  r=copy.deepcopy(d['request']);v=json.loads(r['messages'][-1]['content']);v['instruction']+=' Before choosing, check EVERY candidate against ALL received clue constraints, including clue cards reported by other guests. One confirmed contradiction excludes a candidate even if several other traits match. A clue saying someone MAY have done something is weak support, not a required fact. An unknown attribute does not itself exclude anyone. Do not restrict your comparison to the three cards you personally found. If exactly one candidate remains unexcluded and has positive matches, name that best-supported candidate while acknowledging any unknowns. Otherwise state which candidates remain and why. Keep the final answer consistent with this comparison.';r['messages'][-1]['content']=json.dumps(v);r['options']['seed']=seed
  record={'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'request':r};dest=out/f'{turn}-{seed}.json';dump(dest,record)
  remaining=900-(time.monotonic()-start)
  if remaining<=0:raise RuntimeError('time budget exhausted')
  try:record['result']=Ollama().complete(r,timeout=min(300,remaining));record['contract_violations']=violations(r,record['result'])
  except Exception as e:record['error']=str(e)
  dump(dest,record);dest.chmod(0o600)
  print(dest.name,json.dumps({'content':record.get('result',{}).get('response',{}).get('message',{}).get('content'),'error':record.get('error'),'contract':record.get('contract_violations')}),flush=True)
