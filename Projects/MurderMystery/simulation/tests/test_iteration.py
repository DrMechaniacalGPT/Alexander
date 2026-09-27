import json,unittest
from dojo.core import State,messages_for
from dojo.models import Ollama
from test_dojo import case

class AssessmentBudget(unittest.TestCase):
 def test_only_assessment_uses_reasoning_and_larger_budget(self):
  s=State(case());b=Ollama(context=32768,tokens=768,assessment_tokens=8192,assessment_thinking=True,model='gemma',assessment_model='qwen')
  chat=b.payload(messages_for(s,'p2',['p1','p2'],'s1','Talk',prompt_profile='dialogue-v1'))
  final=b.payload(messages_for(s,'p2',['p2'],'assessment','Answer',True,prompt_profile='dialogue-v1'))
  self.assertFalse(chat['think']);self.assertEqual(chat['options']['num_predict'],768)
  self.assertTrue(final['think']);self.assertEqual(final['options']['num_predict'],8192)
  self.assertEqual(chat['model'],'gemma');self.assertEqual(final['model'],'qwen')
 def test_budget_guard_uses_effective_assessment_tokens(self):
  s=State(case());m=messages_for(s,'p2',['p2'],'assessment','Answer',True)
  with self.assertRaises(ValueError):Ollama(context=8192,tokens=128,assessment_tokens=8192).payload(m)
 def test_missing_override_preserves_global_thinking(self):
  s=State(case());m=messages_for(s,'p2',['p2'],'assessment','Answer',True)
  self.assertTrue(Ollama(context=8192,thinking=True).payload(m)['think'])
 def test_museum_truth_not_in_player_view(self):
  from pathlib import Path
  c=json.loads(Path('fixtures/05_museum_party.json').read_text());s=State(c)
  m=messages_for(s,'p1',['p1'],'assessment','Answer',True,prompt_profile='dialogue-v1')
  self.assertNotIn('secretly committed',json.dumps(m));self.assertNotIn('"culprit"',json.dumps(m))


class OpenPartySetup(unittest.TestCase):
 def test_expanded_party_runs_all_phases_without_inference(self):
  from tools.import_movie import adapt
  from dojo.models import Stub
  from dojo.runner import run
  import tempfile
  source={'roles':[{'id':f'p{i}','name':f'Guest {i}','brief':'Original test brief.'} for i in range(8)],
          'culprit_id':'p0','clues':[{'id':f'c{i}','text':f'Original clue {i}','copies':3} for i in range(16)],
          'source':{},'public_rules':'Original test party.','host_signal':'A signal','death_notice':'Search now'}
  old=adapt(source);new=adapt(source,partners=7,discussion_rounds=2,guided_mingling=True)
  self.assertNotIn('No extra post-hunt discussion',new['provenance']['assumptions'])
  longer=adapt(source,turns_each=4)
  self.assertIn('4 utterances',longer['provenance']['assumptions'][1])
  self.assertEqual(old['players'],new['players']);self.assertEqual(old['provenance']['hunt_assignment'],new['provenance']['hunt_assignment'])
  class PhaseStub(Stub):
   def complete(self,payload,timeout=120):
    v=json.loads(payload['messages'][-1]['content']);a={'say':'' if v['final_assessment'] else 'Hello.','private_note':'','conclusion':'Unknown.' if v['final_assessment'] else '', 'action':v['legal_actions'][-1],'evidence':[]}
    return {'response':{'message':{'content':json.dumps(a)},'done_reason':'stop'},'wall_seconds':0}
  with tempfile.TemporaryDirectory() as d:
   result=run(new,d,PhaseStub({},strict_output=True),{'backend':'stub','seed':17,'max_calls':140,'max_seconds':60,'prompt_profile':'dialogue-v1','strict_output':True})
   self.assertEqual(result['status'],'complete');self.assertEqual(result['usage']['requests'],138)
   self.assertEqual(len(result['conclusions']),8)

