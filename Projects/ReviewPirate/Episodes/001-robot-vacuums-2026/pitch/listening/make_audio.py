from pathlib import Path
import os,json,numpy as np,soundfile as sf,onnxruntime as rt
from kokoro_onnx import Kokoro
root=Path(__file__).parent
opts=rt.SessionOptions();opts.intra_op_num_threads=4;opts.inter_op_num_threads=1
session=rt.InferenceSession(str(Path(os.environ['KOKORO_MODEL_DIR'])/'kokoro-v1.0.onnx'),sess_options=opts,providers=['CPUExecutionProvider'])
voice=Kokoro.from_session(session,str(Path(os.environ['KOKORO_MODEL_DIR'])/'voices-v1.0.bin'))
scenes=json.loads((root/'scenes.json').read_text());(root/'audio').mkdir(exist_ok=True)
for s in scenes:
 samples,sr=voice.create(s['spoken'],voice='af_heart',speed=.98,lang='en-us')
 samples=np.concatenate([np.zeros(int(.1*sr)),samples,np.zeros(int(.22*sr))])
 peak=float(np.max(np.abs(samples)))
 if peak>.95:samples*=.95/peak
 sf.write(root/s['audio'],samples,sr,subtype='PCM_16')
 s.update(duration=round(len(samples)/sr,2),voice='Kokoro af_heart',sample_rate=sr,peak=float(np.max(np.abs(samples))))
 print(s['id'],s['duration'],flush=True)
(root/'scenes.json').write_text(json.dumps(scenes,indent=2))
