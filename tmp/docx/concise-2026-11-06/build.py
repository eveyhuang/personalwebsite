from pathlib import Path
from copy import deepcopy as cp
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import re,json,hashlib,sys
sys.path.insert(0,str(Path(__file__).parent))
from content import *
ROOT=Path.cwd();TMP=Path(__file__).parent;SRC=TMP/'user-edited-source.docx';OUT=ROOT/'output/docx/Evey_Huang_Research_Portfolio_Revised.docx'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships';NS={'w':W,'r':R}
def q(t):return '{'+W+'}'+t
def el(t,**attrs):return E.Element(q(t),{q(k):str(v) for k,v in attrs.items()})
def txt(e):return ''.join(e.xpath('.//w:t/text()',namespaces=NS))
with ZipFile(SRC) as z:parts={n:z.read(n) for n in z.namelist()}
root=E.fromstring(parts['word/document.xml']);body=root.find(q('body'));orig=list(body)
sections=root.xpath('//w:sectPr',namespaces=NS);portrait=cp(sections[1]);landscape=cp(sections[10])
refs={}
for p in root.xpath('//w:body/w:p',namespaces=NS):
 m=re.match(r'^\[(\d+)\]',txt(p))
 if m:refs[int(m.group(1))]=cp(p)
assert set(refs)==set(range(1,17))
# Keep the user's first page, including its paragraph/run formatting and title table.
for node in orig[12:]:body.remove(node)
INK='17181B';MUTED='595D65';RED='A65F50';BLUE='607B91';GREEN='688477';GRAY='73757C'

def rp(size=10.5,bold=False,color=INK):
 r=el('rPr');r.append(el('rFonts',ascii='Campton Bold' if bold else 'Campton Light',hAnsi='Campton Bold' if bold else 'Campton Light',eastAsia='Campton Light',cs='Campton Light'))
 r.append(el('sz',val=round(size*2)));r.append(el('szCs',val=round(size*2)));r.append(el('color',val=color))
 if bold:r.append(el('b'))
 return r

def run(text,size=10.5,bold=False,color=INK):
 r=el('r');r.append(rp(size,bold,color));t=el('t');t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=text;r.append(t);return r

def para(text='',size=10.5,bold=False,color=INK,before=0,after=8,line=None,style='Normal',keep=False):
 p=el('p');pp=el('pPr');pp.append(el('pStyle',val=style));pp.append(el('spacing',before=round(before*20),after=round(after*20),line=round((line or size*1.32)*20),lineRule='exact'));pp.append(el('widowControl'))
 if keep:pp.append(el('keepNext'))
 p.append(pp);p.append(run(text,size,bold,color));return p

def add(p):body.append(p);return p

def title(kicker,name,color=RED):
 add(para(kicker,8,color=color,after=11,keep=True));add(para(name,23,bold=True,line=27,after=14,style='Heading1',keep=True))

def intro(s):add(para(s,10.5,after=15))

def blocks(items,size=10.5):
 for h,s in items:
  add(para(h,11.5,bold=True,before=3,after=5,keep=True,style='Heading2'))
  add(para(s,size,after=10))

def reference(ids):
 add(para('REFERENCES',7,color=MUTED,before=10,after=5,keep=True))
 for i in ids:
  p=cp(refs[i]);pp=p.find(q('pPr'))
  if pp is None:pp=el('pPr');p.insert(0,pp)
  for x in list(pp):
   if x.tag in [q('spacing'),q('keepNext'),q('pageBreakBefore'),q('sectPr')]:pp.remove(x)
  pp.append(el('spacing',after=55,line=175,lineRule='exact'))
  for r in p.xpath('.//w:r',namespaces=NS):
   old=r.find(q('rPr'))
   if old is not None:r.remove(old)
   r.insert(0,rp(7.5,False,MUTED))
  body.append(p)

def pagebreak():
 p=para('',1,after=0,line=1);p.find(q('pPr')).append(cp(portrait));body.append(p)

