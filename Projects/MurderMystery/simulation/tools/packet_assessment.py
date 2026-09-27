"""Compare a local model to a frozen symbolic player's exact received packets."""
import hashlib,json,random,time
from pathlib import Path
from dojo.models import Ollama
from dojo.runner import dump
from dojo.symbolic import prepare

def main():
    root=Path('local-private/movie');out=root/'packet-assessment';out.mkdir(mode=0o700)
    case_path=root/'symbolic/movie-strict-sampled.json';trace_path=root/'symbolic/trace-strict-seed17.json'
    case=json.loads(case_path.read_text());trace=json.loads(trace_path.read_text());players,packets=prepare(case)
    roster=json.loads((root/'adapted.json').read_text())['players'];names={p:r['name'] for p,r in roster.items()};choices=list(names.values());random.Random(23).shuffle(choices)
    dump(out/'plan.json',{'method':'Gemma receives only the known authoritative predicate assertions and clue packets; irrelevant background omitted of each nonculprit from the frozen seeded transport. No symbolic decisions, rankings, remaining candidates, or culprit label provided. Same private own-innocence convention. Randomized candidate order frozen before calls. This is a structured-information diagnostic, not natural dialogue.','case_sha256':hashlib.sha256(case_path.read_bytes()).hexdigest(),'trace_sha256':hashlib.sha256(trace_path.read_bytes()).hexdigest(),'max_calls':7,'max_seconds':900,'per_call_seconds':180,'model':'gemma4:e4b-it-qat','thinking':True,'context':32768,'tokens':8192,'seed':23})
    start=time.monotonic();rows=[]
    for who in players:
      if who not in case['private_exclusions']:continue
      facts=[];clues=[]
      for key in trace['known_packets'][who]:
        item=packets[key]
        if item['kind']=='fact':
          for a in item['assertions']:
            if set(a.get('requires',[])) <= set(trace['known_packets'][who]):
              facts.append({'subject':names[item['subject']],'predicate':a['predicate'],'value':a['value'],'source':a['source_atom']})
        else:clues.append({k:item[k] for k in ['id','predicate','expected','strength','source_atom']})
      view={'self':names[who],'candidates':choices,'own_private_knowledge':'Your character is not the murderer.','facts':facts,'clues':clues,'task':'At this murder mystery party, vote for exactly one most likely murderer. These fixed fact packets and clue cards are authoritative within this diagnostic. Hard clues require the stated predicate value; soft clues cannot exclude anyone. Missing facts are unknown, not false. Use the available matches and contradictions to make your best guess even if not logically certain. Return only suspect.'}
      payload={'model':'gemma4:e4b-it-qat','messages':[{'role':'system','content':'You are playing one participant in a fictional murder mystery party. Use only the supplied information.'},{'role':'user','content':json.dumps(view)}],'format':{'type':'object','properties':{'suspect':{'type':'string','enum':choices}},'required':['suspect'],'additionalProperties':False},'stream':False,'think':True,'keep_alive':'2m','options':{'temperature':0.7,'seed':23,'num_ctx':32768,'num_predict':8192}}
      if sum(len(m['content'].encode()) for m in payload['messages'])+len(json.dumps(payload['format']).encode())+512+8192>32768:raise ValueError('Context bound exceeded')
      d={'request':payload};path=out/f'{who}.json';dump(path,d);remaining=900-(time.monotonic()-start)
      if remaining<=0:raise RuntimeError('Time budget exhausted')
      try:
        d['result']=Ollama().complete(payload,timeout=min(180,remaining));raw=d['result']['response'];a=json.loads(raw['message']['content']);d['valid']=set(a)=={'suspect'} and a['suspect'] in choices and raw.get('done_reason')!='length'
      except Exception as e:d['error']=str(e);d['valid']=False;a={}
      dump(path,d);path.chmod(0o600)
      row={'player':who,'suspect':a.get('suspect'),'valid':d['valid'],'error':d.get('error'),'seconds':d.get('result',{}).get('wall_seconds')};rows.append(row);dump(out/'summary.json',rows);print(json.dumps(row),flush=True)
if __name__=='__main__':main()