class ScenarioFork(unittest.TestCase):
 def test_fork_reuses_only_unchanged_prefix_and_retains_lineage(self):
  import tempfile,copy
  from pathlib import Path
  from dojo.models import Stub
  from dojo.runner import run
  from test_dojo import config,action
  class Counting(Stub):
   calls=0
   def complete(self,*a,**kw):self.calls+=1;return super().complete(*a,**kw)
  c=case();b=Counting({p:action() for p in c['players']})
  with tempfile.TemporaryDirectory() as d:
   parent=Path(d)/'parent';run(c,parent,b,config());before=b.calls
   with self.assertRaises(ValueError):
    run(c,Path(d)/'too-far',b,config(),continue_from=parent,reuse_turns=999,fork_case=True)
   self.assertEqual(b.calls,before)
   changed=copy.deepcopy(c);changed['question']='A revised private question.'
   child=Path(d)/'child'
   result=run(changed,child,b,config(),continue_from=parent,reuse_turns=1,fork_case=True)
   self.assertEqual(result['status'],'complete')
   lineage=json.loads((child/'manifest.json').read_text())['continuation']
   self.assertTrue(lineage['case_fork']);self.assertIn('parent_case_sha256',lineage)
   self.assertTrue(json.loads((child/'turns/t00000.json').read_text())['inherited_from'])
   changed['public']='This changes the reused first prompt.'
   before=b.calls
   result=run(changed,Path(d)/'bad',b,config(),continue_from=parent,reuse_turns=1,fork_case=True)
   self.assertEqual(result['status'],'incomplete');self.assertIn('Recorded prompt',result['failure'])
   self.assertEqual(b.calls,before)
 def test_fork_requires_explicit_prefix(self):
  import tempfile
  from dojo.models import Stub
  from dojo.runner import run
  from test_dojo import config
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError):run(case(),d,Stub({}),config(),fork_case=True)

 def test_fork_rejects_gap_in_declared_parent_prefix(self):
  import tempfile
  from pathlib import Path
  from dojo.models import Stub
  from dojo.runner import run
  from test_dojo import config,action
  c=case()
  with tempfile.TemporaryDirectory() as d:
   parent=Path(d)/'parent';run(c,parent,Stub({p:action() for p in c['players']}),config())
   (parent/'turns/t00001.json').unlink()
   with self.assertRaises(ValueError):
    run(c,Path(d)/'child',Stub({}),config(),continue_from=parent,reuse_turns=3,fork_case=True)

 def test_fork_rejects_unused_inherited_tail(self):
  import tempfile,copy
  from pathlib import Path
  from dojo.models import Stub
  from dojo.runner import run
  from test_dojo import config,action
  c=case();ids=list(c['players']);c['epilogue']=[{'participants':ids,'speakers':[ids[0]],'instruction':'Closing remark.'}]
  class Counting(Stub):
   calls=0
   def complete(self,*a,**kw):self.calls+=1;return super().complete(*a,**kw)
  b=Counting({p:action() for p in ids})
  with tempfile.TemporaryDirectory() as d:
   parent=Path(d)/'parent';run(c,parent,b,config());n=len(list((parent/'turns').glob('*.json')));before=b.calls
   changed=copy.deepcopy(c);changed.pop('epilogue')
   result=run(changed,Path(d)/'child',b,config(),continue_from=parent,reuse_turns=n,fork_case=True)
   self.assertEqual(result['status'],'incomplete');self.assertIn('did not consume',result['failure'])
   self.assertEqual(b.calls,before)

class EffectiveModelContinuation(unittest.TestCase):
 def test_model_change_allowed_only_after_inherited_prefix(self):
  import tempfile
  from pathlib import Path
  from dojo.models import Stub
  from dojo.runner import run
  from test_dojo import config,action
  class PhaseModel(Stub):
   def __init__(self,assessment,thinking=True):super().__init__({p:action() for p in case()['players']});self.assessment=assessment;self.thinking=thinking;self.calls=0
   def payload(self,messages):
    r=super().payload(messages);v=json.loads(messages[-1]['content']);r['model']=self.assessment if v['final_assessment'] else 'gemma';r['think']=self.thinking if v['final_assessment'] else False;return r
   def complete(self,*a,**kw):self.calls+=1;return super().complete(*a,**kw)
  with tempfile.TemporaryDirectory() as d:
   parent=Path(d)/'parent';run(case(),parent,PhaseModel('gemma'),config())
   b=PhaseModel('qwen');child=Path(d)/'child'
   r=run(case(),child,b,config(),continue_from=parent,reuse_turns=1)
   self.assertEqual(r['status'],'complete')
   blocked=PhaseModel('qwen');n=len(list((parent/'turns').glob('*.json')))
   r=run(case(),Path(d)/'blocked',blocked,config(),continue_from=parent,reuse_turns=n)
   self.assertEqual(r['status'],'incomplete');self.assertIn('different effective model',r['failure']);self.assertEqual(blocked.calls,0)

   fast=PhaseModel('gemma',False)
   r=run(case(),Path(d)/'fast',fast,config(),continue_from=parent,reuse_turns=1)
   self.assertEqual(r['status'],'complete')
   blocked=PhaseModel('gemma',False)
   r=run(case(),Path(d)/'blocked-thinking',blocked,config(),continue_from=parent,reuse_turns=n)
   self.assertEqual(r['status'],'incomplete');self.assertIn('different effective think',r['failure']);self.assertEqual(blocked.calls,0)
