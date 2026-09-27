import copy,json,tempfile,unittest
from dojo.core import State,messages_for
from dojo.models import Ollama,Stub
from dojo.audit import violations
from dojo.runner import run
from test_dojo import case,config,action

class Dialogue(unittest.TestCase):
 def test_role_history_and_private_boundaries(self):
  s=State(case());s.emit('hidden','p1',['p1'],'HIDDEN EVENT','s1')
  s.apply('own','p2',['p1','p2'],action('OWN LINE'),'s1')
  s.emit('reply','p1',['p1','p2'],'OTHER LINE','s1')
  s.emit('host','host',['p2'],'HOST CLUE','s1','delivery')
  s.emit('gesture','p2',['p1','p2'],'SYMBOL','s1','action')
  before=copy.deepcopy(s.events)
  m=messages_for(s,'p2',['p2','p3'],'s2','Reply',prompt_profile='dialogue-v1')
  self.assertEqual([x['role'] for x in m],['system','user','assistant','user','user','user','user'])
  text=json.dumps(m)
  for forbidden in ['HIDDEN EVENT','SECRET INTENTION','VIOLET-5831','cabinet 4']: self.assertNotIn(forbidden,text)
  self.assertEqual(text.count('OWN LINE'),1);self.assertEqual(text.count('OTHER LINE'),1)
  self.assertEqual(s.events,before)
  self.assertEqual(json.loads(m[-1]['content'])['audience_names'],{'p2':'Bea','p3':'Cal'})
 def test_private_notes_and_conclusions_do_not_become_history(self):
  s=State(case());s.apply('lie','p2',['p2','p3'],action('I never met Ari.'),'s1')
  s.conclusions['p2']='PRIVATE CONCLUSION'
  m=messages_for(s,'p2',['p2','p3'],'s2','Reply',prompt_profile='dialogue-v1')
  rendered=json.dumps(m)
  self.assertNotIn('SECRET INTENTION',rendered);self.assertNotIn('PRIVATE CONCLUSION',rendered)
  self.assertIn('I never met Ari.',m[2]['content']);self.assertEqual(m[2]['role'],'assistant')
  self.assertNotIn('I never met Ari.',m[1]['content'])
 def test_schema_phase_and_available_citations(self):
  s=State(case());e=s.emit('host','host',['p2'],'CLUE','s1','delivery')
  m=messages_for(s,'p2',['p2'],'assessment','Answer',True,prompt_profile='dialogue-v1')
  p=Ollama(context=16384,strict_output=True).payload(m)
  self.assertEqual(p['format']['properties']['evidence']['items']['enum'],[e['id']])
  a=action();a['say']='';a['evidence']=[e['id']]
  self.assertEqual(violations(p,{'response':{'message':{'content':json.dumps(a)}}}),[])
 def test_bounded_memory_applies_before_rendering(self):
  c=case();c['players']['p2']['policy']={'memory_events':1};s=State(c)
  s.emit('old','p1',['p2'],'FORGOTTEN','s1');s.emit('new','p1',['p2'],'REMEMBERED','s1')
  m=messages_for(s,'p2',['p2','p3'],'s2','Speak',prompt_profile='dialogue-v1')
  self.assertNotIn('FORGOTTEN',json.dumps(m));self.assertIn('REMEMBERED',json.dumps(m))
 def test_run_and_replay(self):
  b=Stub({p:action() for p in case()['players']},strict_output=True)
  with tempfile.TemporaryDirectory() as d:
   cfg=config(prompt_profile='dialogue-v1',strict_output=True)
   self.assertEqual(run(case(),d,b,cfg)['status'],'complete')
   self.assertEqual(run(case(),d,b,cfg,replay=True)['status'],'complete')


class Schedule(unittest.TestCase):
 def test_four_distinct_partners_each(self):
  from dojo.schedule import distinct_encounters
  players=[f'p{i}' for i in range(8)]
  encounters=distinct_encounters(players,4,17)
  pairs=[frozenset(e['participants']) for e in encounters]
  self.assertEqual(len(pairs),16);self.assertEqual(len(set(pairs)),16)
  for p in players:
   self.assertEqual(sum(p in pair for pair in pairs),4)
  for window in range(4):
   self.assertEqual(sorted(p for e in encounters if e['window']==window for p in e['participants']),players)
  self.assertEqual(encounters,distinct_encounters(players,4,17))
 def test_invalid_schedules_fail(self):
  from dojo.schedule import distinct_encounters
  for players,partners in [(['a','b','c'],1),(['a','a'],1),(['a','b'],2),(['a','b'],0)]:
   with self.assertRaises(ValueError): distinct_encounters(players,partners)

 def test_adapter_preserves_clues_when_changing_schedule(self):
  from tools.import_movie import adapt
  source={'roles':[{'id':f'p{i}','name':f'Guest {i}','brief':'Original test brief.'} for i in range(8)],
          'culprit_id':'p0','clues':[{'id':f'c{i}','text':f'Original clue {i}','copies':3} for i in range(16)],
          'source':{},'public_rules':'Original test party.','host_signal':'A signal','death_notice':'Search now'}
  old=adapt(source);new=adapt(source,partners=4)
  self.assertEqual(old['players'],new['players'])
  self.assertEqual(old['scenes'][1:],new['scenes'][1:])
  self.assertEqual(old['provenance']['hunt_assignment'],new['provenance']['hunt_assignment'])
  self.assertEqual(len(new['scenes'][0]['encounters']),16)
  self.assertEqual(old['scenes'][0]['mode'],'random_pairs')

class Metrics(unittest.TestCase):
 def test_repetition_is_speaker_specific_and_not_truth_score(self):
  from dojo.metrics import conversation_metrics
  def e(actor,text,kind='speech',scene='mingling'):
   return {'actor':actor,'content':text,'recipients':['a','b'],'kind':kind,'scene':scene}
  r=conversation_metrics([e('a','hello'),e('b','hello'),e('a','hello'),e('a','hello','action'),e('a','hello',scene='assessment')])
  self.assertEqual(r['speech_turns'],3);self.assertEqual(r['exact_repeated_turns'],1)
  self.assertEqual(r['by_player']['a']['other_speech_received'],1)
  self.assertEqual(r['by_player']['b']['other_speech_received'],2)
