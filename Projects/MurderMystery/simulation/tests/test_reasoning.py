import json
import unittest
from dojo.benchmark import request
from dojo.models import Ollama
from dojo.core import State,messages_for
from test_dojo import case

class Reasoning(unittest.TestCase):
 def test_rubric_and_other_roles_never_enter_prompt(self):
  row={'id':'SECRET EVALUATOR LABEL','brief':'You are Cal.','events':[['p2','A report.']], 'question':'What did you hear?','rubric':'HIDDEN ANSWER'}
  payload=request(row,'grounded-v1',Ollama(context=8192,tokens=768))
  text=json.dumps(payload)
  for hidden in ('SECRET EVALUATOR LABEL','PRIVATE OTHER ROLE','HIDDEN ANSWER'):
   self.assertNotIn(hidden,text)
  self.assertIn('A report.',text)
 def test_profile_changes_only_system_prompt(self):
  state=State(case())
  old=messages_for(state,'p2',['p2'],'s1','Speak')
  explicit=messages_for(state,'p2',['p2'],'s1','Speak',prompt_profile='legacy')
  new=messages_for(state,'p2',['p2'],'s1','Speak',prompt_profile='grounded-v1')
  self.assertEqual(old,explicit)
  self.assertEqual(old[1],new[1])
  self.assertTrue(new[0]['content'].startswith(old[0]['content']))
  self.assertNotIn('VIOLET-5831',json.dumps(new))
 def test_unknown_profile_fails(self):
  with self.assertRaises(ValueError):
   messages_for(State(case()),'p2',['p2'],'s1','Speak',prompt_profile='typo')

class BenchmarkJournals(unittest.TestCase):
 def test_resume_no_duplicate_and_changed_request_rejected(self):
  from dojo.benchmark import collect
  from dojo.models import Stub
  import tempfile
  class Counting(Stub):
   count=0
   def complete(self,*a,**kw):
    self.count+=1
    return super().complete(*a,**kw)
  b=Counting({}); row={'id':'probe','brief':'You are Cal.','events':[],'question':'What do you know?'}
  with tempfile.TemporaryDirectory() as d:
   collect([row],d,b); collect([row],d,b)
   self.assertEqual(b.count,2)
   row['question']='Changed question'
   with self.assertRaises(ValueError): collect([row],d,b)
 def test_failed_request_is_not_silently_retried(self):
  from dojo.benchmark import collect
  from dojo.models import Stub
  import tempfile
  class Broken(Stub):
   def complete(self,*a,**kw): raise TimeoutError('test timeout')
  row={'id':'probe','brief':'You are Cal.','events':[],'question':'What do you know?'}
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(TimeoutError): collect([row],d,Broken({}))
   with self.assertRaises(RuntimeError): collect([row],d,Stub({}))

