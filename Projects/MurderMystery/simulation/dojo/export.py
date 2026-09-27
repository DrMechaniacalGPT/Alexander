"""Export original synthetic evidence with model reasoning text omitted.

Prompts, action responses and private_note remain. This is not a private-data
sanitizer and must not be used to publish source-owned external game packets.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path


def omit_reasoning(record):
    """Preserve action responses exactly; mark omitted model reasoning by hash."""
    result=copy.deepcopy(record)
    if isinstance(result,list): return [omit_reasoning(item) for item in result]
    if not isinstance(result,dict): return result
    entries=result.get('attempts',[result])
    for entry in entries:
        message=entry.get('result',{}).get('response',{}).get('message',{})
        reasoning=message.pop('thinking',None)
        if reasoning is not None:
            message['omitted_thinking']={'characters':len(reasoning),
                'sha256':hashlib.sha256(reasoning.encode()).hexdigest()}
    return result


def export(source, destination):
    source,destination=Path(source).resolve(),Path(destination).resolve()
    if destination==source or source in destination.parents or destination in source.parents:
        raise ValueError('Export must be a separate sibling tree')
    if destination.exists(): raise ValueError('Use a new export directory')
    # Player inspection files duplicate private information and are not exported.
    files=[p for p in source.rglob('*') if p.is_file() and p.suffix in ('.json','.md') and 'players' not in p.relative_to(source).parts and p.name!='.run.lock']
    manifest=[]
    destination.mkdir(parents=True)
    for path in sorted(files):
        raw=path.read_bytes();relative=path.relative_to(source)
        if path.suffix=='.json':
            value=omit_reasoning(json.loads(raw))
            public=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
        else: public=raw
        target=destination/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(public)
        manifest.append({'path':str(relative),'local_original_sha256':hashlib.sha256(raw).hexdigest(),
                         'published_sha256':hashlib.sha256(public).hexdigest()})
    (destination/'export-manifest.json').write_text(json.dumps({'omission':'Only model-returned thinking text is omitted; prompts and structured action fields remain.', 'files':manifest},indent=2)+'\n')
    return len(manifest)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('destination',type=Path);a=p.parse_args()
    print(export(a.source,a.destination),'files exported')
