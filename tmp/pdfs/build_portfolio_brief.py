from pathlib import Path
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from fontTools.ttLib import TTFont as Font
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image

ROOT=Path.cwd(); TMP=ROOT/'tmp/pdfs'; OUT=ROOT/'output/pdf/Evey_Huang_Research_Portfolio.pdf'
for name,file,axes in [('Space','SpaceGrotesk',{'wght':400}),('SpaceBold','SpaceGrotesk',{'wght':600}),('News','Newsreader',{'wght':400,'opsz':24})]:
 f=instantiateVariableFont(Font(TMP/'fonts'/f'{file}.ttf'),axes,inplace=False); f.save(TMP/'fonts'/f'{name}-static.ttf'); pdfmetrics.registerFont(TTFont(name,str(TMP/'fonts'/f'{name}-static.ttf')))
pdfmetrics.registerFontFamily('Space',normal='Space',bold='SpaceBold',italic='Space',boldItalic='SpaceBold')
W,H=612,792; M=44; CW=W-2*M
INK='#17181b'; MUTED='#595d65'; ACC='#a65f50'; LINE='#c9cac5'; BG='#f6f6f3'
c=canvas.Canvas(str(OUT),pagesize=(W,H)); c.setTitle('Evey Huang | Research Portfolio');c.setAuthor('Evey Huang'); c.setSubject('Human-AI collaboration in teams and organizations')
def text(s,x,y,size=10,font='Space',color=INK):
 c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,H-y-size,s)
def para(s,x,y,w,size=10.5,font='Space',color=INK,leading=None):
 st=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.4,textColor=HexColor(color))
 p=Paragraph(s,st);_,h=p.wrap(w,700);p.drawOn(c,x,H-y-h);return y+h

def rule(y,x=M,w=CW):
 c.setStrokeColor(HexColor(LINE));c.setLineWidth(.6);c.line(x,H-y,x+w,H-y)
def base(n,label):
 c.setFillColor(HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0)
 text('EVEY HUANG',M,25,8,color=ACC);text('HUMAN-AI COLLABORATION',W-204,25,7.5,color=MUTED);rule(49)
 rule(749);text('eveyhuang.com',M,761,8,color=MUTED);c.linkURL('https://www.eveyhuang.com/',(M,14,M+110,32),relative=0)
 text(label.upper(),246,762,7,color=MUTED);text(f'{n:02d} / 06',W-80,761,8,color=MUTED)
 c.bookmarkPage(str(n));c.addOutlineEntry(label,str(n),level=0)
def heading(kicker,title):
 text(kicker,M,72,8,color=ACC);return para(title,M,94,CW,29,'SpaceBold',leading=32)
def raster(im,w,h):
 im=im.convert('RGB'); im.thumbnail((int(w*3),int(h*3)),Image.Resampling.LANCZOS)
 b=BytesIO(); im.save(b,format='JPEG',quality=90,optimize=True);b.seek(0);return ImageReader(b)
def img(path,x,y,w,h):
 im=Image.open(path); iw,ih=im.size;scale=min(w/iw,h/ih);dw,dh=iw*scale,ih*scale
 c.drawImage(raster(im,dw,dh),x+(w-dw)/2,H-y-dh,dw,dh,mask='auto')
def block(title,status,body,y,w=CW,x=M,size=10.2):
 text(status.upper(),x,y,7.5,color=ACC); y+=15
 y=para(title,x,y,w,14,'SpaceBold',leading=17)+7
 return para(body,x,y,w,size,leading=size*1.35)+17

def refs(entries,y):
 rule(y);text('REFERENCES',M,y+10,7,color=MUTED); yy=y+25
 for e in entries: yy=para(e,M,yy,CW,7.5,color=MUTED,leading=9.5)+4
 assert yy<739,('reference overflow',yy)

