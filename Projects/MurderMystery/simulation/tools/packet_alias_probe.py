"""Robustness control: anonymize identities and shuffle unchanged packet evidence."""
import copy,hashlib,json,random,time
from pathlib import Path
from dojo.models import Ollama
from dojo.runner import dump

def anonymize(original,seed=41):
 p=copy.deepcopy(original);v=json.loads(p['messages'][-1]['content']);rng=random.Random(seed)
 names=sorted(v['candidates']);aliases=[f'Guest {letter}' for letter in 'ABCDEFGH'];rng.shuffle(aliases);mapping=dict(zip(names,aliases))
 v['self']=mapping[v['self']];v['candidates']=[mapping[n] for n in v['candidates']];rng.shuffle(v['candidates'])
 for f in v['facts']:f['subject']=mapping[f['subject']]
 markers=sorted({f['source'] for f in v['facts']} | {c['source_atom'] for c in v['clues']} | {c['id'] for c in v['clues']})
 labels=[f'R{i:03d}' for i in range(len(markers))];rng.shuffle(labels);marker_map=dict(zip(markers,labels))
 for f in v['facts']:f['source']=marker_map[f['source']]
 for c in v['clues']:
  c['source_atom']=marker_map[c['source_atom']];c['id']=marker_map[c['id']]
 rng.shuffle(v['facts']);rng.shuffle(v['clues']);p['messages'][-1]['content']=json.dumps(v);p['format']['properties']['suspect']['enum']=v['candidates']
 # Invert labels to check conservation of every supplied fact and clue.
 inv={a:n for n,a in mapping.items()};before=json.loads(original['messages'][-1]['content']);restored=copy.deepcopy(v)
 restored['self']=inv[restored['self']];restored['candidates']=[inv[n] for n in restored['candidates']]
 marker_inverse={a:n for n,a in marker_map.items()}
 for f in restored['facts']:
  f['subject']=inv[f['subject']];f['source']=marker_inverse[f['source']]
 for c in restored['clues']:
  c['source_atom']=marker_inverse[c['source_atom']];c['id']=marker_inverse[c['id']]
 for key in ['candidates','facts','clues']:
  assert sorted(json.dumps(x,sort_keys=True) for x in before[key])==sorted(json.dumps(x,sort_keys=True) for x in restored[key])
 assert before['self']==restored['self'];assert before['own_private_knowledge']==restored['own_private_knowledge']
 return p,mapping

def main():
 root=Path('local-private/movie');out=root/'packet-alias';out.mkdir(mode=0o700);rows=[];start=time.monotonic()
 dump(out/'plan.json',{'method':'Three preselected packet-assessment contexts p2,p4,p8. Replace character names by shuffled Guest labels, anonymize source/clue identifiers, shuffle fact/clue/candidate order; assertions unchanged under inverse mapping. Same Gemma settings, no answer in request. This is a combined label/order robustness control.','max_calls':3,'max_seconds':540,'per_call_seconds':180,'alias_seed':41})
 for who in ['p2','p4','p8']:
  source=root/'packet-assessment'/f'{who}.json';original=json.loads(source.read_text())['request'];p,mapping=anonymize(original);d={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'alias_mapping':mapping,'request':p};path=out/f'{who}.json';dump(path,d);remaining=540-(time.monotonic()-start)
  if remaining<=0:raise RuntimeError('Budget exhausted')
  try:
   d['result']=Ollama().complete(p,timeout=min(180,remaining));raw=d['result']['response'];a=json.loads(raw['message']['content']);d['valid']=set(a)=={'suspect'} and a['suspect'] in mapping.values() and raw.get('done_reason')!='length'
  except Exception as e:d['error']=str(e);d['valid']=False;a={}
  dump(path,d);path.chmod(0o600);inverse={a:n for n,a in mapping.items()};row={'player':who,'suspect_alias':a.get('suspect'),'decoded_suspect':inverse.get(a.get('suspect')),'valid':d['valid'],'seconds':d.get('result',{}).get('wall_seconds'),'error':d.get('error')};rows.append(row);dump(out/'summary.json',rows);print(json.dumps(row),flush=True)
if __name__=='__main__':main()
