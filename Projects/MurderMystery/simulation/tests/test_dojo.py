import copy
import json
import tempfile
import unittest
from pathlib import Path
from dojo.core import State, InvalidAction, messages_for
from dojo.models import Stub, Ollama
from dojo.runner import run, encounters
import random

ROOT=Path(__file__).resolve().parents[1]
def action(text='hello', evidence=None):
 return {'say':text,'private_note':'SECRET INTENTION','evidence':evidence or [],'conclusion':'Unknown','action':'none'}
def case():
 return json.loads((ROOT/'fixtures/02_private_relay.json').read_text())
def config(**kw):
 return dict({'backend':'stub','seed':1,'max_calls':20,'max_seconds':30},**kw)

class Boundaries(unittest.TestCase):
 def test_private_role_not_in_other_prompt(self):
  s=State(case()); prompt=json.dumps(messages_for(s,'p2',['p1','p2'],'s1','Speak'))
  self.assertNotIn('VIOLET-5831',prompt); self.assertNotIn('cabinet 4',prompt)
 def test_delivery_and_rumor_are_distinct(self):
  s=State(case()); e=s.emit('x','p1',['p1','p2'],'receipt is in cabinet 4','s1')
  self.assertEqual(s.observations('p3'),[])
  s.apply('t','p2',['p2','p3'],action('Ari says it is in cabinet 4',[e['id']]),'s1')
  seen=s.observations('p3'); self.assertEqual(len(seen),1)
  self.assertEqual(seen[0]['actor'],'p2'); self.assertNotIn('SECRET INTENTION',json.dumps(seen))
 def test_evidence_id_must_be_visible(self):
  s=State(case()); e=s.emit('x','host',['p1'],'secret','s1')
  with self.assertRaises(InvalidAction): s.apply('t','p2',['p2'],action(evidence=[e['id']]),'s1')
  self.assertEqual(s.private['p2'],[])
 def test_absent_and_late_join_no_backfill(self):
  s=State(case()); s.present.remove('p3')
  with self.assertRaises(InvalidAction): s.apply('t','p1',['p1','p3'],action(),'s1')
  s.apply('t','p1',['p1','p2'],action('earlier'),'s1'); s.present.add('p3')
  s.apply('u','p2',['p2','p3'],action('later'),'s1')
  self.assertEqual([e['content'] for e in s.observations('p3')],['later'])
 def test_bounded_memory_not_omniscient_summary(self):
  c=case(); c['players']['p2']['policy']={'memory_events':1}; s=State(c)
  s.emit('a','p1',['p2'],'old','s1'); s.emit('b','p1',['p2'],'new','s1')
  self.assertEqual([e['content'] for e in s.observations('p2')],['new'])
  self.assertEqual(len(s.events),2)
 def test_duplicate_and_impossible_action_rejected(self):
  s=State(case()); s.apply('x','p1',['p1','p2'],action(),'s1')
  with self.assertRaises(InvalidAction): s.apply('x','p1',['p1','p2'],action(),'s1')
  a=action(); a['action']='create_magic_artifact'
  with self.assertRaises(InvalidAction): s.apply('y','p1',['p1','p2'],a,'s1')
  self.assertEqual(len(s.events),1)
 def test_group_delivers_to_exact_members(self):
  s=State(case()); s.apply('x','p1',['p1','p2','p3'],action(),'s1')
  self.assertEqual([len(s.observations(p)) for p in s.case['players']],[1,1,1])
 def test_history_cannot_be_changed_by_claim(self):
  s=State(case()); original=copy.deepcopy(s.case['truth'])
  s.apply('x','p1',['p1','p2'],action('The receipt was destroyed.'),'s1')
  self.assertEqual(s.case['truth'],original)