def image_source(which):
 # Reuse the existing picture element and relationship, retaining replaceable images.
 for p in orig:
  drawings=p.xpath('.//w:drawing',namespaces=NS)
  if not drawings:continue
  desc=' '.join(p.xpath('.//*[local-name()="docPr"]/@descr'))
  if which in desc:
   v=cp(p);pp=v.find(q('pPr'))
   if pp is None:pp=el('pPr');v.insert(0,pp)
   for n in list(pp):
    if n.tag in [q('spacing'),q('keepNext')]:pp.remove(n)
   pp.append(el('spacing',before=0,after=70,line=240,lineRule='auto'));pp.append(el('keepNext'));return v
 if which=='Entrepreneurship pitching':
  from docx import Document
  from docx.shared import Pt
  temp=Document();p=temp.add_paragraph();p.paragraph_format.line_spacing=1.0
  path='/Users/eveyhuang/Documents/NICO/Org_Sci-Entrepreneurial_Pitching/docs/figures/fig 1.png'
  shape=p.add_run().add_picture(path,width=Pt(659));shape._inline.docPr.set('descr','Entrepreneurship pitching pipeline and concept bottleneck analysis');shape._inline.docPr.set('id','900')
  rels=E.fromstring(parts['word/_rels/document.xml.rels']);rid='rIdPitchFigureRestored'
  E.SubElement(rels,'{http://schemas.openxmlformats.org/package/2006/relationships}Relationship',Id=rid,Type=R+'/image',Target='media/pitch-pipeline.png')
  parts['word/_rels/document.xml.rels']=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
  parts['word/media/pitch-pipeline.png']=Path(path).read_bytes()
  node=cp(p._p)
  for blip in node.xpath('.//*[local-name()="blip"]'):blip.set('{'+R+'}embed',rid)
  return node
 raise ValueError(which)

# Page 2: compact, fully editable visual index.
title('RESEARCH OVERVIEW','How AI changes collective work')
intro('Three connected questions organize the research: how people learn, what organizations can observe, and how they make judgments.')
table=el('tbl');pr=el('tblPr');pr.append(el('tblW',w=10480,type='dxa'));pr.append(el('tblLayout',type='fixed'));borders=el('tblBorders')
for side in ['top','left','bottom','right','insideH','insideV']:borders.append(el(side,val='nil'))
pr.append(borders);table.append(pr);grid=el('tblGrid');grid.append(el('gridCol',w=850));grid.append(el('gridCol',w=9630));table.append(grid)
rows=[('01',RED,'F1E7E3','How people learn','Coaching model → AI coaching system   /   p. 3','Collaboration skills and learning environments   /   p. 4'),('02',BLUE,'E7EDF2','What organizations can observe','Multimodal measurement across science, pitching, and sport   /   p. 5','Full entrepreneurship pipeline figure   /   p. 9'),('03',GREEN,'E8EEE9','How organizations make judgments','Diversity in scientific ideas and reviews   /   p. 6','AI as a participant in generation and evaluation')]
for number,col,fill,heading,l1,l2 in rows:
 tr=el('tr');trpr=el('trPr');trpr.append(el('cantSplit'));tr.append(trpr)
 for k in range(2):
  tc=el('tc');tcp=el('tcPr');tcp.append(el('tcW',w=850 if k==0 else 9630,type='dxa'));tcp.append(el('shd',fill=col if k==0 else fill));mar=el('tcMar')
  for side in ['top','bottom','left','right']:mar.append(el(side,w=190 if side in ['top','bottom'] else 150,type='dxa'))
  tcp.append(mar);tcp.append(el('vAlign',val='center'));tc.append(tcp)
  if k==0:tc.append(para(number,15,bold=True,color='FFFFFF',after=0))
  else:
   tc.append(para(heading,15,bold=True,color=col,after=9));tc.append(para(l1,10.5,after=5));tc.append(para(l2,10,after=0,color=MUTED))
  tr.append(tc)
 table.append(tr)
 # Thin whitespace separator, within a single editable matrix.
 tr=el('tr')
 for width in [850,9630]:
  tc=el('tc');pp=el('tcPr');pp.append(el('tcW',w=width,type='dxa'));tc.append(pp);tc.append(para('',1,line=10,after=0));tr.append(tc)
 table.append(tr)
