import copy,json,unittest
from tools.required_guess import require_guess
from tools.choice_only_probe import choice_request

class RequiredChoice(unittest.TestCase):
 def request(self):
  return {'model':'local','think':True,'options':{'seed':17},'messages':[{'role':'system','content':'Card and instructions.'},{'role':'user','content':'Earlier witnessed speech.'},{'role':'user','content':json.dumps({'self':'p2','final_assessment':True,'observations':[{'id':'e1'}],'instruction':'Choose or abstain.'})}], 'format':{'properties':{'conclusion':{'type':'string'}},'required':['conclusion']}}
 def test_evidence_and_settings_unchanged_in_both_variants(self):
  p=self.request();before=copy.deepcopy(p)
  for build in (require_guess,choice_request):
   q=build(p,['Alice','Bob']);self.assertEqual(q['messages'][:-1],p['messages'][:-1]);self.assertEqual(q['options'],p['options']);self.assertEqual(q['model'],p['model']);self.assertEqual(q['think'],p['think'])
   a=json.loads(p['messages'][-1]['content']);b=json.loads(q['messages'][-1]['content'])
   for key in a:
    if key!='instruction':self.assertEqual(a[key],b[key])
   self.assertEqual(q['format']['properties']['suspect']['enum'],['Alice','Bob'])
  self.assertEqual(p,before)
 def test_vote_has_only_one_decision_field(self):
  q=choice_request(self.request(),['Alice','Bob']);self.assertEqual(q['format']['required'],['suspect']);self.assertEqual(set(q['format']['properties']),{'suspect'})
 def test_nonassessment_rejected(self):
  p=self.request();p['messages'][-1]['content']='{"final_assessment":false}'
  for build in (require_guess,choice_request):
   with self.assertRaises(ValueError):build(p,['Alice','Bob'])

 def test_alias_control_preserves_evidence_and_original_input(self):
  from tools.packet_alias_probe import anonymize
  names=list('ABCDEFGH')
  view={'self':'A','candidates':names,'own_private_knowledge':'innocent','facts':[{'subject':'B','predicate':'x','value':True,'source':'original-source'}],'clues':[{'id':'original-clue','predicate':'x','expected':True,'strength':'hard','source_atom':'printed-source'}]}
  p={'messages':[{'role':'user','content':json.dumps(view)}],'format':{'properties':{'suspect':{'enum':names}}}};before=copy.deepcopy(p)
  result,mapping=anonymize(p);new=json.loads(result['messages'][-1]['content'])
  self.assertEqual(p,before);self.assertEqual(new['self'],mapping['A']);self.assertEqual(new['facts'][0]['subject'],mapping['B']);self.assertTrue(new['facts'][0]['value'])
  self.assertNotEqual(new['facts'][0]['source'],'original-source');self.assertEqual(set(new['candidates']),set(mapping.values()));self.assertEqual(new['candidates'],result['format']['properties']['suspect']['enum'])