class Execution(unittest.TestCase):
 def test_resume_replay_no_new_calls_or_duplicate_events(self):
  class Counting(Stub):
   calls=0
   def complete(self,*a,**k): self.calls+=1; return super().complete(*a,**k)
  b=Counting({p:action() for p in case()['players']})
  with tempfile.TemporaryDirectory() as d:
   first=run(case(),d,b,config()); events=Path(d,'events.json').read_bytes(); calls=b.calls
   again=run(case(),d,b,config(),replay=True)
   self.assertEqual(first['status'],'complete'); self.assertEqual(again['status'],'complete')
   self.assertEqual(b.calls,calls); self.assertEqual(Path(d,'events.json').read_bytes(),events)
   run(case(),d,b,config()); self.assertEqual(b.calls,calls)
 def test_bad_output_is_retained_and_stops(self):
  class Bad(Stub):
   def complete(self,*a,**k): return {'response':{'message':{'content':'not json'}},'wall_seconds':0}
  with tempfile.TemporaryDirectory() as d:
   result=run(case(),d,Bad({}),config()); self.assertEqual(result['status'],'incomplete')
   raw=json.loads(next(Path(d,'turns').glob('*.json')).read_text())
   self.assertIn('invalid',raw['attempts'][0]); self.assertEqual(result['events'],0)
 def test_budget_and_manifest_change(self):
  with tempfile.TemporaryDirectory() as d:
   result=run(case(),d,Stub({}),config(max_calls=1)); self.assertEqual(result['status'],'incomplete')
   self.assertEqual(result['usage']['requests'],1)
   changed=case(); changed['public']='changed'
   with self.assertRaises(ValueError): run(changed,d,Stub({}),config(max_calls=1))
 def test_random_pairs_no_double_booking(self):
  schedule=list(encounters({'mode':'random_pairs','windows':2},list('abcde'),random.Random(4)))
  for window in range(2):
   members=[p for e in schedule if e['window']==window for p in e['participants']]
   self.assertEqual(len(members),len(set(members))); self.assertEqual(len(members),4)
 def test_context_and_endpoint_guards(self):
  with self.assertRaises(ValueError): Ollama(endpoint='https://example.com')
  with self.assertRaises(ValueError): Ollama(context=1024).payload([{'content':'x'*2000}])

class Regression(unittest.TestCase):
 def test_final_answer_is_private_and_nonempty(self):
  s=State(case()); a=action(); a['conclusion']='Private accusation'
  s.apply('x','p1',['p1'],a,'assessment',True)
  self.assertNotIn('Private accusation',json.dumps(s.view('p2')))
  a['conclusion']=''
  with self.assertRaises(InvalidAction): s.apply('y','p2',['p2'],a,'assessment',True)
 def test_scene_action_does_not_satisfy_later_scene(self):
  c=case(); c['scenes']=[{'id':'early','encounters':[{'participants':['p1','p2'],'speakers':['p1'],'legal_actions':['signal']}]},
   {'id':'late','encounters':[{'participants':['p1','p2'],'speakers':['p2']}],'requires_action':{'player':'p1','action':'signal'}}]
  a=action(); a['action']='signal'
  with tempfile.TemporaryDirectory() as d:
   result=run(c,d,Stub({'p1':a,'p2':action()}),config())
   self.assertEqual(result['status'],'incomplete'); self.assertIn('Prescribed action',result['failure'])
 def test_contact_trigger_or_budget_explicit_and_scene_local(self):
  c=case(); c['scenes']=[{'id':'early','encounters':[{'participants':['p1','p3']}]},
   {'id':'late','encounters':[{'participants':['p1','p2']},{'participants':['p1','p3']}],
    'transition_after_contacts':{'player':'p1','count':2}}]
  with tempfile.TemporaryDirectory() as d:
   result=run(c,d,Stub({}),config()); self.assertEqual(result['status'],'complete')
   self.assertEqual(result['transitions'][1]['reason'],'contact_trigger')
   self.assertEqual(result['events'],6)
  c['scenes'][1]['transition_after_contacts']['count']=3
  with tempfile.TemporaryDirectory() as d:
   result=run(c,d,Stub({}),config()); self.assertEqual(result['transitions'][1]['reason'],'schedule_budget')
   self.assertEqual(result['transitions'][1]['contact_count'],2)
 def test_pending_success_resumes_without_regeneration(self):
  with tempfile.TemporaryDirectory() as d:
   run(case(),d,Stub({}),config())
   path=Path(d,'turns/t00000.json'); rec=json.loads(path.read_text()); del rec['accepted'];path.write_text(json.dumps(rec))
   class Never(Stub):
    def complete(self,*a,**k): raise AssertionError('Should use journaled raw response')
   result=run(case(),d,Never({}),config());self.assertEqual(result['status'],'complete')
 def test_truncated_response_is_not_accepted(self):
  class Truncated(Stub):
   def complete(self,*a,**k):
    r=super().complete(*a,**k);r['response']['done_reason']='length';return r
  with tempfile.TemporaryDirectory() as d:
   result=run(case(),d,Truncated({}),config()); self.assertEqual(result['status'],'incomplete')
   self.assertIn('Truncated',result['failure'])
 def test_no_accusation_visible_before_reveal(self):
  c=case(); c['scenes']=[{'id':'d','mode':'delivery_only','deliveries':[]}]
  with tempfile.TemporaryDirectory() as d:
   result=run(c,d,Stub({}),config())
   self.assertEqual(result['status'],'complete')
   rec=json.loads(Path(d,'turns/t00001.json').read_text())
   self.assertNotIn('conclusions',rec['request']['messages'][1]['content'])