add(table)
add(para('OTHER PROJECTS',8,color=GRAY,before=18,after=7,keep=True))
add(para('Literary style · Online harassment · Emoji recommendations',11.5,bold=True,after=5));add(para('Related work on judgment, influence, and context   /   p. 7',10,color=MUTED,after=16))
add(para('RESEARCH AND APPLIED EXPERIENCE',8,color=GRAY,after=7,keep=True));add(para('Northwestern · Novohaven · Education and field partnerships   /   p. 8',10.5,after=15))
add(para('Across these projects, AI is a phenomenon to study, an intervention to design, and an instrument for measuring collective work.',10.5,color=MUTED,before=10))
pagebreak()
# Page 3: coaching trajectory and original flow figure.
title('01 / HOW PEOPLE LEARN','From coaching expertise to AI support')
intro(COACH_INTRO);blocks(COACH,10.5)
add(image_source('Coaching workflow'))
add(para('The system connects novice reflection, mentor preparation, and revision of the expert model. [2]',8,color=MUTED,after=9))
add(para(DISSERTATION,9.5,after=6));reference([1,2,16]);pagebreak()
# Page 4: one paragraph per related publication.
title('01 / HOW PEOPLE LEARN','Learning to collaborate')
intro(LEARNING_INTRO);blocks(LEARNING,10.5);reference([8,11,13,14]);pagebreak()
# Page 5: all multimodal study descriptions together.
title('02 / WHAT ORGANIZATIONS CAN OBSERVE','Measuring interaction with multimodal AI',BLUE)
intro(MULTI_INTRO);blocks(MULTI,10);reference([3,4,15,5,6]);pagebreak()
# Page 6: short scientific AI theme, with no research-agenda filler.
title('03 / HOW ORGANIZATIONS MAKE JUDGMENTS','AI and scientific knowledge production',GREEN)
intro(JUDGMENT_INTRO);blocks(JUDGMENT,11)
reference([7]);pagebreak()
# Page 7: all requested other projects.
title('RELATED RESEARCH','Other projects',GRAY)
intro(OTHER_INTRO);blocks(OTHER,10.5);reference([9,10,12]);pagebreak()
# Page 8: applied workflow has one paragraph; personal experience stays concise.
title('RESEARCH AND APPLIED EXPERIENCE','Research, design, and practice')
intro(EXPERIENCE_INTRO);blocks(EXPERIENCE,10.5)
add(para('Outside work, I play guitar and tennis, take film and digital photographs, read, doodle, and cook spicy food.',10.5,before=5))
add(para('jiaxinh.evey@gmail.com   /   eveyhuang.com',10.5,color=MUTED,before=8));pagebreak()
# Page 9: retain the full-resolution supplied figure.
add(image_source('Entrepreneurship pitching'))
add(para('Entrepreneurship pitching [5]: annotation, interaction records, and concept bottleneck analysis. Project summary on page 5.',8,color=MUTED,after=0))
body.append(cp(landscape))
# All other source parts remain byte-identical except settings and font repair in page furniture.
parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
settings=E.fromstring(parts['word/settings.xml']);uf=settings.find(q('updateFields'))
if uf is None:uf=el('updateFields');settings.append(uf)
uf.set(q('val'),'true');parts['word/settings.xml']=E.tostring(settings,xml_declaration=True,encoding='UTF-8',standalone=True)
# The source's inherited header font renders blank; apply the user's Campton choice there too.
for name in list(parts):
 if re.match(r'word/(header|footer)\d+\.xml$',name):
  x=E.fromstring(parts[name])
  for r in x.xpath('//w:r',namespaces=NS):
   pr=r.find(q('rPr'))
   if pr is None:pr=el('rPr');r.insert(0,pr)
   f=pr.find(q('rFonts'))
   if f is None:f=el('rFonts');pr.insert(0,f)
   for a in list(f.attrib):
    if 'Theme' in a:del f.attrib[a]
   for a in ['ascii','hAnsi','cs','eastAsia']:f.set(q(a),'Campton Light')
  parts[name]=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(OUT,'w',ZIP_DEFLATED) as z:
 for n,b in parts.items():z.writestr(n,b)
print(OUT)
# Evidence of exact preservation of the user's page-one body.
with ZipFile(SRC) as z:source=E.fromstring(z.read('word/document.xml'))
assert all(E.tostring(a)==E.tostring(b) for a,b in zip(list(source.find(q('body')))[:12],list(body)[:12]))
print('User first-page body: unchanged XML. Reference numbering: 1–16 retained.')
