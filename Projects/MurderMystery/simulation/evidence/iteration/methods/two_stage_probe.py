import sys,copy,json,time,hashlib
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from dojo.models import Ollama
from dojo.audit import violations
from dojo.runner import dump
root=Path('local-private/movie');out=root/'iteration-two-stage';out.mkdir(mode=0o700)
models=['qwen3.5:9b','gemma4:e4b-it-qat'];cases=['t00070','t00071'];start=time.monotonic();count=0
plan={'models':models,'cases':cases,'seed':17,'max_calls':8,'max_seconds':1200,'review_tokens':3072,'decision_tokens':768,'context':32768,'thinking':False,'method':'Same visible player history and private role. Fallible generated candidate review precedes one final decision. Review and decision retained; no evaluator truth supplied.'};dump(out/'plan.json',plan)
for model in models:
 for case in cases:
  source=root/'dialogue-four-partners/turns'/f'{case}.json';original=json.loads(source.read_text())['request'];messages=copy.deepcopy(original['messages']);context=json.loads(messages[1]['content']);current=json.loads(messages[-1]['content']);names=list(context['cast'].values())
  review_schema={'type':'object','properties':{'candidates':{'type':'array','minItems':8,'maxItems':8,'items':{'type':'object','properties':{'candidate':{'type':'string','enum':names},'supports':{'type':'string','maxLength':240},'rules_out':{'type':'string','maxLength':240},'unknown':{'type':'string','maxLength':160}},'required':['candidate','supports','rules_out','unknown'],'additionalProperties':False}},'best_supported':{'type':'string','enum':names+['undetermined']},'explanation':{'type':'string','maxLength':400}},'required':['candidates','best_supported','explanation'],'additionalProperties':False}
  messages[0]={'role':'system','content':'You are simulating a person playing their assigned character at a murder mystery party. Privately review your available evidence before deciding whom to accuse. Your character sheet supplies your own facts, not other characters\' facts. The chronological history labels who said each statement; preserve that ownership. Host-delivered printed clue cards are rules of this puzzle. Other guests\' statements can be mistaken or deceptive. Use only the supplied information. Missing information is unknown, not a match and not a contradiction. A candidate explicitly contradicted by a clue cannot be your supported choice. Your own role information about your innocence also matters. Do not infer personality from a job title or a different unrelated trait. List all cast members once, separating support, exclusions, and unknowns. An undetermined result is permitted. Return the requested review JSON, not public dialogue.'}
  messages[-1]={'role':'user','content':json.dumps({'self':current['self'],'self_name':current['self_name'],'instruction':'Review every candidate against your received clue cards and character knowledge. Attribute each supplied fact to its actual owner. Decide whether one candidate is supported; do not make unknown facts true to force a result.','visible_event_ids':[e['id'] for e in current['observations']]})}
  payload=copy.deepcopy(original);payload['messages']=messages;payload['model']=model;payload['format']=review_schema;payload['options'].update(num_ctx=32768,num_predict=3072,seed=17)
  prefix=f'{model.split(":")[0]}-{case}';review={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'stage':'review','request':payload};path=out/(prefix+'-review.json');dump(path,review)
  if count>=8 or time.monotonic()-start>=1200:raise RuntimeError('batch budget')
  count+=1
  try:
   review['result']=Ollama().complete(payload,timeout=min(180,1200-(time.monotonic()-start)))
   raw=review['result']['response'];parsed=json.loads(raw['message']['content'])
   if raw.get('done_reason')=='length':raise ValueError('truncated review')
   if sorted(r['candidate'] for r in parsed['candidates'])!=sorted(names):raise ValueError('candidate coverage mismatch')
  except Exception as e:
   review['error']=str(e);dump(path,review);print(prefix,'review failed',review['error'],flush=True);continue
  dump(path,review);path.chmod(0o600)
  decision=copy.deepcopy(original);decision['model']=model;decision['options']['num_ctx']=32768
  decision['messages'][-1:-1]=[{'role':'assistant','content':'Private evidence review (fallible, generated from the preceding evidence):\n'+raw['message']['content']}]
  final=json.loads(decision['messages'][-1]['content']);final['instruction']+=' Use your review as a fallible aid. Give one consistent final answer. Do not accuse someone whom your own supplied evidence rules out. If the review conflicts with the original evidence, use the original evidence. Clearly separate a tentative best candidate from a proven unique solution.';decision['messages'][-1]['content']=json.dumps(final)
  record={'source_sha256':review['source_sha256'],'stage':'decision','review_record':path.name,'request':decision};p=out/(prefix+'-decision.json');dump(p,record)
  if count>=8 or time.monotonic()-start>=1200:raise RuntimeError('batch budget')
  count+=1
  try:record['result']=Ollama().complete(decision,timeout=min(120,1200-(time.monotonic()-start)));record['contract_violations']=violations(decision,record['result'])
  except Exception as e:record['error']=str(e)
  dump(p,record);p.chmod(0o600)
  print(prefix,record.get('result',{}).get('response',{}).get('message',{}).get('content','failed'),flush=True)
