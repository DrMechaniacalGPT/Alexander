import copy
import json
import tempfile
import unittest
from pathlib import Path
from dojo.core import State,messages_for
from dojo.models import Ollama,Stub
from dojo.runner import run
from test_dojo import case,config,action

class StrictContract(unittest.TestCase):
 def test_phase_specific_schema_and_explicit_thinking(self):
  state=State(case());backend=Ollama(context=8192,tokens=2048,thinking=True,strict_output=True)
  final=backend.payload(messages_for(state,'p1',['p1'],'assessment','Answer',True))
  speech=backend.payload(messages_for(state,'p1',['p1','p2'],'s1','Speak'))
  self.assertTrue(final['think'])
  self.assertEqual(final['format']['properties']['say']['enum'],[''])
  self.assertEqual(final['format']['properties']['conclusion']['minLength'],1)
  self.assertEqual(speech['format']['properties']['conclusion']['enum'],[''])
  self.assertNotIn('enum',speech['format']['properties']['say'])
 def test_stray_final_speech_rejected_and_retained(self):
  class Bad(Stub):
   def complete(self,payload,timeout=120):
    a=action('Forbidden assessment speech');a['conclusion']='Unknown'
    return {'response':{'message':{'content':json.dumps(a)},'done_reason':'stop'},'wall_seconds':0}
  c=case();c['scenes']=[]
  with tempfile.TemporaryDirectory() as d:
   result=run(c,d,Bad({},strict_output=True),config(strict_output=True))
   self.assertEqual(result['status'],'incomplete');self.assertEqual(result['events'],0)
   record=json.loads(Path(d,'turns/t00000.json').read_text())
   self.assertNotIn('accepted',record)
   self.assertIn('Strict output contract',record['attempts'][0]['invalid'])
   self.assertIn('Forbidden assessment speech',record['attempts'][0]['result']['response']['message']['content'])
 def test_strict_stub_fixture_and_replay(self):
  c=case();b=Stub(c.get('stub',{}),strict_output=True)
  with tempfile.TemporaryDirectory() as d:
   result=run(c,d,b,config(strict_output=True))
   self.assertEqual(result['status'],'complete')
   replay=run(c,d,b,config(strict_output=True),replay=True)
   self.assertEqual(replay['conclusions'],result['conclusions'])
 def test_reasoning_text_never_enters_player_context(self):
  class Reasoning(Stub):
   def complete(self,*a,**kw):
    r=super().complete(*a,**kw);r['response']['message']['thinking']='MODEL_REASONING_CANARY';return r
  c=case();b=Reasoning(c.get('stub',{}),strict_output=True)
  with tempfile.TemporaryDirectory() as d:
   result=run(c,d,b,config(strict_output=True,thinking=True))
   self.assertEqual(result['status'],'complete')
   self.assertNotIn('MODEL_REASONING_CANARY',Path(d,'events.json').read_text())
   for p in Path(d,'turns').glob('*.json'):
    r=json.loads(p.read_text());self.assertNotIn('MODEL_REASONING_CANARY',json.dumps(r['request']))
    self.assertIn('MODEL_REASONING_CANARY',json.dumps(r['attempts']))
 def test_default_payload_matches_historical_request(self):
  expected=json.loads((Path(__file__).parent/'fixtures/legacy-final-request.json').read_text())
  options=expected['options']
  backend=Ollama(expected['model'],context=options['num_ctx'],tokens=options['num_predict'],seed=options['seed'])
  self.assertEqual(backend.payload(expected['messages']),expected)
 def test_thinking_configuration_cannot_silently_change_on_resume(self):
  c=case();b=Stub({},strict_output=True)
  with tempfile.TemporaryDirectory() as d:
   run(c,d,b,config(strict_output=True,thinking=True))
   with self.assertRaises(ValueError):run(c,d,b,config(strict_output=True))
 def test_benchmark_records_contract_failures_without_retry(self):
  from dojo.benchmark import collect
  class Broken(Ollama):
   calls=0
   def complete(self,*a,**kw):
    self.calls+=1
    out=action('Forbidden speech')
    return {'response':{'message':{'content':json.dumps(out)},'done_reason':'length'},'wall_seconds':0}
  row={'id':'probe','brief':'You are Cal.','events':[],'question':'Answer'}
  backend=Broken(context=8192,strict_output=True)
  with tempfile.TemporaryDirectory() as d:
   summary=collect([row],d,backend,profiles=['grounded-v2'])
   self.assertEqual(summary,{'responses':1,'contract_failures':1})
   record=json.loads(Path(d,'probe-grounded-v2.json').read_text())
   self.assertIn('generation truncated',record['contract_violations'])
   self.assertIn('private assessment contains public speech/action',record['contract_violations'])
   self.assertEqual(collect([row],d,backend,profiles=['grounded-v2']),summary)
   self.assertEqual(backend.calls,1)

class Publication(unittest.TestCase):
 def test_omission_preserves_raw_action_and_does_not_mutate_original(self):
  from dojo.export import omit_reasoning
  raw={'attempts':[{'result':{'response':{'message':{'content':'ACTION EXACT','thinking':'LOCAL MODEL REASONING'}}}}]}
  output=omit_reasoning(raw)
  message=output['attempts'][0]['result']['response']['message']
  self.assertEqual(message['content'],'ACTION EXACT');self.assertNotIn('thinking',message)
  self.assertEqual(message['omitted_thinking']['characters'],21)
  self.assertEqual(raw['attempts'][0]['result']['response']['message']['thinking'],'LOCAL MODEL REASONING')
 def test_export_refuses_nested_destination_or_overwrite(self):
  from dojo.export import export
  with tempfile.TemporaryDirectory() as d:
   source=Path(d,'source');source.mkdir()
   with self.assertRaises(ValueError):export(source,source/'nested')
   destination=Path(d,'public');destination.mkdir()
   with self.assertRaises(ValueError):export(source,destination)
