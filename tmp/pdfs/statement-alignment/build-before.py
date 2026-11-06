from pathlib import Path
from io import BytesIO
import sys,math
sys.path.insert(0,str(Path.cwd()/'tmp/pdfs/style-revision'))
from portfolio_content import INTRO,PAGES
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from PIL import Image
ROOT=Path.cwd();TMP=ROOT/'tmp/pdfs';OUT=ROOT/'output/pdf/Evey_Huang_Research_Portfolio.pdf'
for name in ['Space','SpaceBold','News']:pdfmetrics.registerFont(TTFont(name,str(TMP/'fonts'/f'{name}-static.ttf')))
pdfmetrics.registerFontFamily('Space',normal='Space',bold='SpaceBold',italic='Space',boldItalic='SpaceBold')
W,H=612,792;M=44;CW=524;INK='#17181b';MUTED='#595d65';ACC='#a65f50';LINE='#c9cac5';BG='#f6f6f3'
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('Evey Huang | Research Portfolio');c.setAuthor('Evey Huang');c.setSubject('Human-AI collaboration in teams and organizations')
def para_obj(s,size,font='Space',color=INK,leading=None):
 return Paragraph(s,ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.32,textColor=HexColor(color)))
def para(s,x,y,w,size=10.3,font='Space',color=INK,leading=None):
 p=para_obj(s,size,font,color,leading);_,h=p.wrap(w,700);assert y+h<742,(s[:60],y+h);p.drawOn(c,x,H-y-h);return y+h

def text(s,x,y,size=10,font='Space',color=INK):
 c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,H-y-size,s)
def line(x1,y1,x2,y2,color=LINE):
 c.setStrokeColor(HexColor(color));c.setLineWidth(.6);c.line(x1,H-y1,x2,H-y2)
def rule(y):line(M,y,W-M,y)
def base(n,label):
 c.setFillColor(HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0)
 text('EVEY HUANG',M,25,8,color=ACC);text('HUMAN-AI COLLABORATION',408,25,7.5,color=MUTED);rule(49)
 rule(749);text('eveyhuang.com',M,761,8,color=MUTED);c.linkURL('https://www.eveyhuang.com/',(M,14,M+110,32))
 text(label.upper(),246,762,7,color=MUTED);text(f'{n:02d} / 10',532,761,8,color=MUTED)
 c.bookmarkPage(str(n));c.addOutlineEntry(label,str(n),0)
def raster(im,w,h):
 im=im.convert('RGB');im.thumbnail((int(w*3),int(h*3)),Image.Resampling.LANCZOS);b=BytesIO();im.save(b,format='JPEG',quality=92,optimize=True);b.seek(0);return ImageReader(b)
def body(sections,y,limit,size=10.3):
 def measure(sz):
  h=0
  for title,s in sections:
   if title:h+=para_obj(title,12.3,'SpaceBold',leading=15).wrap(CW,700)[1]+5
   h+=para_obj(s,sz,leading=sz*1.31).wrap(CW,700)[1]+10
  return h
 while y+measure(size)>limit and size>9.4:size=round(size-.1,2)
 assert y+measure(size)<=limit,('body overflow',y+measure(size),limit)
 for title,s in sections:
  if title:y=para(title,M,y,CW,12.3,'SpaceBold',leading=15)+5
  y=para(s,M,y,CW,size,leading=size*1.31)+10
 print('body',round(size,1),'end',round(y,1))
 return y

def refheight(ref):return 25+sum(para_obj(t,7.5,color=MUTED,leading=9.5).wrap(CW,700)[1]+4 for t in ref)
def refs(ref,y):
 rule(y);text('REFERENCES',M,y+8,7,color=MUTED);yy=y+23
 for t in ref:yy=para(t,M,yy,CW,7.5,color=MUTED,leading=9.5)+4

def figure(kind,y):
 if kind=='coaching':
  im=Image.open(TMP/'style-revision/risk-model-detail.png');h=CW*im.height/im.width
  c.drawImage(ImageReader(im),M,H-y-h,CW,h,mask='auto')
  para('Interface detail: a mentor can revise the risk definition guiding subsequent AI questions. Excerpt from Huang et al. (2025), Fig. 4B [2]; original highlighting retained.',M,y+h+6,CW,8,color=MUTED,leading=10.5)
 elif kind=='pipeline':
  labels=['Pitch video','Codebook-guided<br/>annotation','Interaction<br/>event records','Behavioral<br/>analysis']
  bw=119;gap=16
  for i,label in enumerate(labels):
   x=M+i*(bw+gap);c.setFillColor(HexColor('#edf0ed'));c.setStrokeColor(HexColor(LINE));c.roundRect(x,H-y-42,bw,42,3,fill=1,stroke=1)
   para(label,x+9,y+7,bw-18,9.4,leading=12)
   if i<3:
    a=x+bw+2;b=x+bw+gap-2;line(a,y+21,b,y+21,MUTED);line(b-4,y+18,b,y+21,MUTED);line(b-4,y+24,b,y+21,MUTED)
  para('Measurement sequence for the entrepreneurship study. Agreement with human coding is examined separately; the diagram describes the method and does not report validation results.',M,y+49,CW,8,color=MUTED,leading=10.5)

base(1,'Introduction')
text('RESEARCH PORTFOLIO',M,83,8,color=ACC);text('Evey Huang, PhD.',M,112,28,'SpaceBold',ACC)
para('Research Assistant Professor<br/>Kellogg School of Management<br/>Northwestern University',M,162,330,10.5,leading=16)
c.saveState();path=c.beginPath();path.circle(476,H-151,68);c.clipPath(path,stroke=0,fill=0)
im=Image.open(ROOT/'src/assets/evey-profile.png');iw,ih=im.size;s=max(136/iw,136/ih);c.drawImage(raster(im,iw*s,ih*s),408-(iw*s-136)/2,H-219-(ih*s-136)/2,iw*s,ih*s,mask='auto');c.restoreState()
y=para('Human-AI collaboration in teams and organizations',M,258,CW,25,'News',leading=29)+24
body(INTRO,y,682,10.5)
rule(696);para('<link href="mailto:jiaxinh.evey@gmail.com">jiaxinh.evey@gmail.com</link> / <link href="https://www.eveyhuang.com/">eveyhuang.com</link>',M,709,CW,10)
c.showPage()
for n,label,kicker,title,lead,sections,reference,visual in PAGES:
 base(n,label);text(kicker,M,71,8,color=ACC)
 y=para(title,M,91,CW,27,'SpaceBold',leading=30)+12
 y=para(lead,M,y,CW,16.5,'News',leading=20)+20
 if n in (3,4,6,9):
  num={3:1,4:2,6:5,9:6}[n];sections=list(sections);t,s=sections[0];sections[0]=(t,s+f' [{num}]')
 refstart=735-refheight(reference) if reference else 735
 visheight=92 if visual=='coaching' else 85 if visual else 0
 visstart=refstart-visheight-8
 limit=(visstart-13) if visual else (refstart-13 if reference else 730)
 print('page',n)
 end=body(sections,y,limit)
 if visual:figure(visual,visstart)
 if reference:refs(reference,refstart)
 c.showPage()
c.save();print(OUT)
