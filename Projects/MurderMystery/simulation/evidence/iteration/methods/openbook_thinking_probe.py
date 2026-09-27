import json,copy,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from dojo.models import Ollama
from dojo.audit import violations
from dojo.runner import dump
source=Path('local-private/movie/iteration-openbook/gemma4.json');out=Path('local-private/movie/iteration-openbook-thinking');out.mkdir(mode=0o700)
r=copy.deepcopy(json.loads(source.read_text())['request']);r['think']=True;r['options']['num_predict']=8192
assert sum(len(m['content'].encode()) for m in r['messages'])+len(json.dumps(r['format']).encode())+512+8192<=32768
dump(out/'plan.json',{'max_calls':1,'max_seconds':300,'method':'Same open-book Gemma request and seed; enable native thinking and expand output budget to8192. No new information.'})
d={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'request':r};p=out/'gemma4.json';dump(p,d)
try:d['result']=Ollama().complete(r,timeout=300);d['contract_violations']=violations(r,d['result'])
except Exception as e:d['error']=str(e)
dump(p,d);p.chmod(0o600)
print(json.dumps({'content':d.get('result',{}).get('response',{}).get('message',{}).get('content'),'seconds':d.get('result',{}).get('wall_seconds'),'violations':d.get('contract_violations'),'error':d.get('error')}))