# 1: Introduction
base(1,'Introduction')
text('hi.',M,84,83,'SpaceBold')
c.saveState(); path=c.beginPath();path.circle(466,H-172,77);c.clipPath(path,stroke=0,fill=0)
im=Image.open(ROOT/'src/assets/evey-profile.png'); iw,ih=im.size;scale=max(154/iw,154/ih); c.drawImage(raster(im,iw*scale,ih*scale),389-(iw*scale-154)/2,H-249-(ih*scale-154)/2,iw*scale,ih*scale,mask='auto');c.restoreState()
text('Evey Huang, PhD.',364,265,17,'SpaceBold',ACC)
text('RESEARCH PORTFOLIO',M,203,8,color=MUTED)
para('I study human-AI collaboration where the human is part of a team or organization.',M,311,CW,27,'News',leading=32)
para('Working with others to tackle complex problems in science, entrepreneurship, and knowledge work.',M,409,470,17,'News',leading=23)
rule(491)
para('<b>Research Assistant Professor</b><br/>Kellogg School of Management, Northwestern University',M,515,CW,11,leading=17)
para('I bring methods from HCI, design, and computational social science to organizational questions, using AI both to study collective work and to design systems that change how work happens.',M,578,485,11,leading=16)
text('LET\'S CONNECT',M,679,8,color=ACC)
para('<link href="mailto:jiaxinh.evey@gmail.com">jiaxinh.evey@gmail.com</link>   /   <link href="https://www.eveyhuang.com/">eveyhuang.com</link>',M,699,CW,10)
c.showPage()
# 2 overview
base(2,'Research overview');heading('RESEARCH OVERVIEW','AI in collective work')
para('How can AI make expertise usable, reveal how collaboration unfolds, and shape the ideas and judgments that groups produce?',M,151,CW,21,'News',leading=27)
rows=[('01','Making expertise usable','Articulating tacit reasoning and connecting people to the knowledge they need.','4-ai-coach.png','3'),('02','Understanding collaboration','Observing how people integrate knowledge, coordinate, and respond to one another.','2-ai-team.png','4'),('03','AI and collective outcomes','Examining the breadth of ideas, the diversity of judgments, and whose input matters.','3-design.png','5')]
for i,(num,title,desc,asset,dest) in enumerate(rows):
 y=263+i*120;rule(y);img(ROOT/'public'/asset,M,y+10,86,99)
 text(num,151,y+17,9,color=ACC);para(title,178,y+14,385,16,'SpaceBold',leading=20)
 para(desc,178,y+45,365,10.5,leading=15)
 c.linkRect('',dest,(M,H-y-112,W-M,H-y),relative=0,thickness=0)
