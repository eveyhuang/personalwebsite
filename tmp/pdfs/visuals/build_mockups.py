from pathlib import Path
from io import BytesIO
import math,hashlib
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
ROOT=Path.cwd();TMP=ROOT/'tmp/pdfs/visuals';OUT=ROOT/'output/pdf/Evey_Huang_Visual_Mockups.pdf'
for name in ['Space','SpaceBold','News']:pdfmetrics.registerFont(TTFont(name,str(ROOT/'tmp/pdfs/fonts'/f'{name}-static.ttf')))
pdfmetrics.registerFontFamily('Space',normal='Space',bold='SpaceBold',italic='Space',boldItalic='SpaceBold')
c=canvas.Canvas(str(OUT),pagesize=(612,792));c.setTitle('Evey Huang | Portfolio visual concepts');c.setAuthor('Evey Huang / visual layout study')
W,H=612,792;M=40;CW=532
INK='#17181b';MUTED='#595d65';ACC='#a65f50';BG='#f6f6f3';LINE='#c9cac5';GREEN='#688477';BLUE='#607b91';PALE='#e7ece8'
def tx(s,x,y,size=10,font='Space',color=INK):
 c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,H-y-size,s)
def p(s,x,y,w,size=10,font='Space',color=INK,leading=None):
 q=Paragraph(s,ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.35,textColor=HexColor(color)));_,h=q.wrap(w,700);q.drawOn(c,x,H-y-h);return y+h

def line(x1,y1,x2,y2,color=LINE,dash=False,width=.7):
 c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.setDash(3,3) if dash else c.setDash();c.line(x1,H-y1,x2,H-y2);c.setDash()
def arrow(x1,y1,x2,y2,color=MUTED,dash=False):
 line(x1,y1,x2,y2,color,dash,1)
 a=math.atan2(y2-y1,x2-x1)
 for d in [-.45,.45]:line(x2,y2,x2-6*math.cos(a+d),y2-6*math.sin(a+d),color,width=1)
def rect(x,y,w,h,fill='#ffffff',stroke=LINE,r=4):
 c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke));c.setLineWidth(.7);c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=1)
def card(title,sub,x,y,w,h=76,color=GREEN):
 rect(x,y,w,h);line(x,y+1,x+w,y+1,color,width=2)
 yy=p(title,x+11,y+10,w-22,11,'SpaceBold',leading=14)+7
 p(sub,x+11,yy,w-22,8.7,color=MUTED,leading=11.5)
def number(n,x,y,color=ACC):
 c.setFillColor(HexColor(color));c.circle(x,H-y,9,fill=1,stroke=0);c.setFillColor(HexColor('#ffffff'));c.setFont('SpaceBold',9);c.drawCentredString(x,H-y-3,str(n))
def img(path,x,y,w,h):
 im=Image.open(path);iw,ih=im.size;s=min(w/iw,h/ih);dw,dh=iw*s,ih*s
 from reportlab.lib.utils import ImageReader
 c.drawImage(ImageReader(im),x+(w-dw)/2,H-y-dh,dw,dh,mask='auto');return dh

def base(n,label,title,lead):
 c.setFillColor(HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0)
 tx('EVEY HUANG',M,24,8,color=ACC);tx('VISUAL CONCEPT / FOR REVIEW',378,24,7.4,color=MUTED);line(M,48,572,48)
 tx(label.upper(),M,66,8,color=ACC);y=p(title,M,88,CW,26,'SpaceBold',leading=29)+12
 p(lead,M,y,CW,15,'News',leading=19)
 line(M,749,572,749);tx('Portfolio remains unchanged',M,761,7.6,color=MUTED);tx(f'{n:02d} / 08',522,761,8,color=MUTED)
 c.bookmarkPage(str(n));c.addOutlineEntry(title,str(n),0)
def note(text,source=None):
 line(M,678,572,678);tx('LAYOUT INTENT',M,690,7,color=ACC);p(text,M,704,CW,8.6,leading=11)
 if source:p(source,M,649,CW,7.2,color=MUTED,leading=9)
 c.showPage()
