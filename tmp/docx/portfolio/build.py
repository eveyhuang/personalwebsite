from pathlib import Path
from io import BytesIO
from html.parser import HTMLParser
import sys,zipfile,uuid
from lxml import etree
from PIL import Image
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.section import WD_SECTION,WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH,WD_BREAK,WD_LINE_SPACING,WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'tmp/pdfs/statement-alignment'))
from content import INTRO,PAGES
OUT=ROOT/'output/docx/Evey_Huang_Research_Portfolio.docx'
D=Document();D.core_properties.title='Evey Huang Research Portfolio';D.core_properties.author='Evey Huang'
SANS='Space Grotesk Light';SERIF='Newsreader 16pt';INK='17181B';MUTED='595D65';ACC='A65F50'
for name in ['Normal','Title','Heading 1','Heading 2','Subtitle','Caption','Header','Footer']:
 s=D.styles[name];s.font.name=SANS;s.font.color.rgb=RGBColor.from_string(INK)
 s.font.size=Pt(10.3);s.paragraph_format.space_after=Pt(8)
 s.paragraph_format.line_spacing=1.24
D.styles['Normal'].paragraph_format.widow_control=True
for name in ['Heading 1','Heading 2','Subtitle']:
 D.styles[name].paragraph_format.keep_with_next=True
D.styles['Heading 1'].font.size=Pt(25);D.styles['Heading 1'].font.bold=True
D.styles['Heading 2'].font.size=Pt(12.3);D.styles['Heading 2'].font.bold=True
D.styles['Heading 2'].paragraph_format.space_before=Pt(5)
D.styles['Heading 2'].paragraph_format.space_after=Pt(5)
D.styles['Subtitle'].font.name=SERIF;D.styles['Subtitle'].font.size=Pt(16);D.styles['Subtitle'].font.italic=False
D.styles['Subtitle'].paragraph_format.line_spacing=1.16;D.styles['Subtitle'].paragraph_format.space_after=Pt(16)
D.styles['Title'].font.size=Pt(28);D.styles['Title'].font.color.rgb=RGBColor.from_string(ACC)
bg=OxmlElement('w:background');bg.set(qn('w:color'),'F6F6F3');D._element.insert(0,bg)
setting=OxmlElement('w:displayBackgroundShape');D.settings._element.append(setting)
emb=OxmlElement('w:embedTrueTypeFonts');D.settings._element.append(emb)

def border(p,where='bottom'):
 pp=p._p.get_or_add_pPr();b=OxmlElement('w:pBdr');e=OxmlElement('w:'+where);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:space'),'8');e.set(qn('w:color'),'C9CAC5');b.append(e);pp.append(b)
def field(p,name):
 r=p.add_run();f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),name);rr=OxmlElement('w:r');t=OxmlElement('w:t');t.text='1';rr.append(t);f.append(rr);p._p.append(f)
def setup(s,land=False):
 s.page_width=Inches(11 if land else 8.5);s.page_height=Inches(8.5 if land else 11);s.orientation=WD_ORIENT.LANDSCAPE if land else WD_ORIENT.PORTRAIT
 s.left_margin=s.right_margin=Pt(44);s.top_margin=Pt(67 if not land else 53);s.bottom_margin=Pt(48)
 s.header_distance=Pt(24);s.footer_distance=Pt(23)
 s.header.is_linked_to_previous=False;s.footer.is_linked_to_previous=False
 h=s.header.paragraphs[0];h.paragraph_format.space_after=Pt(0);h.paragraph_format.tab_stops.add_tab_stop(s.page_width-Pt(88),WD_TAB_ALIGNMENT.RIGHT)
 r=h.add_run('EVEY HUANG');r.font.size=Pt(8);r.font.color.rgb=RGBColor.from_string(ACC)
 r=h.add_run('\tHUMAN-AI COLLABORATION');r.font.size=Pt(7.5);r.font.color.rgb=RGBColor.from_string(MUTED);border(h)
 f=s.footer.paragraphs[0];f.paragraph_format.tab_stops.add_tab_stop(s.page_width-Pt(88),WD_TAB_ALIGNMENT.RIGHT)
 f.add_run('eveyhuang.com\t');field(f,'PAGE');f.add_run(' / ');field(f,'NUMPAGES');border(f,'top')
 for r in f.runs:r.font.size=Pt(8);r.font.color.rgb=RGBColor.from_string(MUTED)

def linkrun(p,txt,url,bold=False):
 hyperlink=OxmlElement('w:hyperlink');hyperlink.set(qn('r:id'),p.part.relate_to(url,RT.HYPERLINK,is_external=True))
 r=OxmlElement('w:r');pr=OxmlElement('w:rPr');co=OxmlElement('w:color');co.set(qn('w:val'),MUTED);pr.append(co)
 if bold:pr.append(OxmlElement('w:b'))
 r.append(pr);t=OxmlElement('w:t');t.set(qn('xml:space'),'preserve');t.text=txt;r.append(t);hyperlink.append(r);p._p.append(hyperlink)
