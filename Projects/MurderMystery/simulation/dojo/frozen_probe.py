"""Compare prompt profiles on an existing synthetic request and no-report control."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from .core import EVIDENCE_GUIDANCE, State, messages_for
from .models import Ollama
from .runner import dump

def validate_legacy_assessment(messages):
 # Obtain the current legacy template without depending on test data or a substring.
 minimal={'id':'template','players':{'p1':{'brief':'','name':'A'},'p2':{'brief':'','name':'B'}},'scenes':[]}
 expected=messages_for(State(minimal),'p1',['p1'],'assessment','',True)[0]
 if len(messages)!=2 or messages[0]!=expected or not json.loads(messages[-1]['content']).get('final_assessment'):
  raise ValueError('Expected an exact legacy final-assessment request')

def without_incoming_report(messages):
 """Remove one final incoming report, retaining only preceding self speech.

 This does not assert the retained self speech is uninformed. Inspect the
 control; broader histories need explicitly authored counterfactuals.
 """
 view=json.loads(messages[-1]['content'])
 incoming=[i for i,e in enumerate(view['observations']) if e['actor']!=view['self']]
 if len(incoming)!=1 or incoming[0]!=len(view['observations'])-1:
  raise ValueError('Requires exactly one incoming report, last in the snapshot')
 view['observations']=view['observations'][:-1]
 result=copy.deepcopy(messages)
 result[-1]['content']=json.dumps(view,ensure_ascii=False)
 return result

def record_call(path, record, backend):
 dump(path,record)
 try: record['result']=backend.complete(record['request'])
 except Exception as e:
  record['error']=str(e);dump(path,record);raise
 dump(path,record)

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('record',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 if a.out.exists(): raise ValueError('Use a new output directory')
 a.out.mkdir(parents=True)
 base=json.loads(a.record.read_text())['request']['messages']
 validate_legacy_assessment(base)
 control=without_incoming_report(base)
 for model in ('qwen3.5:9b','gemma4:e4b-it-qat'):
  backend=Ollama(model,context=8192,tokens=768,seed=1)
  for condition in ('delivered','no_report'):
   for profile in ('legacy','grounded-v1'):
    messages=copy.deepcopy(base)
    if profile=='grounded-v1': messages[0]['content']+=EVIDENCE_GUIDANCE
    if condition=='no_report':
     messages[-1]=copy.deepcopy(control[-1])
    record={'source_sha256':hashlib.sha256(a.record.read_bytes()).hexdigest(),'model':model,'condition':condition,'profile':profile,'request':backend.payload(messages)}
    path=a.out/(model.split(':')[0]+'-'+condition+'-'+profile+'.json')
    record_call(path,record,backend)
    print(path.name,flush=True)
if __name__=='__main__':main()