# 1 opportunities
base(1,'Placement plan','Visuals that do explanatory work','Keep the restored research narrative. Add visual space where the relationships, mechanisms, or evidence are difficult to picture.')
rows=[('02 / Overview','Three connected research questions','A visual index that explains what each stream studies and how the streams inform one another.','A'),('03 / Coaching model','How expertise becomes usable','A small network or mediation diagram: coaches translate experience, connect peers, and structure requests.','Later'),('04 / Coaching system','Two roles, one conversation','A workflow plus a companion page of actual screenshots. Show different support for novice and mentor, and the editable expert model.','B + C'),('06-07 / Multimodal studies','From video to interpretable evidence','A simplified pipeline, a visible human-validation branch, then a readable episode and exchange example.','D + E'),('08 / Double compression','Two stages, two types of narrowing','A conceptual comparison of generation and evaluation; clearly separate a schematic from a measured result.','F'),('09 / Participation and influence','Who supplies input; who decides?','A flow of reporting, classification, and response with control points marked.','G'),('10 / Experience','A compact research-to-practice timeline','Optional: small role labels or a shared-workflow diagram. Keep the personal prose; avoid decorative skill icons.','Later')]
y=181
for loc,title,desc,code in rows:
 line(M,y,572,y);tx(loc,M,y+9,8,color=ACC);tx(code,524,y+9,8,color=ACC)
 y=p(title,181,y+8,320,10.5,'SpaceBold',leading=13)+4
 y=p(desc,181,y,377,9.1,leading=12)+14
note('Recommended first pass: B+C, D+E, and F. Add A to orient readers; G is useful if space allows. Allow the portfolio to grow beyond ten pages rather than replacing explanations with figures.')
#2 map
base(2,'A / Current page 2','Three connected directions','A map of the research program, not a claim that one study causally proves the next.')
items=[('01','Making expertise usable','What do collaborators need to articulate and share?','Coaching model + AI system\nWorkplace learning + tacit judgment',GREEN),('02','Understanding collaboration','How does collective work unfold in interaction?','Multimodal measurement\nScientific teams + pitching + sports',ACC),('03','AI and collective outcomes','What range of ideas and judgments does the collective produce?','Double compression\nParticipation + decision authority',BLUE)]
for i,(num,title,q,projects,col) in enumerate(items):
 y=196+i*124;rect(M,y,CW,107,stroke=LINE);tx(num,54,y+14,18,'SpaceBold',col)
 p(title,99,y+12,440,15,'SpaceBold',leading=18);p(q,99,y+38,435,11,'News',leading=14)
 p(projects.replace('\n',' / '),99,y+73,429,9,color=MUTED,leading=12)
