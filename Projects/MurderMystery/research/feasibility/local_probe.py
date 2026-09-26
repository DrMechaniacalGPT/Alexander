"""Three bounded local Ollama calls; synthetic marker only, no game simulation."""
import json
import time
import urllib.request
from pathlib import Path

ENDPOINT = 'http://127.0.0.1:11434/api/chat'
MODEL = 'qwen3:8b'

def main():
    cases = [
        ('A_private', [{'role':'user','content':'This is a context-routing smoke test. Your private test marker is APRICOT-7319. Reply with exactly that marker and nothing else.'}], 'APRICOT-7319'),
        ('B_before_delivery', [{'role':'user','content':'This is a context-routing smoke test. No private marker has been supplied to you. What is player A\'s private test marker? Reply exactly UNKNOWN if it is not in this conversation. Do not guess.'}], 'UNKNOWN'),
        ('B_after_delivery', [{'role':'user','content':'This is a context-routing smoke test. A delivered this message to you: "My private test marker is APRICOT-7319." What marker did A tell you? Reply with exactly the marker and nothing else.'}], 'APRICOT-7319'),
    ]
    records=[]
    for i,(name,messages,expected) in enumerate(cases):
        payload={'model':MODEL,'messages':messages,'stream':False,'think':False,
                 'keep_alive':'0' if i==len(cases)-1 else '2m',
                 'options':{'temperature':0,'num_predict':64,'num_ctx':2048}}
        request=urllib.request.Request(ENDPOINT,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
        start=time.monotonic()
        with urllib.request.urlopen(request,timeout=120) as response:
            result=json.load(response)
        output=result.get('message',{}).get('content','').strip()
        record={'case':name,'request':payload,'output':output,'expected':expected,'passed':output==expected,
                'wall_seconds':round(time.monotonic()-start,3),
                'model':result.get('model'),'created_at':result.get('created_at'),
                'done_reason':result.get('done_reason'),
                'usage':{k:result.get(k) for k in ['prompt_eval_count','eval_count','load_duration','prompt_eval_duration','eval_duration','total_duration']}}
        records.append(record)
        print(json.dumps({k:record[k] for k in ['case','output','passed','wall_seconds','usage']}),flush=True)
        Path(__file__).with_name('local_probe_results.json').write_text(json.dumps(records,indent=2)+'\n')
    if not all(r['passed'] for r in records):
        raise SystemExit('One or more marker checks failed; inspect outputs.')

if __name__=='__main__':
    main()
