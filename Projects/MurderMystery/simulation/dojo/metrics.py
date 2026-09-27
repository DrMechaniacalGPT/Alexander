"""Mechanical conversation diagnostics; no automatic truth or enjoyment score."""
import argparse
import json
from pathlib import Path


def conversation_metrics(events, scene='mingling'):
    speakers={};heard={};contacts={}
    for event in events:
        if event['scene']!=scene or event['kind']!='speech': continue
        actor=event['actor'];text=event['content']
        row=speakers.setdefault(actor,{'turns':0,'exact_repeated_turns':0,'words':0,'seen':set()})
        row['turns']+=1;row['words']+=len(text.split())
        row['exact_repeated_turns']+=int(text in row['seen'])
        row['seen'].add(text)
        for recipient in event['recipients']:
            if recipient!=actor:
                heard[recipient]=heard.get(recipient,0)+1
                contacts.setdefault(recipient,set()).add(actor)
                contacts.setdefault(actor,set()).add(recipient)
    for actor,row in speakers.items():
        row['distinct_utterances']=len(row.pop('seen'))
        row['other_speech_received']=heard.get(actor,0)
        row['distinct_partners']=len(contacts.get(actor,set()))
    return {'scene':scene,'speech_turns':sum(r['turns'] for r in speakers.values()),
            'exact_repeated_turns':sum(r['exact_repeated_turns'] for r in speakers.values()),
            'by_player':speakers,
            'limitation':'Exact same-speaker string repetition only. A unique line can still be false, repetitive in meaning, irrelevant, or addressed to the wrong person. Contacts are opportunities, not proof of exchanged facts.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('events',type=Path)
    p.add_argument('--scene',default='mingling');p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    result=conversation_metrics(json.loads(a.events.read_text()),a.scene)
    if a.out.exists():raise ValueError('Use a new report path')
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