rect(M,584,CW,47,fill=PALE);p('<b>Shared design question:</b> How can AI support collaboration while preserving human interpretation, diverse perspectives, and meaningful influence?',54,594,503,10,leading=13)
note('Use as the visual index alongside the fuller overview text. Repeated 01 / 02 / 03 markers can identify each stream throughout the portfolio. Color distinguishes topics without implying a sequence.')
#3 flow
base(3,'B / Current page 4','Two roles, one conversation','AI prepares collaborators differently; the mentor can also revise the knowledge that guides the system.')
card('Novice preparation','Articulate project context, reflect on questions, prioritize risks.',40,195,228,88,GREEN)
card('Mentor preparation','Review context and omitted risks; specify goals and plan support.',344,195,228,88,BLUE)
arrow(268,239,302,239);arrow(344,239,310,239);number(1,306,239)
card('Shared coaching context','Project updates, diagnosed risks, reflections, and the novice\'s agenda.',166,315,280,78,ACC)
arrow(306,250,306,315)
card('Human coaching meeting','Use the preparation to explore uncertainty, interpret context, and plan next steps.',166,433,280,83,GREEN)
arrow(306,393,306,433)
rect(40,551,532,62,fill=PALE);p('<b>Editable expert model</b> / Project areas, risk definitions, and examples.',53,562,503,10.5,leading=14);p('Mentors can add or revise the model when the system misses an important risk.',53,585,503,9.2,color=MUTED)
line(553,551,553,300,BLUE,dash=True);arrow(553,300,458,300,BLUE,dash=True);arrow(458,300,458,283,BLUE,dash=True)
line(59,551,59,300,GREEN,dash=True);arrow(59,300,154,300,GREEN,dash=True);arrow(154,300,154,283,GREEN,dash=True)
tx('Model informs both roles',208,624,8.5,color=MUTED)
note('A half-page workflow on the narrative page, with the interface evidence on a facing or following page. Solid arrows show preparation; dashed lines show how the editable model guides future support.','Adapted conceptually from Huang, Easterday & Gerber (2025), Figs. 1 and 5. doi:10.1145/3757549. New portfolio drawing; not a new result.')
#4 screenshots
base(4,'C / Companion to current page 4','Show the system, not only describe it','Use selected, readable interface excerpts to demonstrate the design contribution.')
img(TMP/'novice.png',40,189,312,363)
number(1,370,207);p('Make risks discussable',389,194,174,12,'SpaceBold',leading=15)
p('The novice sees the diagnosis, the question, and their own response together. The interface helps turn a model output into a subject for reflection.',389,236,174,9.7,leading=13)
number(2,370,359);p('Choose a meeting agenda',389,347,174,12,'SpaceBold',leading=15)
p('The novice chooses which risks to discuss and can add other concerns. Preparing a human conversation is the point of the interaction.',389,389,174,9.7,leading=13)
line(40,567,572,567);img(TMP/'author.png',40,582,314,66)
number(3,370,591);p('Revise the expert model',389,578,174,11.5,'SpaceBold',leading=15)
p('Mentors can edit risk definitions, not only accept or reject an answer.',389,615,174,9.4,leading=12)
note('Use the novice dashboard as the main image and the authoring interface as a supporting detail. Preserve the full study methods, findings, and limitations on the adjacent narrative page.','Actual screenshot excerpts: Huang, Easterday & Gerber (2025), Fig. 3B and Fig. 4B, p. 9. Cropped from the supplied paper; original annotations retained. CC BY 4.0.')
#5 pipeline
base(5,'D / Current pages 6-7','From interaction to behavioral evidence','A simplified reading path through the entrepreneurship measurement pipeline, with validation visibly separate from prediction.')
card('1 / Pitch video','An episode of founder-investor interaction.',40,198,153,81,GREEN)
card('2 / MLLM annotation','Use a literature-grounded codebook to annotate behavior.',230,198,153,81,ACC)
card('3 / Event record','Who spoke, what happened, and when.',420,198,152,81,BLUE)
arrow(193,238,230,238);arrow(383,238,420,238)
rect(230,313,153,64,fill=PALE);p('<b>Codebook</b><br/>Construct definitions, scales, rules, and examples.',242,324,129,9.2,leading=12)
arrow(306,313,306,279,ACC)
rect(40,412,343,99,fill='#edf0ed');p('Human validation',53,424,313,13,'SpaceBold',leading=16);p('Two trained coders annotate a sample without seeing model outputs. Compare human-human and human-model agreement.',53,450,313,10,leading=14)
line(116,279,116,395,MUTED,dash=True);arrow(116,395,116,412,MUTED,dash=True)
line(496,279,496,529,MUTED);arrow(496,461,383,461,MUTED,dash=True)
card('4 / Interpretable analysis','Aggregate named concepts and examine their relationship to the offer outcome.',40,548,246,80,BLUE)
card('5 / Questions the model can address','What does interaction reveal beyond baseline information? Which concept families add information?',326,548,246,80,ACC)
arrow(286,588,326,588);line(496,511,496,529);line(496,529,163,529);arrow(163,529,163,548)
note('Use the full technical Fig. 1 only as a linked supplement. Keep this portfolio figure readable: five stages, one codebook, one validation branch. Exact sample counts and model versions can go in the caption.','Adapted from the supplied entrepreneurship Fig. 1 (working pipeline). No percentage bars or performance claims are reproduced. Pipeline structure is a method illustration, not validation evidence.')
#6 timeline
base(6,'E / Companion to current page 7','What a behavioral record looks like','Pair a whole-episode view with a guide to the coding fields so readers can see what the pipeline makes observable.')
tx('01 / THE EPISODE',40,189,8,color=ACC);img(TMP/'episode.png',40,209,532,130)
p('The record distinguishes speakers, actions, and decision moments over time. It supports questions about sequences of interaction, rather than only total speaking time.',40,346,532,10,leading=14)
line(40,392,572,392);tx('02 / HOW TO READ AN EXCHANGE',40,405,8,color=ACC)
card('Investor question','Topic and question type: ask, substantiate, or contest.',40,435,235,85,BLUE)
card('Founder response','Answer substance and grounding in a checkable specific.',337,435,235,85,ACC)
arrow(337,477,275,477);tx('linked to',282,451,7.6,color=MUTED)
rect(40,550,532,77,fill=PALE)
p('What this record lets you study',53,561,502,12,'SpaceBold',leading=15)
p('The analysis can follow which answer responds to which question, the topic under discussion, and how the exchange develops. An event sequence retains context that a total speaking-time measure loses.',53,585,502,9.7,leading=13)
note('The episode is an actual excerpt from the supplied draft; the lower diagram explains the coding fields without inventing values. Re-export the original timeline with larger vector labels for final publication.','Upper image: supplied Fig. 1, panel B (draft). Lower image: new conceptual reading guide to the same coding structure. The draft illustration is not presented as a validated finding.')
#7 double
base(7,'F / Current page 8','Two forms of compression','Show why producing plausible individual outputs is different from preserving diversity across a collection.')
tx('CONCEPTUAL ILLUSTRATION / NOT EMPIRICAL DATA',40,185,8,color=ACC)
rect(40,211,532,174);tx('GENERATION',53,222,8,color=ACC)
p('Breadth of candidate ideas',53,240,235,14,'SpaceBold',leading=17)
p('Similar territory; uneven concentration',322,240,237,12,'SpaceBold',leading=15)
tx('Human proposals / schematic',53,272,8,color=BLUE);tx('AI proposals / schematic',322,272,8,color=ACC)
# Scatter shapes without axes/data
left=[(65,299),(95,284),(128,309),(160,290),(202,305),(242,282),(74,348),(119,354),(155,337),(209,350),(257,333),(180,363)]
right=[(352,298),(363,307),(375,296),(370,318),(387,310),(443,338),(455,346),(449,328),(465,333),(479,343),(509,291),(530,359)]
for points,col in [(left,BLUE),(right,ACC)]:
 for x,y in points:c.setFillColor(HexColor(col));c.circle(x,H-y-8,4.2,fill=1,stroke=0)