class Rich(HTMLParser):
 def __init__(self,p):super().__init__();self.p=p;self.bold=False;self.url=None
 def handle_starttag(self,t,a):
  if t=='b':self.bold=True
  if t=='link':self.url=dict(a).get('href')
  if t=='br':self.p.add_run().add_break()
 def handle_endtag(self,t):
  if t=='b':self.bold=False
  if t=='link':self.url=None
 def handle_data(self,s):
  s=s.replace('–','-').replace('—','-').replace('‑','-')
  if self.url:linkrun(self.p,s,self.url,self.bold)
  else:
   r=self.p.add_run(s)
   if self.bold:r.bold=True

def paragraph(s,style=None,size=None):
 p=D.add_paragraph(style=style);Rich(p).feed(s)
 if size:
  for r in p.runs:r.font.size=Pt(size)
  for r in p._p.xpath('./w:hyperlink/w:r'):
   rp=r.find(qn('w:rPr'))
   sz=OxmlElement('w:sz');sz.set(qn('w:val'),str(round(size*2)));rp.append(sz)
  p.paragraph_format.line_spacing=Pt(size*1.31)
 return p

def reference(rs):
 if not rs:return
 p=paragraph('REFERENCES',size=7);p.paragraph_format.space_before=Pt(12);p.paragraph_format.space_after=Pt(6);p.paragraph_format.keep_with_next=True
 for t in rs:
  p=paragraph(t,size=7.5);p.paragraph_format.line_spacing=Pt(9.5);p.paragraph_format.space_after=Pt(4)
  for r in p.runs:r.font.color.rgb=RGBColor.from_string(MUTED)

def image(path,w,alt):
 p=D.add_paragraph();p.paragraph_format.line_spacing=1.0;p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_after=Pt(6);p.paragraph_format.keep_with_next=True
 sh=p.add_run().add_picture(str(path),width=Pt(w));sh._inline.docPr.set('descr',alt);return p

def caption(t):
 p=paragraph(t,'Caption',8);p.paragraph_format.line_spacing=Pt(10);p.paragraph_format.space_after=Pt(8)
 for r in p.runs:r.italic=False;r.font.color.rgb=RGBColor.from_string(MUTED)

def newpage(land=False):
 s=D.add_section(WD_SECTION.NEW_PAGE);setup(s,land)
 # The section-boundary paragraph is structural, not an extra blank line.
 p=D.paragraphs[-1];p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=Pt(1)
 for r in p.runs:r.font.size=Pt(1)

setup(D.sections[0])
paragraph('RESEARCH PORTFOLIO',size=8).runs[0].font.color.rgb=RGBColor.from_string(ACC)
# The two-cell title block preserves the portfolio's side-by-side portrait layout.
t=D.add_table(rows=1,cols=2);t.autofit=False;t.columns[0].width=Pt(380);t.columns[1].width=Pt(144)
for cell in t.rows[0].cells:
 tcPr=cell._tc.get_or_add_tcPr();bd=OxmlElement('w:tcBorders')
 for side in ['top','left','bottom','right']:
  el=OxmlElement('w:'+side);el.set(qn('w:val'),'nil');bd.append(el)
 tcPr.append(bd)
