import copy,json,time,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from dojo.models import Ollama
from dojo.audit import violations
from dojo.runner import dump
out=Path('local-private/movie/iteration-notebook');out.mkdir(mode=0o700)
plan={'sources':['t00149','t00150'],'seed':17,'model':'gemma4:e4b-it-qat','context':49152,'tokens':8192,'thinking':True,'max_calls':2,'max_seconds':600,'per_call_seconds':300,'method':'Replace alternating historical chat messages for assessment with one attributed notebook. Preserve exact player card, all rendered visible event text/IDs in chronological order, current question and schema. No extracted facts or evaluator information.'};dump(out/'plan.json',plan);start=time.monotonic()
for turn in plan['sources']:
 p=Path('local-private/movie/iteration-clarify-gemma-large/turns')/(turn+'.json');d=json.loads(p.read_text());r=copy.deepcopy(d['request']);old=r['messages'];v=json.loads(old[-1]['content']);context=json.loads(old[1]['content']);history=old[2:-1]
 assert len(history)==len(v['observations'])
 v['personal_context']=context
 v['observations']=[{'id':e['id'],'recorded_event':m['content']} for e,m in zip(v['observations'],history)]
 system=old[0]['content']+' This is a private assessment of a recorded notebook, not a continuation of the public conversation. The notebook preserves the chronological events you actually received. Attribute statements to the named speaker. Your own past public claims can be mistaken; your supplied character card remains authoritative about your own fixed facts.'
 r['messages']=[{'role':'system','content':system},{'role':'user','content':json.dumps(v,ensure_ascii=False)}]
 assert sum(len(m['content'].encode()) for m in r['messages'])+len(json.dumps(r['format']).encode())+512+8192<=49152
 record={'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'request':r};dest=out/(turn+'.json');dump(dest,record);remaining=600-(time.monotonic()-start)
 if remaining<=0:raise RuntimeError('time budget exhausted')
 try:record['result']=Ollama().complete(r,timeout=min(300,remaining));record['contract_violations']=violations(r,record['result'])
 except Exception as e:record['error']=str(e)
 dump(dest,record);dest.chmod(0o600)
 print(dest.name,json.dumps({'content':record.get('result',{}).get('response',{}).get('message',{}).get('content'),'error':record.get('error'),'contract':record.get('contract_violations')}),flush=True)