class JournalIntegrity(unittest.TestCase):
 def test_modified_accepted_action_is_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   run(case(),d,Stub({}),config())
   path=Path(d,'turns/t00000.json');r=json.loads(path.read_text());r['accepted']['say']='tampered';path.write_text(json.dumps(r))
   result=run(case(),d,Stub({}),config(),replay=True)
   self.assertEqual(result['status'],'incomplete');self.assertIn('differs from recorded',result['failure'])

class Locking(unittest.TestCase):
 def test_concurrent_writer_is_rejected(self):
  import fcntl
  with tempfile.TemporaryDirectory() as d:
   with Path(d,'.run.lock').open('w') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    with self.assertRaises(RuntimeError): run(case(),d,Stub({}),config())

class Continuation(unittest.TestCase):
 def test_explicit_fork_reuses_only_accepted_prefix(self):
  with tempfile.TemporaryDirectory() as d:
   old=Path(d,'old'); new=Path(d,'new')
   first=run(case(),old,Stub({}),config(max_calls=1));self.assertEqual(first['status'],'incomplete')
   result=run(case(),new,Stub({}),config(),continue_from=old)
   self.assertEqual(result['status'],'complete'); self.assertEqual(result['usage']['inherited_turns'],1)
   self.assertEqual(result['usage']['new_requests'],6)
   self.assertEqual(json.loads((old/'summary.json').read_text())['status'],'incomplete')
   with self.assertRaises(ValueError): run(case(),Path(d,'bad'),Stub({}),config(seed=2),continue_from=old)

class Epilogue(unittest.TestCase):
 def test_previous_epilogue_action_cannot_satisfy_next(self):
  c=case(); c['scenes']=[{'id':'empty','mode':'delivery_only'}]
  c['epilogue']=[{'participants':['p1','p2'],'speakers':['p1'],'instruction':'confess','legal_actions':['none','confess'],'required_action':'confess'},
   {'participants':['p1','p2'],'speakers':['p2'],'instruction':'confess','legal_actions':['none','confess'],'required_action':'confess'}]
  class FirstOnly(Stub):
   def complete(self,payload,**kw):
    view=json.loads(payload['messages'][1]['content']);a=action()
    if view['scene']=='epilogue' and view['self']=='p1': a['action']='confess'
    return {'response':{'message':{'content':json.dumps(a)}},'wall_seconds':0}
  with tempfile.TemporaryDirectory() as d:
   result=run(c,d,FirstOnly({}),config());self.assertEqual(result['status'],'incomplete')
   self.assertIn('epilogue action',result['failure'])

class OutputSchema(unittest.TestCase):
 def test_schema_only_offers_visible_evidence(self):
  s=State(case()); private=s.emit('hidden','host',['p1'],'private','s1')
  shared=s.emit('visible','host',['p2'],'public to p2','s1')
  payload=Ollama(context=8192).payload(messages_for(s,'p2',['p1','p2'],'s1','Speak'))
  ids=payload['format']['properties']['evidence']['items']['enum']
  self.assertEqual(ids,[shared['id']]);self.assertNotIn(private['id'],ids)
 def test_schema_empty_evidence_at_start(self):
  s=State(case());payload=Ollama(context=8192).payload(messages_for(s,'p2',['p1','p2'],'s1','Speak'))
  self.assertEqual(payload['format']['properties']['evidence']['maxItems'],0)

if __name__=='__main__': unittest.main()
