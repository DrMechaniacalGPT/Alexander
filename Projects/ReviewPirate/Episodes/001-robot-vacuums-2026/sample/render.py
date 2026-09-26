"""Original vector-animation sample. No product footage or generated test results.
Usage: python render.py [--stills]  (expects timing.json and narration.wav)
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,math,json,subprocess,sys,imageio_ffmpeg,textwrap
R=Path(__file__).parent; W,H=1280,720; FPS=30
PAPER='#f2efe5'; INK='#193b3a'; MUTED='#6c807a'; LIME='#d3e87b'; CORAL='#e59275'; BLUE='#9ac6ce'; LIGHT='#faf8f0'; LINE='#d7ddd0'
F='/usr/share/fonts/truetype/dejavu/'
fonts={}
def font(n,bold=False,mono=False):
 k=(n,bold,mono)
 if k not in fonts: fonts[k]=ImageFont.truetype(F+('DejaVuSansMono' if mono else 'DejaVuSans')+('-Bold' if bold else '')+'.ttf',n)
 return fonts[k]
def ease(t):
 t=max(0,min(1,t));return 1-(1-t)**3
def mix(a,b,t):return a+(b-a)*t
def txt(d,pos,s,n=24,fill=INK,b=False,anchor=None,mono=False):
 d.text(pos,s,font=font(n,b,mono),fill=fill,anchor=anchor,spacing=7)
def line(d,pts,fill=INK,w=3):d.line(pts,fill=fill,width=w,joint='curve')
def rr(d,box,fill=LIGHT,outline=None,r=18,w=2):d.rounded_rectangle(tuple(map(round,box)),r,fill=fill,outline=outline,width=w)
def pill(d,x,y,s,bg=LIME,fg=INK,n=15):
 length=d.textlength(s,font=font(n,True));rr(d,(x,y,x+length+28,y+32),bg,r=16);txt(d,(x+14,y+7),s,n,fg,True)
def arrow(d,a,b,color=INK,w=3):
 line(d,[a,b],color,w);ang=math.atan2(b[1]-a[1],b[0]-a[0]); z=10
 d.polygon([b,(b[0]-z*math.cos(ang-.5),b[1]-z*math.sin(ang-.5)),(b[0]-z*math.cos(ang+.5),b[1]-z*math.sin(ang+.5))],fill=color)
def robot(d,x,y,size=60,angle=0):
 # Diagrammatic, intentionally not a rendering of any named model.
 d.ellipse((x-size,y-size*.42+13,x+size,y+size*.42+13),fill='#b1bbb0')
 d.ellipse((x-size,y-size*.48,x+size,y+size*.48+7),fill=INK)
 d.ellipse((x-size+4,y-size*.48-10,x+size-4,y+size*.48-3),fill=LIGHT,outline=INK,width=2)
 d.ellipse((x-15,y-18,x+15,y-3),fill=BLUE,outline=INK,width=2)
 d.arc((x-size+13,y-size*.48-5,x+size-13,y+size*.48-8),10,130,fill=MUTED,width=2)
 d.ellipse((x+size*.48-3,y-8,x+size*.48+3,y-2),fill=CORAL)
 for a in [angle,angle+2.1,angle+4.2]:
  line(d,[(x+size*.85,y+8),(x+size*.85+15*math.cos(a),y+8+9*math.sin(a))],INK,2)
def floor(d,cx,cy,scale=1,carpet=False,t=0):
 # Isometric plane with a moving robot; no debris disappears (not a performance simulation).
 ax=230*scale;ay=112*scale
 def p(u,v):return(cx+(u-v)*ax,cy+(u+v)*ay)
 pts=[p(-1,-1),p(1,-1),p(1,1),p(-1,1)]
 d.polygon([(x,y+15) for x,y in pts],fill='#bdc7bd')
 d.polygon(pts,fill=CORAL if carpet else '#e0ddcc',outline=INK)
 for i in np.linspace(-1,1,11):
  line(d,[p(i,-1),p(i,1)],'#c98b75' if carpet else '#c4c7b7',1)
 if carpet:
  for i in range(34):
   u=math.sin(i*13.7)*.88;v=math.cos(i*5.9)*.88;x,y=p(u,v)
   d.arc((x-7,y-3,x+8,y+4),0,210,fill='#835d4a',width=2)
 else:
  for j in [-.5,0,.5]:line(d,[p(-1,j),p(1,j)],'#c4c7b7',1)
 # Persistent path is movement only, not a claim of pickup.
 points=[p(-.65+.3*math.sin(k*.18),-.65+k*.014) for k in range(80)]
 upto=int((t*.2%1)*79)+1
 if upto>1:line(d,points[:upto],BLUE,4)
 u=-.15+.45*math.sin(t*.55);v=.1+.45*math.cos(t*.4)
 x,y=p(u,v);robot(d,x,y,48*scale,t*6)
def dog(d,x,y,s=1):
 # A rug that is 'mostly dog': clearly a joke, not a product trial.
 d.ellipse((x-100*s,y-26*s,x+85*s,y+31*s),fill=LIGHT,outline=INK,width=3)
 d.ellipse((x+52*s,y-57*s,x+121*s,y+9*s),fill=LIGHT,outline=INK,width=3)
 d.polygon([(x+54*s,y-51*s),(x+67*s,y+2*s),(x+88*s,y-46*s)],fill=INK)
 d.ellipse((x+99*s,y-30*s,x+107*s,y-22*s),fill=INK)
 d.ellipse((x+113*s,y-15*s,x+125*s,y-5*s),fill=INK)
 line(d,[(x-88*s,y-5*s),(x-116*s,y-29*s),(x-118*s,y-48*s)],INK,9)
 for k in [-50,32]:rr(d,(x+k*s,y+13*s,x+(k+22)*s,y+47*s),LIGHT,INK,r=8,w=2)
def chrome(d,t,total,dark=False,chapter='THE SHORT ANSWER'):
 c=LIGHT if dark else INK;m='#a5b7ac' if dark else MUTED
 txt(d,(48,29),'FIELDNOTES',19,c,True,mono=True)
 txt(d,(235,32),'A REVIEW OF THE REVIEWS',12,m,mono=True)
 txt(d,(1232,32),'ROBOT VACUUMS / 01',13,m,anchor='ra',mono=True)
 line(d,[(48,65),(1232,65)],'#48635b' if dark else LINE,1)
 txt(d,(48,87),chapter,13,LIME if dark else MUTED,True,mono=True)
 d.rectangle((0,715,int(W*t/total),719),fill=LIME if dark else INK)
def title(d,lines,x=48,y=150,n=57,color=INK):
 for i,s in enumerate(lines):txt(d,(x,y+i*(n+7)),s,n,color,True)
def source(d,s,dark=False):
 txt(d,(48,595),s,13,'#b4c4b7' if dark else MUTED,mono=True)
 txt(d,(1232,595),'CHECKED 26 SEP 2026',12,'#b4c4b7' if dark else MUTED,anchor='ra',mono=True)
def caption(d,s,t,duration):
 # Sentence/phrase chunks follow voice duration proportionally within each synthesized scene.
 words=s.split();chunks=[];cur=[]
 for w in words:
  if len(' '.join(cur+[w]))>79 and cur:chunks.append(' '.join(cur));cur=[]
  cur.append(w)
 if cur:chunks.append(' '.join(cur))
 weights=[len(c) for c in chunks]; target=max(0,min(1,(t-.16)/max(.1,duration-.54)))*sum(weights)
 chosen=chunks[-1]
 for c,w in zip(chunks,weights):
  if target<=w:chosen=c;break
  target-=w
 tw=d.textlength(chosen,font=font(21));rr(d,((W-tw)/2-19,644,(W+tw)/2+19,691),INK,r=10)
 txt(d,(W/2,657),chosen,21,LIGHT,anchor='ma')
def scene_frame(s,u,t,total):
 id=s['id']; dark=id in ['conflict','distinction','method']; im=Image.new('RGB',(W,H),INK if dark else PAPER);d=ImageDraw.Draw(im)
 chapters={'shortcut':'THE SHORT ANSWER','hardfloor':'01 / START WITH YOUR FLOOR','caveat':'02 / READ THE EXCEPTION','dog':'YOUR HOME IS PART OF THE QUESTION','sources':'GO STRAIGHT TO THE ORIGINALS','conflict':'SAME PRODUCT. DIFFERENT QUESTIONS.','distinction':'SEPARATE THE CLAIMS','method':'HOW WE MAKE THE SHORTCUT','close':'LESS TAB OPENING. MORE CLARITY.'}
 chrome(d,t,total,dark,chapters[id]);p=ease(u/0.8)
 if id=='shortcut':
  title(d,['The shortcut.','Then the receipts.'],y=154,n=65)
  pill(d,50,335,'ANSWER FIRST',LIME)
  # Three source cards feed into one useful result.
  for i,label in enumerate(['TESTS','REVIEWS','YOUR HOME']):
   x=760+i*35;y=164+i*84+12*math.sin(u*.6+i)
   rr(d,(x,y,x+260,y+65),[LIGHT,BLUE,LIME][i],INK,r=13)
   txt(d,(x+21,y+21),label,21,INK,True,mono=True)
  arrow(d,(796,435),(670,492));pill(d,398,473,'ONE USEFUL DECISION',INK,LIGHT,19)
  txt(d,(50,520),'No countdown. No treasure hunt.',22,MUTED)
  source(d,'FORMAT PILOT / ORIGINAL ANIMATION / SYNTHETIC NARRATION')
 elif id in ['hardfloor','caveat']:
  title(d,['Mostly','hard floors?'] if id=='hardfloor' else ['One important','exception.'],n=60)
  if id=='hardfloor':
   pill(d,48,325,'PREMIUM SHORTLIST')
   txt(d,(48,384),'Roborock',24,MUTED)
   txt(d,(48,420),'Saros 10R',45,INK,True)
   txt(d,(48,491),'A starting point, not a universal winner.',17,MUTED)
   floor(d,938,338,.66,False,u)
  else:
   pill(d,48,325,'CARPET + PET HAIR',CORAL)
   txt(d,(48,390),'RTINGS flags weak pickup.',27,INK,True)
   txt(d,(48,441),'Check the relevant test before buying.',20,MUTED)
   floor(d,938,338,.66,True,u)
   pill(d,782,515,'ILLUSTRATION / NOT TEST FOOTAGE',LIGHT,INK,11)
  source(d,'SOURCE: RTINGS / BEST ROBOT VACUUMS + SAROS 10R REVIEW')
 elif id=='dog':
  title(d,['If your rug','is mostly dog...'],n=56)
  floor(d,936,374,.65,True,u*.1)
  dog(d,940,330+math.sin(u*1.5)*2,1.08)
  pill(d,48,357,'OVERALL WINNER ≠ YOUR WINNER',CORAL,INK,15)
  txt(d,(48,430),'Your priority changes the decision.',23,MUTED)
  source(d,'EDITORIAL INFERENCE FROM RTINGS / ILLUSTRATION, NOT A PRODUCT TEST')
 elif id=='sources':
  title(d,['Prefer the original tests?'],n=49,y=146)
  for i,(label,sub,kind) in enumerate([('RTINGS','Lab results + buying guides','READ'),('The Hook Up','Flagship comparison video','WATCH')]):
   x=48+i*611;y=255+20*(1-ease((u-i*.15)/.7))
   rr(d,(x,y,x+574,y+233),LIGHT,LINE,r=20)
   pill(d,x+25,y+24,kind,LIME if i==0 else BLUE)
   txt(d,(x+25,y+79),label,43,INK,True)
   txt(d,(x+25,y+143),sub,20,MUTED)
   arrow(d,(x+482,y+184),(x+527,y+184),INK,3)
  txt(d,(48,525),'Direct source links accompany this sample.',22,MUTED)
  source(d,'SOURCE MAP: RTINGS.COM / THESMARTHOMEHOOKUP.COM')
 elif id=='conflict':
  txt(d,(48,135),'Qrevo Curv 2 Flow',49,LIGHT,True)
  # Pair of contrasting claims about one model, not commensurate scores.
  labels=[('THE HOOK UP','Top overall score','in its seven-model comparison',LIME),('RTINGS','Poor pet-hair pickup','on carpet',CORAL)]
  for i,(a,b,c,col) in enumerate(labels):
   x=48+i*611;y=246+25*(1-ease((u-i*1.8)/.6))
   rr(d,(x,y,x+574,y+243),'#254b47',None,r=18)
   pill(d,x+24,y+22,a,col)
   txt(d,(x+24,y+90),b,31,LIGHT,True)
   txt(d,(x+24,y+143),c,19,'#c4d2c7')
   line(d,[(x+24,y+208),(x+24+480*ease((u-i*1.8)/1.2),y+208)],col,5)
  source(d,'SOURCES: THE HOOK UP / 8 APR 2026; RTINGS / CURV 2 FLOW REVIEW',True)
 elif id=='distinction':
  title(d,['Different questions.','Not a clean contradiction.'],n=46,color=LIGHT,y=137)
  # Two conceptual lenses orbit and separate; no invented numerical scores.
  sep=220+50*ease(u/3);cy=409
  for i,(x,col,label,sub) in enumerate([(640-sep,LIME,'OVERALL','Many tradeoffs'),(640+sep,CORAL,'ONE JOB','Carpet pet hair')]):
   d.ellipse((x-130,cy-88,x+130,cy+88),outline=col,width=3)
   d.arc((x-141,cy-99,x+141,cy+99),u*30+i*90,u*30+70+i*90,fill=col,width=7)
   txt(d,(x,cy-24),label,30,LIGHT,True,anchor='ma')
   txt(d,(x,cy+21),sub,19,'#b9ccc0',anchor='ma')
  txt(d,(640,397),'≠',56,LIGHT,True,anchor='ma')
  source(d,'INTERPRETATION / THESE ARE DIFFERENT CLAIMS, NOT NORMALIZED SCORES',True)
 elif id=='method':
  title(d,['Product. Test. Home.'],n=58,color=LIGHT,y=145)
  for i,(label,col) in enumerate([('PRODUCT',BLUE),('TEST',LIME),('YOUR HOME',CORAL)]):
   x=48+i*411;y=286
   rr(d,(x,y,x+366,y+167),'#254b47',None,r=15)
   pill(d,x+22,y+20,f'0{i+1}',col)
   txt(d,(x+22,y+91),label,30,LIGHT,True)
   if i<2:
    dotx=x+366+40*((u*.28+i*.2)%1);d.ellipse((dotx-5,y+82,dotx+5,y+92),fill=col)
  txt(d,(48,504),'No fake average.',29,LIGHT,True)
  txt(d,(644,504),'No mystery score.',29,LIGHT,True)
  source(d,'OUR METHOD / TRACEABLE CLAIMS INSTEAD OF COUNTING WINNER VOTES',True)
 elif id=='close':
  title(d,['A better question.','A better shortlist.'],n=60,y=150)
  txt(d,(48,324),'Pick the problem you need solved.',25,MUTED)
  # Receipt unroll with source ticks.
  x=906;y=156; h=340*ease(u/1.7)
  if h>50:
   rr(d,(x-137,y,x+137,y+h),LIGHT,LINE,r=12)
   txt(d,(x,y+22),'THE RECEIPTS',18,INK,True,anchor='ma',mono=True)
   for i,label in enumerate(['Original sources','Exact model','Relevant test','Honest limits']):
    yy=y+79+i*56
    if yy+24<y+h:
     d.ellipse((x-108,yy+1,x-90,yy+19),fill=LIME)
     txt(d,(x-76,yy),label,17,INK)
  pill(d,48,418,'THE SHORTCUT COMES FIRST',LIME,INK,17)
  txt(d,(48,477),'The receipts come with it.',28,INK,True)
  source(d,'FIELDNOTES IS A WORKING VISUAL IDENTITY / BRAND NOT SELECTED')
 caption(d,s['caption'],u,s['duration'])
 return im

def srt_stamp(t):
 ms=int(round(t*1000));return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
def main():
 scenes=json.loads((R/'timing.json').read_text());total=scenes[-1]['end'];(R/'frames').mkdir(exist_ok=True)
 contacts=[]
 for i,s in enumerate(scenes):
  u=min(s['duration']-.2,max(2,s['duration']*.55));im=scene_frame(s,u,s['start']+u,total);im.save(R/'frames'/f'{i:02}-{s["id"]}.png');contacts.append(im.resize((426,240)))
 contact=Image.new('RGB',(1278,720),PAPER)
 for i,im in enumerate(contacts):contact.paste(im,((i%3)*426,(i//3)*240))
 contact.save(R/'contact-sheet.jpg')
 (R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{srt_stamp(s["start"])} --> {srt_stamp(s["end"])}\n{s["caption"]}' for i,s in enumerate(scenes))+'\n')
 if '--stills' in sys.argv:return
 ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
 cmd=[ffmpeg,'-y','-loglevel','warning','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(R/'narration.wav'),'-c:v','libx264','-crf','19','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-af','loudnorm=I=-16:TP=-1.5:LRA=9','-movflags','+faststart','-shortest',str(R/'sample-v1.mp4')]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);idx=0
 for f in range(int(round(total*FPS))):
  t=f/FPS
  while idx<len(scenes)-1 and t>=scenes[idx]['end']:idx+=1
  s=scenes[idx];proc.stdin.write(scene_frame(s,t-s['start'],t,total).tobytes())
  if f%300==0:print('render',round(t,1),'/',round(total,1),flush=True)
 proc.stdin.close();rc=proc.wait();assert rc==0
 print('saved',R/'sample-v1.mp4',flush=True)
if __name__=='__main__':main()
