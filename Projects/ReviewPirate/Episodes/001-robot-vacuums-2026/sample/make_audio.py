from pathlib import Path
import json,wave,numpy as np
from piper import PiperVoice,SynthesisConfig
root=Path(__file__).parent
voice=PiperVoice.load(str(root/'models/en_US-ljspeech-high.onnx'))
cfg=SynthesisConfig(length_scale=1.12,noise_scale=0.55,noise_w_scale=0.65,normalize_audio=True)
scenes=json.loads((root/'scenes.json').read_text())
audio=[];cursor=0;sr=22050
for i,s in enumerate(scenes):
 a=np.concatenate([c.audio_float_array for c in voice.synthesize(s['text'],cfg)])
 # Modest head/tail room; scene timing is derived from audio, not guessed.
 a=np.concatenate([np.zeros(int(sr*.16)),a,np.zeros(int(sr*.38))]).astype(np.float32)
 # Quantize scene boundary to a video frame.
 dur=np.ceil(len(a)/sr*30)/30
 a=np.pad(a,(0,int(round(dur*sr))-len(a)))
 s.update(start=cursor,duration=dur,end=cursor+dur)
 audio.append(a);cursor+=dur
 print(s['id'],round(dur,2),flush=True)
a=np.concatenate(audio); peak=np.max(np.abs(a)); a=a/max(peak,1)*.86
with wave.open(str(root/'narration.wav'),'wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((a*32767).astype('<i2').tobytes())
(root/'timing.json').write_text(json.dumps(scenes,indent=2))
print('TOTAL',cursor,'PEAK',float(np.max(np.abs(a))))
