"""Compare match counts with distinct-source counts on identical seeded traces."""
import argparse,hashlib,json,random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from dojo.symbolic import simulate

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('case',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 if a.out.exists():p.error('Output exists')
 c=json.loads(a.case.read_text());rows=[]
 for seed in range(1,101):
  r=simulate(c,partners=7,seed=seed,packets_per_encounter=4,group_rounds=2,group_packets=4)
  for i,who in enumerate(c['players']):
   if who==c['truth']['culprit']:continue
   d=r['decisions'][who];pool=d['remaining'] or [p for p in c['players'] if p not in c.get('private_exclusions',{}).get(who,[])];top=max(d['candidates'][p]['unique_source_match_count'] for p in pool);ties=sorted(p for p in pool if d['candidates'][p]['unique_source_match_count']==top);choice=random.Random(seed+i).choice(ties)
   rows.append({'clue_weight_correct':d['guess']==c['truth']['culprit'],'source_weight_correct':choice==c['truth']['culprit'],'changed':choice!=d['guess']})
 out={'case_sha256':hashlib.sha256(a.case.read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256((Path(__file__).resolve().parents[1]/'dojo/symbolic.py').read_bytes()).hexdigest(),'seed_range':[1,100],'partners':7,'packets':4,'group_rounds':2,'group_packets':4,'decisions':len(rows),'correct_by_clue_matches':sum(x['clue_weight_correct'] for x in rows),'correct_by_distinct_sources':sum(x['source_weight_correct'] for x in rows),'changed_votes':sum(x['changed'] for x in rows),'method':'Same traces and elimination, rerank by distinct matching fact-source atoms; same tie seed. This is a weighting sensitivity, not calibrated probability.'}
 a.out.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
