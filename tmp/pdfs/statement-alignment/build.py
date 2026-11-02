from pathlib import Path
from io import BytesIO
import sys
sys.path.insert(0,str(Path.cwd()/'tmp/pdfs/statement-alignment'))
from content import INTRO,PAGES
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
W,H=612,792;M=44;CW=524;INK='#17181b';MUTED='#595d65';ACC='#a65f50';LINE='#c9cac5';BG='#f6f6f3';TOTAL=1+len(PAGES)
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('Evey Huang | Research Portfolio');c.setAuthor('Evey Huang');c.setSubject('Human-AI collaboration in teams and organizations')
def clean(s):return s.replace('–','-').replace('—','-').replace('‑','-')
def po(s,size,font='Space',color=INK,leading=None):
 return Paragraph(clean(s),ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.32,textColor=HexColor(color)))
def para(s,x,y,w,size=10.3,font='Space',color=INK,leading=None):
 p=po(s,size,font,color,leading);_,h=p.wrap(w,700);assert y+h<H-49,(s[:60],y+h);p.drawOn(c,x,H-y-h);return y+h

def text(s,x,y,size=10,font='Space',color=INK):
 c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,H-y-size,clean(s))
def rule(y):
 c.setStrokeColor(HexColor(LINE));c.setLineWidth(.6);c.line(M,H-y,W-M,H-y)
def base(n,label,landscape=False):
 global W,H,CW
 W,H=(792,612) if landscape else (612,792);CW=W-2*M;c.setPageSize((W,H))
 c.setFillColor(HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0)
 text('EVEY HUANG',M,25,8,color=ACC);text('HUMAN-AI COLLABORATION',W-204,25,7.5,color=MUTED);rule(49)
 rule(H-43);text('eveyhuang.com',M,H-31,8,color=MUTED);c.linkURL('https://www.eveyhuang.com/',(M,14,M+110,32))
 text(label.upper(),W/2-60,H-30,7,color=MUTED);text(f'{n:02d} / {TOTAL}',W-80,H-31,8,color=MUTED)
 c.bookmarkPage(str(n));c.addOutlineEntry(label,str(n),0)
def body(sections,y,limit,size=10.3):
 def measure(sz):
  h=0
  for title,s in sections:
   if title:h+=po(title,12.3,'SpaceBold',leading=15).wrap(CW,700)[1]+5
   h+=po(s,sz,leading=sz*1.31).wrap(CW,700)[1]+10
  return h
 while y+measure(size)>limit and size>9.2:size=round(size-.1,2)
 assert y+measure(size)<=limit,('body overflow',y+measure(size),limit)
 for title,s in sections:
  if title:y=para(title,M,y,CW,12.3,'SpaceBold',leading=15)+5
  y=para(s,M,y,CW,size,leading=size*1.31)+10
 print('body',round(size,1),'end',round(y,1));return y

def refheight(ref):return 25+sum(po(t,7.5,color=MUTED,leading=9.5).wrap(CW,700)[1]+4 for t in ref)
def refs(ref,y):
 rule(y);text('REFERENCES',M,y+8,7,color=MUTED);yy=y+23
 for t in ref:yy=para(t,M,yy,CW,7.5,color=MUTED,leading=9.5)+4

def coaching(y):
 im=Image.open('/Users/eveyhuang/Desktop/flow.png');h=CW*im.height/im.width
 c.drawImage(ImageReader(im),M,H-y-h,CW,h,mask='auto')
 para('Coaching workflow [2]. Novices reflect and prioritize risks; mentors review the resulting context, prepare assistance, and revise the expert model guiding the system.',M,y+h+7,CW,8,color=MUTED,leading=10)

def pitch(n,label):
 base(n,label,True)
 im=Image.open('/Users/eveyhuang/Documents/NICO/Org_Sci-Entrepreneurial_Pitching/docs/figures/fig 1.png')
 w=662;h=w*im.height/im.width;x=(W-w)/2;y=57
 c.drawImage(ImageReader(im),x,H-y-h,w,h,mask='auto')
 para('Entrepreneurship pitching [5]: annotation, interaction records, and concept bottleneck analysis. Full project discussion on page 10.',M,550,CW,7.2,color=MUTED,leading=9)
 c.showPage()

base(1,'Introduction')
text('RESEARCH PORTFOLIO',M,83,8,color=ACC);text('Evey Huang, PhD.',M,112,28,'SpaceBold',ACC)
para('Research Assistant Professor<br/>Kellogg School of Management<br/>Northwestern University',M,162,330,10.5,leading=16)
c.saveState();path=c.beginPath();path.circle(476,H-151,68);c.clipPath(path,stroke=0,fill=0)
im=Image.open(ROOT/'src/assets/evey-profile.png').convert('RGB');im.thumbnail((700,700),Image.Resampling.LANCZOS);b=BytesIO();im.save(b,format='JPEG',quality=92);b.seek(0);im=Image.open(b);iw,ih=im.size;s=max(136/iw,136/ih);c.drawImage(ImageReader(im),408-(iw*s-136)/2,H-219-(ih*s-136)/2,iw*s,ih*s,mask='auto');c.restoreState()
y=para('Human-AI collaboration in teams and organizations',M,258,CW,25,'News',leading=29)+24
body(INTRO,y,682,10.5)
rule(696);para('<link href="mailto:jiaxinh.evey@gmail.com">jiaxinh.evey@gmail.com</link> / <link href="https://www.eveyhuang.com/">eveyhuang.com</link>',M,709,CW,10)
c.showPage()
for n,label,kicker,title,lead,sections,reference,visual in PAGES:
 if visual=='pitch':pitch(n,label);continue
 base(n,label);text(kicker,M,71,8,color=ACC)
 y=para(title,M,91,CW,25,'SpaceBold',leading=28)+12
 y=para(lead,M,y,CW,16,'News',leading=19)+18
 refstart=735-refheight(reference) if reference else 735
 visheight=195 if visual=='coaching' else 0
 visstart=refstart-visheight-8
 limit=(visstart-10) if visual else (refstart-13 if reference else 730)
 print('page',n)
 end=body(sections,y,limit)
 if visual:coaching(visstart)
 if reference:refs(reference,refstart)
 c.showPage()
c.save();print(OUT)
