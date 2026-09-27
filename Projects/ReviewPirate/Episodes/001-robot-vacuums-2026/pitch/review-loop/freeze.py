from pathlib import Path
import sys,json,re,hashlib
p=Path(__file__).resolve().parent.parent;r=p/'review-loop'/sys.argv[1]
s=json.loads((r/'scenes.json').read_text());h=(r/'index.html').read_text();h=re.sub(r'const S=.*?;let n=0;',lambda m:'const S='+json.dumps(s)+';let n=0;',h,flags=re.S);(r/'index.html').write_text(h)
files=[r/'index.html',r/'scenes.json']+[r/x['audio'] for x in s]+[p/'assets'/n for n in sorted({x['photo'] for x in s})]
(r/'manifest.json').write_text(json.dumps({str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},indent=2));print(sum(x['duration'] for x in s))
