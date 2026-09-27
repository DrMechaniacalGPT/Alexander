"""Audit recorded output contracts. This deliberately does not grade reasoning."""
import argparse
import json
from pathlib import Path

def violations(request, result):
    errors=[]
    raw=result.get('response',{})
    if raw.get('done_reason')=='length' or raw.get('truncated'): errors.append('generation truncated')
    try: action=json.loads(raw['message']['content'])
    except (KeyError,TypeError,ValueError): return errors+['invalid JSON response']
    if 'format' not in request: return errors+['request lacks an output schema; cannot audit this backend']
    schema=request['format']; fields=schema['properties']
    if not isinstance(action,dict) or set(action)!=set(schema['required']): return errors+['wrong fields']
    for name,rule in fields.items():
        value=action[name]
        if rule['type']=='string':
            if not isinstance(value,str): errors.append(name+': not a string');continue
            if len(value)<rule.get('minLength',0): errors.append(name+': minimum length')
            if len(value)>rule.get('maxLength',float('inf')): errors.append(name+': length limit')
            if 'enum' in rule and value not in rule['enum']: errors.append(name+': unavailable value')
        elif rule['type']=='array':
            if not isinstance(value,list): errors.append(name+': not an array');continue
            if len(value)<rule.get('minLength',0): errors.append(name+': minimum length')
            if len(value)>rule.get('maxItems',float('inf')): errors.append(name+': item limit')
            if any(not isinstance(v,str) for v in value): errors.append(name+': non-string item')
            if 'enum' in rule['items'] and any(v not in rule['items']['enum'] for v in value): errors.append(name+': unseen citation')
    view=json.loads(request['messages'][-1]['content'])
    if view['final_assessment']:
        if action['say']!='' or action['action']!='none': errors.append('private assessment contains public speech/action')
        if not isinstance(action['conclusion'],str) or not action['conclusion'].strip(): errors.append('empty assessment')
    elif action['conclusion']!='': errors.append('conclusion outside assessment')
    return errors

def audit(root):
    rows=[]
    for path in sorted(Path(root).rglob('*.json')):
        record=json.loads(path.read_text())
        if not isinstance(record,dict) or 'request' not in record: continue
        attempts=record.get('attempts',[record])
        for index,attempt in enumerate(attempts):
            result=attempt.get('result')
            rows.append({'record':str(path.relative_to(root)),'attempt':index,
                         'model':record['request'].get('model'),
                         'wall_seconds':result.get('wall_seconds',0) if result else 0,
                         'violations':violations(record['request'],result) if result else ['no result']})
    return {'generation_attempts':len(rows),'wall_seconds':round(sum(r['wall_seconds'] for r in rows),3),
            'contract_failures':sum(bool(r['violations']) for r in rows),'records':rows,
            'limitation':'Syntactic citation availability is not evidential support. Semantic judgments require separate review.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    report=audit(a.root);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2))
if __name__=='__main__': main()