tx('vs.',286,318,9,color=MUTED)
rect(40,409,532,168);tx('EVALUATION',53,420,8,color=ACC)
p('Different reasons to question an idea',53,438,246,12,'SpaceBold',leading=15)
p('More similar evaluative perspectives',322,438,236,12,'SpaceBold',leading=15)
tx('Human reviews / schematic',53,462,8,color=BLUE);tx('AI reviews / schematic',322,462,8,color=ACC)
for i in range(3):
 x=55+i*74;rect(x,477,61,76,fill='#ffffff');
 for j,L in enumerate([[38,25,43],[22,41,29],[42,29,19]][i]):line(x+9,497+j*13,x+9+L,497+j*13,BLUE,width=2)
for i in range(3):
 x=330+i*74;rect(x,477,61,76,fill='#ffffff')
 for j,L in enumerate([38,31,38]):line(x+9,497+j*13,x+9+L,497+j*13,ACC,width=2)
tx('vs.',286,506,9,color=MUTED)
p('<b>The two stages differ.</b> Generation can underrepresent distinctive possibilities. Evaluation can converge in judgment even when reviews cover much of the same semantic territory.',40,601,532,10.5,leading=14)
note('Place alongside the findings, with the computational design and limitations kept in full. If validated result figures are supplied later, a measured plot can replace this schematic. Avoid fabricated percentages or axes.','New explanatory schematic based on the portfolio\'s working-manuscript account of Double Compression. Dots and marks are symbolic; they are not the study observations or estimated effect sizes.')
#8 influence
base(8,'G / Current page 9','Participation and decision authority','A compact diagram makes the distinction between contributing information and controlling a consequential decision visible.')
card('Report an experience','A person supplies context and describes harm.',40,211,152,100,GREEN)
card('Classify the experience','A system or platform decides which category applies.',230,211,152,100,ACC)
card('Choose a response','Available actions shape what can happen next.',420,211,152,100,BLUE)
arrow(192,260,230,260);arrow(382,260,420,260)
number(1,116,345);number(2,306,345);number(3,496,345)
p('Who is heard?',50,370,132,12,'SpaceBold',leading=15);p('Whose experiences and risks inform the design?',50,399,132,10,leading=14)
p('Who defines?',240,370,132,12,'SpaceBold',leading=15);p('Whose definitions count as harm? Can people contest them?',240,399,132,10,leading=14)
p('Who can act?',430,370,132,12,'SpaceBold',leading=15);p('Who selects the response, and what choices are available?',430,399,132,10,leading=14)
rect(40,481,532,112,fill=PALE)
p('The connection to collective AI',54,494,504,14,'SpaceBold',leading=18)
p('The same distinction appears when mentors revise an expert model, teams interpret behavioral measurements, or evaluators shape which scientific ideas receive support. These are connections across the research program, not outcomes all tested in the harassment review.',54,526,504,10,leading=14)
p('A small decision-flow is more informative here than a generic shield, warning symbol, or AI icon.',40,618,532,10,'News',leading=14)
note('Add this as a half-page figure beside the review findings. Retain the distinction between documented reporting gaps and demonstrated system failures. The diagram summarizes an analytic question, not every tool in the review.','New conceptual diagram based on Huang et al. (2024), Opportunities, Tensions, and Challenges in Computational Approaches to Addressing Online Harassment. doi:10.1145/3643834.3661623.')
c.save();print(OUT)
