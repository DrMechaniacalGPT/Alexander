"""Follow-up: one explicit vote, with no competing prose accusation field."""
import copy,hashlib,json,time
from pathlib import Path
from dojo.models import Ollama
from dojo.runner import dump

def choice_request(original,names):
    p=copy.deepcopy(original);v=json.loads(p['messages'][-1]['content'])
    if not v.get('final_assessment'):raise ValueError('Expected assessment')
    v['instruction']='The murder mystery party ends with a vote. Using only your own character card and what you heard, choose exactly one most likely murderer from these names: '+', '.join(names)+'. You must make your best guess even if uncertain. Return only the suspect field required by the output schema.'
    v['next_turn']='Cast your private vote.'
    p['messages'][-1]['content']=json.dumps(v,ensure_ascii=False)
    p['format']={'type':'object','properties':{'suspect':{'type':'string','enum':list(names)}},'required':['suspect'],'additionalProperties':False}
    return p

def main():
    out=Path('local-private/movie/choice-only');out.mkdir(mode=0o700)
    names=[p['name'] for p in json.loads(Path('local-private/movie/adapted.json').read_text())['players'].values()]
    sources=['iteration-open-gemma','iteration-clarify-gemma-large'];start=time.monotonic();rows=[]
    dump(out/'plan.json',{'method':'Same original evidence/model/budgets; replace only final request instruction and schema with required suspect-only vote. No explanation/consistency metric available.','sources':sources,'max_calls':14,'max_seconds':1800,'per_call_seconds':180})
    for run in sources:
      for source in sorted((Path('local-private/movie')/run/'turns').glob('*.json')):
        p=json.loads(source.read_text())['request'];v=json.loads(p['messages'][-1]['content'])
        if not v.get('final_assessment') or v['self']=='p1':continue
        p=choice_request(p,names);d={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'request':p};path=out/f'{run}-{v["self"]}.json';dump(path,d)
        remaining=1800-(time.monotonic()-start)
        if remaining<=0:raise RuntimeError('Budget exhausted')
        try:
          d['result']=Ollama().complete(p,timeout=min(180,remaining));raw=d['result']['response'];a=json.loads(raw['message']['content'])
          d['valid']=set(a)=={'suspect'} and a['suspect'] in names and raw.get('done_reason')!='length'
        except Exception as e:d['error']=str(e);a={};d['valid']=False
        dump(path,d);path.chmod(0o600)
        row={'run':run,'player':v['self'],'suspect':a.get('suspect'),'valid':d['valid'],'error':d.get('error'),'seconds':d.get('result',{}).get('wall_seconds')};rows.append(row);dump(out/'summary.json',rows);print(json.dumps(row),flush=True)
if __name__=='__main__':main()
