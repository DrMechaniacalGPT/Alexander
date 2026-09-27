"""Reproducible bounded sharing sweep; inputs may be private, output is aggregate."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from dojo.symbolic import simulate

def study(case,seeds=100):
    rows=[];scored=[p for p in case['players'] if p!=case.get('truth',{}).get('culprit')]
    for partners in (2,4,7):
      for packets in (2,4):
       for rounds in (0,2):
        correct=unique=remaining=known=decisions=0
        for seed in range(1,seeds+1):
          r=simulate(case,partners=partners,seed=seed,packets_per_encounter=packets,group_rounds=rounds,group_packets=packets)
          for p in scored:
            d=r['decisions'][p];decisions+=1;correct+=r['evaluation']['correct'][p];unique+=len(d['remaining'])==1;remaining+=len(d['remaining']);known+=sum(x.startswith('fact:') for x in r['known_packets'][p])
        rows.append({'partners':partners,'packets_per_exchange':packets,'group_rounds':rounds,'seeds':seeds,'nonculprit_decisions':decisions,'correct_votes':correct,'unique_remaining':unique,'mean_remaining':round(remaining/decisions,3),'mean_known_fact_packets':round(known/decisions,3)})
    return {'case':case['id'],'semantic_case_sha256':hashlib.sha256(json.dumps(case,sort_keys=True).encode()).hexdigest(),'engine_sha256':hashlib.sha256((Path(__file__).resolve().parents[1]/'dojo/symbolic.py').read_bytes()).hexdigest(),'study_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seed_range':[1,seeds],'relay':False,'novelty_selection':'optimistic scheduler knows recipient ledger; not modeled human awareness','rows':rows}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('case',type=Path);p.add_argument('--seeds',type=int,default=100);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 if not 1<=a.seeds<=1000:p.error('seeds must be 1..1000')
 if a.out.exists():p.error('output already exists')
 result=study(json.loads(a.case.read_text()),a.seeds);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
