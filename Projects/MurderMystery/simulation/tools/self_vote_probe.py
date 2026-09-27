"""Follow-up on three observed self-votes from an explicitly innocent player."""
import copy,hashlib,json,time
from pathlib import Path
from dojo.models import Ollama
from dojo.runner import dump

def main():
 root=Path('local-private/movie');out=root/'self-vote-fix';out.mkdir(mode=0o700);rows=[];start=time.monotonic()
 dump(out/'plan.json',{'method':'Three exact suspect-only contexts with observed self-votes. Remove own character from candidate enum and candidate-list instruction because their own private card explicitly establishes innocence. No other evidence or settings change.','max_calls':3,'max_seconds':540,'per_call_seconds':180})
 for run,who in [('iteration-open-gemma','p6'),('iteration-clarify-gemma-large','p5'),('iteration-clarify-gemma-large','p6')]:
  path=root/'choice-only'/f'{run}-{who}.json';old=json.loads(path.read_text());p=copy.deepcopy(old['request']);v=json.loads(p['messages'][-1]['content']);own=v['self_name'];names=p['format']['properties']['suspect']['enum'];eligible=[n for n in names if n!=own]
  assert len(eligible)==len(names)-1
  v['instruction']=v['instruction'].replace(', '.join(names),', '.join(eligible))+' Your own private character card says you did not commit the murder, so your own character is not an eligible vote.'
  p['messages'][-1]['content']=json.dumps(v,ensure_ascii=False);p['format']['properties']['suspect']['enum']=eligible;d={'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'request':p};dest=out/f'{run}-{who}.json';dump(dest,d)
  remaining=540-(time.monotonic()-start)
  if remaining<=0:raise RuntimeError('Budget exhausted')
  try:
   d['result']=Ollama().complete(p,timeout=min(180,remaining));raw=d['result']['response'];ans=json.loads(raw['message']['content']);d['valid']=set(ans)=={'suspect'} and ans['suspect'] in eligible and raw.get('done_reason')!='length'
  except Exception as e:d['error']=str(e);d['valid']=False;ans={}
  dump(dest,d);dest.chmod(0o600);row={'run':run,'player':who,'suspect':ans.get('suspect'),'valid':d['valid'],'error':d.get('error'),'seconds':d.get('result',{}).get('wall_seconds')};rows.append(row);dump(out/'summary.json',rows);print(json.dumps(row),flush=True)
if __name__=='__main__':main()
