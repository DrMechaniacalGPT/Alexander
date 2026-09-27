"""Build a private text adaptation from locally extracted, source-owned data.

Does not contain or download role/clue text. Do not publish its output under MIT.
The input schema is documented in README.md; extraction must be checked against
original pages. This adapter implements selected mechanics, not physical realism.
"""
import argparse
import json
import random
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def adapt(source, seed=17, partners=None):
    roles = source['roles']
    if len(roles) != 8 or len({r['id'] for r in roles}) != 8:
        raise ValueError('This bounded adaptation requires eight distinct guest cards')
    ids = [r['id'] for r in roles]
    culprit = source['culprit_id']
    if culprit not in ids: raise ValueError('Selected cast omits culprit')
    clues = source['clues']
    if len(clues) != 16 or len({c['id'] for c in clues}) != 16 or any(c['copies'] != 3 for c in clues):
        raise ValueError('Expected printed inventory: sixteen clue types, three copies each')
    # Model 48 hidden card locations, sample 24 without replacement, three per guest.
    # Fixed equal search allocation is an explicit idealization, not observed behavior.
    copies = [{'copy': f"{c['id']}-{n}", 'text': c['text']} for c in clues for n in range(c['copies'])]
    random.Random(seed).shuffle(copies)
    assignment = {p: copies[i*3:i*3+3] for i,p in enumerate(ids)}
    case = {'id':'movie-printed-packet-adaptation',
        'provenance': {'source': source['source'], 'private': True,
          'interpretation':'16 printed clue types ×3, not the 18-item reference inventory',
          'assumptions':['Eight selected guests and engine Director',
            'Two finite random-pair windows, two utterances each per encounter',
            'Three privately discovered card copies per guest sampled without replacement',
            'No extra post-hunt discussion', 'Simultaneous private accusations before generated confession',
            'Physical acting, food, real time and optional awards not simulated'],
          'hunt_seed':seed, 'hunt_assignment':assignment},
        'public':source['public_rules'],
        'truth':{'culprit':culprit},
        'players':{r['id']:{'name':r['name'],'brief':r['brief']} for r in roles},
        'scenes':[
          {'id':'mingling','mode':'random_pairs','windows':2,'turns_each':2,
           'instruction':'The Director is elsewhere. Converse with your partner about the film and your character facts, motives and interests. React to what they actually say.'},
          {'id':'host-signal','deliveries':[{'recipients':ids,'content':source['host_signal']}],
           'encounters':[{'participants':ids,'speakers':[culprit],'turns_each':1,
               'instruction':'The Director is in the room. Respond to the visible signal according to your role. Use action serve_food_or_drink if you do so; otherwise none.',
               'legal_actions':['none','serve_food_or_drink']}],
           'requires_action':{'player':culprit,'action':'serve_food_or_drink'}},
          {'id':'death-and-hunt','absent':[],
           'deliveries':[{'recipients':ids,'content':'The Director falls dead. '+source['death_notice']}]+
              [{'recipients':[p],'content':'You discover this printed clue card: '+c['text']} for p in ids for c in assignment[p]],
           # Deliveries only: empty fixed encounters is explicitly allowed for this phase.
           'mode':'delivery_only'}],
        'question':'Privately name the ONE guest you accuse of murdering the Director, or explicitly say insufficient evidence. Explain briefly using your own observations and discovered cards. Other accusations are not yet available.',
        'epilogue':[{'participants':ids,'speakers':[culprit],
                    'instruction':'Accusations are locked. It is now the scheduled confession. Follow your role and confess in your own words. This speech is your generated performance, not text from the author. Use action confess.',
                    'legal_actions':['none','confess'],'required_action':'confess'}]}
    if partners is not None:
        from dojo.schedule import distinct_encounters
        scene = case['scenes'][0]
        scene['encounters'] = distinct_encounters(ids, partners, seed, scene['turns_each'], scene['instruction'])
        scene['mode'] = 'fixed'
        scene.pop('windows')
        case['provenance']['assumptions'][1] = f'{partners} distinct partners each; two utterances per player per encounter'
    return case


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source_json',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--seed',type=int,default=17)
    p.add_argument('--partners',type=int,help='Experimental distinct-partner mingling schedule')
    a=p.parse_args()
    result=adapt(json.loads(a.source_json.read_text()),a.seed,a.partners)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n');a.output.chmod(0o600)
    print('Wrote private adaptation:',a.output)
if __name__=='__main__':main()
