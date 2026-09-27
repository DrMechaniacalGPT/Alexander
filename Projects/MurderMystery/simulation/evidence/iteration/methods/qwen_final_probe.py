import json,copy,time,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from dojo.models import Ollama
from dojo.audit import violations
from dojo.runner import dump
out=Path('local-private/movie/iteration-qwen-final');out.mkdir(mode=0o700)
sources={'wrong-choice':'local-private/movie/iteration-clarify-gemma-large/turns/t00149.json','ownership':'local-private/movie/iteration-clarify-gemma-large/turns/t00150.json'}
models=['qwen3.5:9b'];start=time.monotonic()
dump(out/'plan.json',{'models':models,'sources':sources,'seed':17,'thinking':True,'context':49152,'tokens':8192,'max_calls':2,'max_seconds':1200,'per_call_seconds':600,'method':'Exact saved messages and output schema; change model and native thinking/output-context budget. Inspect final structured response only; preserve internal reasoning privately.'})
for model in models:
 for name,source in sources.items():
  p=Path(source);original=json.loads(p.read_text())['request'];payload=copy.deepcopy(original);payload['model']=model;payload['think']=True;payload['options'].update(num_ctx=49152,num_predict=8192,seed=17)
  path=out/f'{model.split(":")[0]}-{name}.json';d={'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'request':payload};dump(path,d)
  remaining=1200-(time.monotonic()-start)
  if remaining<=0:raise RuntimeError('time budget exhausted')
  try:d['result']=Ollama().complete(payload,timeout=min(600,remaining));d['contract_violations']=violations(payload,d['result'])
  except Exception as e:d['error']=str(e)
  dump(path,d);path.chmod(0o600)
  raw=d.get('result',{}).get('response',{});print(path.name,json.dumps({'content':raw.get('message',{}).get('content',''),'tokens':raw.get('eval_count'),'seconds':d.get('result',{}).get('wall_seconds'),'errors':d.get('contract_violations',d.get('error'))}),flush=True)