p=t.cell(0,0).paragraphs[0];p.style=D.styles['Title'];p.add_run('Evey Huang, PhD.');p.paragraph_format.space_before=Pt(18)
p=t.cell(0,0).add_paragraph('Research Assistant Professor\nKellogg School of Management\nNorthwestern University');p.paragraph_format.line_spacing=1.4
im=Image.open(ROOT/'src/assets/evey-profile.png').convert('RGB');im.thumbnail((650,650));b=BytesIO();im.save(b,format='JPEG',quality=92);b.seek(0)
p=t.cell(0,1).paragraphs[0];p.paragraph_format.line_spacing=1.0;p.alignment=WD_ALIGN_PARAGRAPH.RIGHT;sh=p.add_run().add_picture(b,width=Pt(130));sh._inline.docPr.set('descr','Portrait of Evey Huang')
# Crop geometry is an editable picture-format setting, not flattened page artwork.
shape=sh._inline.xpath('.//a:prstGeom')
if shape:shape[0].set('prst','ellipse')
p=paragraph('Human-AI collaboration in teams and organizations','Subtitle',25);p.paragraph_format.space_before=Pt(32);p.paragraph_format.space_after=Pt(20)
for _,s in INTRO:paragraph(s,size=10.5)
p=paragraph('<link href="mailto:jiaxinh.evey@gmail.com">jiaxinh.evey@gmail.com</link> / <link href="https://www.eveyhuang.com/">eveyhuang.com</link>',size=10);p.paragraph_format.space_before=Pt(25)
SIZES={3:9.9,4:9.5,5:9.4,6:10,9:9.3,12:10.2}
for n,label,kicker,title,lead,sections,refs,vis in PAGES:
 newpage(vis=='pitch')
 if vis=='pitch':
  p=image('/Users/eveyhuang/Documents/NICO/Org_Sci-Entrepreneurial_Pitching/docs/figures/fig 1.png',659,'Entrepreneurship pitching annotation pipeline, episode timeline, concept bottleneck model, and results')
  p.paragraph_format.space_after=Pt(1)
  caption('Entrepreneurship pitching [5]: annotation, interaction records, and concept bottleneck analysis. Full project discussion on page 10.')
  continue
 p=paragraph(kicker,size=8);p.paragraph_format.space_after=Pt(9);p.paragraph_format.keep_with_next=True;p.runs[0].font.color.rgb=RGBColor.from_string(ACC)
 paragraph(title,'Heading 1');paragraph(lead,'Subtitle')
 for h,s in sections:
  if h:paragraph(h,'Heading 2')
  paragraph(s,size=SIZES.get(n,10.3))
 if vis=='coaching':
  image('/Users/eveyhuang/Desktop/flow.png',524,'Coaching workflow connecting the expert model, chatbot, novice reflection, dashboard, mentor preparation, and model revision')
  caption('Coaching workflow [2]. Novices reflect and prioritize risks; mentors review the resulting context, prepare assistance, and revise the expert model guiding the system.')
 reference(refs)
# Clear template theme overrides and title borders; use deliberate line metrics.
for style in D.styles:
 for node in style.element.xpath('.//w:pBdr'):
  node.getparent().remove(node)
 if style.name in ['Normal','Title','Heading 1','Heading 2','Subtitle','Caption','Header','Footer']:
  family=SERIF if style.name=='Subtitle' else SANS
  rf=style.element.get_or_add_rPr().get_or_add_rFonts()
  for a in list(rf.attrib):
   if 'Theme' in a:del rf.attrib[a]
  for a in ['ascii','hAnsi','cs','eastAsia']:rf.set(qn('w:'+a),family)
  style.paragraph_format.line_spacing=Pt({'Title':33,'Heading 1':28,'Heading 2':15,'Subtitle':19,'Header':10,'Footer':10,'Caption':10}.get(style.name,13.5))
for sec in D.sections:
 for p in [sec.header.paragraphs[0],sec.footer.paragraphs[0]]:
  p.paragraph_format.tab_stops.clear_all()
  p.paragraph_format.tab_stops.add_tab_stop(sec.page_width-Pt(88),WD_TAB_ALIGNMENT.RIGHT)
D.save(OUT)
# Embed the exact fonts so the document retains its visual style in Word.
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with zipfile.ZipFile(OUT) as z:parts={x:z.read(x) for x in z.namelist()}
ft=etree.fromstring(parts['word/fontTable.xml']);relpath='word/_rels/fontTable.xml.rels';rels=etree.fromstring(parts[relpath]) if relpath in parts else etree.Element('Relationships',nsmap={None:'http://schemas.openxmlformats.org/package/2006/relationships'})
for i,(family,style,fname) in enumerate([(SANS,'embedRegular','Space'),(SANS,'embedBold','SpaceBold'),(SERIF,'embedRegular','News')]):
 found=ft.xpath('w:font[@w:name=$name]',namespaces=ns,name=family)
 font=found[0] if found else etree.SubElement(ft,qn('w:font'),{qn('w:name'):family})
 guid=uuid.uuid4();key=guid.bytes[::-1];data=bytearray((ROOT/'tmp/pdfs/fonts'/f'{fname}-static.ttf').read_bytes())
 for j in range(32):data[j]^=key[j%16]
 filename=f'font{i}.odttf';parts['word/fonts/'+filename]=bytes(data);rid='rIdEmbed'+str(i)
 etree.SubElement(font,qn('w:'+style),{qn('r:id'):rid,qn('w:fontKey'):'{'+str(guid).upper()+'}'})
 etree.SubElement(rels,'{http://schemas.openxmlformats.org/package/2006/relationships}Relationship',Id=rid,Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/font',Target='fonts/'+filename)
parts['word/fontTable.xml']=etree.tostring(ft,xml_declaration=True,encoding='UTF-8',standalone=True);parts[relpath]=etree.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
ct=etree.fromstring(parts['[Content_Types].xml']);etree.SubElement(ct,'{http://schemas.openxmlformats.org/package/2006/content-types}Default',Extension='odttf',ContentType='application/vnd.openxmlformats-officedocument.obfuscatedFont');parts['[Content_Types].xml']=etree.tostring(ct,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
 for n,data in parts.items():z.writestr(n,data)
print(OUT)