rule(630)
text('HOW I WORK',M,647,8,color=ACC)
para('Field observation and interviews clarify the work. System design explores new forms of support. Multimodal measurement and computational experiments examine interaction and collective outcomes at scale.',M,669,CW,11,leading=16)
c.showPage()
# 3 expertise
base(3,'Making expertise usable');heading('RESEARCH STREAM 01','Making expertise usable')
para('Helping people prepare to learn from and support one another.',M,142,325,21,'News',leading=25)
para('Expertise is distributed across people and often difficult to articulate. I study the practices that make it available, then build AI grounded in those practices.',M,211,324,10.5,leading=15)
img(ROOT/'public/4-ai-coach.png',399,135,169,158)
y=307
y=block('From coaching practice to a cognitive model [1]','CSCW 2023 / Empirical study','Analysis of 24 coaching sessions with three coaches and 30 novices revealed how coaches turn project-specific experience into transferable lessons, connect people, question assumptions, and help novices ask for useful assistance.',y)
y=block('AI that helps us help each other [2]','CSCW 2025 / Design and exploratory deployment','I designed a proactive AI system that helps entrepreneurs surface assumptions and risks before coaching meetings. Mentors receive context and can revise the expert model. In a deployment with one mentor and 11 novices, participants reported more focused conversations; incomplete context still required verification.',y)
y=block('Collaboration skills and tacit judgment [3, 4]','Related foundations','A workplace-learning agenda examines how routines and technologies build collaboration skills. Earlier literary-style tools make difficult-to-articulate judgments available for exploration and reflection.',y)
refs(['[1] Huang, E., Rees Lewis, D., Gaudani, S., Easterday, M., &amp; Gerber, E. (2023). Intelligent Coaching Systems: Understanding One-to-many Coaching for Ill-defined Problem Solving. <link href="https://doi.org/10.1145/3579614">CSCW. doi:10.1145/3579614</link>.','[2] Huang, E., Easterday, M., &amp; Gerber, E. (2025). AI That Helps Us Help Each Other: A Proactive System for Scaffolding Mentor-Novice Collaboration in Entrepreneurship Coaching. <link href="https://doi.org/10.1145/3757549">CSCW. doi:10.1145/3757549</link>.','[3] Huang, E., et al. (2023). Supporting Workers in Developing Effective Collaboration Skills for Complex Work. <link href="https://doi.org/10.1145/3584931.3611290">CSCW Companion. doi:10.1145/3584931.3611290</link>.','[4] Sterman, S., Huang, E., Liu, V., &amp; Paulos, E. (2020). Interacting with Literary Style through Computational Tools. <link href="https://doi.org/10.1145/3313831.3376730">CHI. doi:10.1145/3313831.3376730</link>.'],max(y,610))
c.showPage()
# 4 multimodal
base(4,'Understanding collaboration');heading('RESEARCH STREAM 02','Understanding collaboration')
para('Making the unfolding process of teamwork observable.',M,142,325,21,'News',leading=25)
para('Across more than 1,000 hours of recorded interaction, I combine language, vocal cues, and visible behavior. We ground codebooks in organizational theory and validate AI annotations against human judgments.',M,211,324,10.5,leading=15)
img(ROOT/'public/2-ai-team.png',399,135,169,158)
y=307
y=block('Measuring what matters in teams [5]','Journal of Organization Design / To appear','With Brian Uzzi and Matt Groh, I develop a methodological agenda for linking organizational constructs to enacted behavior at greater scale, resolution, and temporal continuity.',y)
y=block('Three settings, connected questions','Empirical projects / Ongoing','<b>Scientific teams:</b> How do members build on, connect, evaluate, and extend one another\'s ideas? A manuscript in preparation examines integration behavior and collective outcomes.<br/><br/><b>Entrepreneurs and investors:</b> How do questions, challenges, and responses reveal preparedness, build rapport, and shape evaluators\' judgments?<br/><br/><b>Professional volleyball:</b> How is cohesion enacted in team huddles, and how does it relate to subsequent performance?',y)
rule(606);para('<b>Research support.</b> $75,000 from Microsoft\'s AI and the New Future of Work program. I independently wrote the proposal, with Brian Uzzi as PI. Our related TeamLens proposal was a finalist in the Stanford HAI and Google DeepMind AI for Organizations Grand Challenge.',M,620,CW,9.5,leading=13)
refs(['[5] Huang, E., Uzzi, B., &amp; Groh, M. (2026). Measuring What Matters in Teams with Multimodal AI. Journal of Organization Design. To appear.'],686)
c.showPage()
# 5 outcomes
base(5,'AI and collective outcomes');heading('RESEARCH STREAM 03','AI and collective outcomes')
para('Useful individual contributions do not necessarily add up to better collective work.',M,142,325,21,'News',leading=25)
para('I examine the breadth of possibilities explored, the variety of evaluative perspectives, and whose input can influence what happens next.',M,235,324,10.5,leading=15)
img(ROOT/'public/3-design.png',399,135,169,158)
y=307
y=block('Double compression in scientific ideas and reviews','Working manuscript / In preparation','With Matt Groh and Brian Uzzi, I compare 23 proposals and 85 expert reviews from a bioscience grant competition with outputs from Claude, Gemini, and GPT under the same call and evaluation criteria.',y)
y=para('<b>Generation:</b> AI proposals cluster around common ideas, leaving some distinctive human proposals underrepresented.<br/><br/><b>Evaluation:</b> AI panels can cover much of the territory of human reviews while producing more similar judgments, especially criticisms.',M,y-5,CW,10.2,leading=14)+15
y=para('These are output comparisons from one competition, not a test of scientists collaborating with AI or realized innovation. Effects vary across models, prompts, and measures.',M,y,CW,9.3,color=MUTED,leading=13)+23
y=block('Whose judgments shape the response? [6]','DIS 2024 / Honorable Mention','A scoping review and qualitative analysis of 17 papers on online harassment exposed gaps between intended beneficiaries\' needs and implemented systems. The work asks who can shape the definitions, judgments, and responses embedded in computational tools.',y)
refs(['[6] Huang, E., Sarma, A., Hwang, S., Chandrasekharan, E., &amp; Chancellor, S. (2024). Opportunities, Tensions, and Challenges in Computational Approaches to Addressing Online Harassment. <link href="https://doi.org/10.1145/3643834.3661623">DIS. doi:10.1145/3643834.3661623</link>.'],max(681,y+2))
c.showPage()
# 6 experience
base(6,'Experience');heading('A LITTLE MORE ABOUT ME','Research, design, and practice')
para('My work moves between understanding how people collaborate and building tools they can use together.',M,150,CW,22,'News',leading=28)
y=242
y=block('Studying collective work at Northwestern','Research Assistant Professor / Jul 2026 - Present','At Kellogg, I connect multimodal studies of team interaction with computational experiments on AI in scientific knowledge production. This builds on my postdoctoral work with Brian Uzzi and Matthew Groh (February 2025 - June 2026).',y)
y=block('Building with domain experts','Novohaven / Oct 2025 - Present','As an AI Advisor and Forward Deployment Engineer, I translate organizational knowledge into shared AI workflows that teams can inspect, revise, and use together. Previously, I advised Spark AI on learning products (2024-2025) and studied older adults\' health-record workflows at Northwestern Memorial Hospital (2022).',y)
y=block('Learning through sustained partnerships','Northwestern / PhD 2024; MS 2023','My PhD in Technology and Social Behavior bridged computer science and communication studies. A sustained partnership with an entrepreneurship incubator grounded my doctoral research. I also coached engineering students in human-centered design. I hold a BA in Economics from UC Berkeley (2017).',y)
rule(632);text('OUTSIDE WORK',M,648,8,color=ACC)
para('I play guitar and tennis, take film and digital photographs, read, doodle, and cook spicy food. If you are thinking about similar research questions, I would love to connect.',M,670,CW,11,leading=16)
c.showPage();c.save();print(OUT)