class ReviewRegressions(unittest.TestCase):
 def test_rubric_changes_cannot_silently_reuse_outputs(self):
  from dojo.benchmark import collect
  from dojo.models import Stub
  import tempfile
  row={'id':'a','brief':'Cal','question':'Answer','events':[],'rubric':'original'}
  with tempfile.TemporaryDirectory() as d:
   collect([row],d,Stub({}))
   row['rubric']='revised'
   with self.assertRaises(ValueError): collect([row],d,Stub({}))
 def test_control_rejects_post_report_echo_and_multiple_sources(self):
  from dojo.frozen_probe import without_incoming_report
  def messages(events):return [{'content':json.dumps({'self':'p1','observations':events})}]
  a={'actor':'p1','content':'Where?'};b={'actor':'p2','content':'cabinet 4'}
  self.assertEqual(json.loads(without_incoming_report(messages([a,b]))[0]['content'])['observations'],[a])
  for events in ([b,a],[a,b,b],[]):
   with self.assertRaises(ValueError): without_incoming_report(messages(events))
 def test_frozen_error_cause_preserved(self):
  from dojo.frozen_probe import record_call
  from pathlib import Path
  import tempfile
  class Broken:
   def complete(self,payload): raise TimeoutError('diagnostic timeout')
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'turn.json'
   with self.assertRaises(TimeoutError): record_call(path,{'request':{}},Broken())
   self.assertEqual(json.loads(path.read_text())['error'],'diagnostic timeout')
 def test_v2_preserves_choice_to_hide_possession(self):
  prompt=messages_for(State(case()),'p1',['p1','p2'],'s1','Speak',prompt_profile='grounded-v2')[0]['content']
  self.assertNotIn('acknowledge possession without printing it',prompt)
  self.assertIn('whether to acknowledge possessing a secret remains your choice',prompt)
 def test_legacy_system_matches_historical_record(self):
  from pathlib import Path
  expected=json.loads((Path(__file__).parent/'fixtures/legacy-final.json').read_text())
  actual=messages_for(State(case()),'p3',['p3'],'assessment','Answer',True)
  self.assertEqual(actual[0],expected[0])
 def test_cli_default_manifest_and_replay(self):
  import subprocess,sys,tempfile
  from pathlib import Path
  root=Path(__file__).resolve().parents[1]
  with tempfile.TemporaryDirectory() as d:
   command=[sys.executable,'-m','dojo.runner',str(root/'fixtures/02_private_relay.json'),'--out',d]
   subprocess.run(command,check=True,capture_output=True)
   self.assertNotIn('prompt_profile',json.loads(Path(d,'manifest.json').read_text())['config'])
   subprocess.run(command+['--replay'],check=True,capture_output=True)
   changed=subprocess.run(command+['--prompt-profile','grounded-v2'],capture_output=True)
   self.assertNotEqual(changed.returncode,0)
 def test_identity_cues_preserve_information_and_event_store(self):
  import copy
  s=State(case());s.emit('a','p1',['p1','p2'],'A report','s1')
  before=copy.deepcopy(s.events)
  view=json.loads(messages_for(s,'p2',['p1','p2'],'s1','Speak',prompt_profile='grounded-v2')[1]['content'])
  self.assertEqual(s.events,before)
  self.assertEqual(view['self_name'],'Bea')
  self.assertEqual(view['observations'][0]['actor_name'],'Ari')
  self.assertEqual(view['audience_names'],{'p1':'Ari','p2':'Bea'})
  self.assertNotIn('VIOLET-5831',json.dumps(view))
  self.assertNotIn('cabinet 4',json.dumps(view))

class ContractAudit(unittest.TestCase):
 def test_assessment_speech_and_unseen_citations_flagged(self):
  from dojo.audit import violations
  row={'id':'a','brief':'Cal','events':[['p2','A report']],'question':'Answer'}
  payload=request(row,'legacy',Ollama(context=8192,tokens=768))
  a={'say':'public','private_note':'','conclusion':'Unknown','evidence':['hidden'],'action':'none'}
  errors=violations(payload,{'response':{'message':{'content':json.dumps(a)}}})
  self.assertIn('evidence: unseen citation',errors)
  self.assertIn('private assessment contains public speech/action',errors)
 def test_available_citation_is_not_semantic_validation(self):
  from dojo.audit import violations
  row={'id':'a','brief':'Cal','events':[['p2','The receipt is in cabinet 4.']],'question':'Answer'}
  payload=request(row,'legacy',Ollama(context=8192,tokens=768))
  a={'say':'','private_note':'','conclusion':'The moon is cheese.','evidence':['e00000'],'action':'none'}
  self.assertEqual(violations(payload,{'response':{'message':{'content':json.dumps(a)}}}),[])
 def test_frozen_comparison_rejects_every_nonlegacy_profile(self):
  from dojo.frozen_probe import validate_legacy_assessment
  for profile in ('legacy','grounded-v1','grounded-v2'):
   messages=messages_for(State(case()),'p3',['p3'],'assessment','Answer',True,prompt_profile=profile)
   if profile=='legacy':validate_legacy_assessment(messages)
   else:
    with self.assertRaises(ValueError):validate_legacy_assessment(messages)
