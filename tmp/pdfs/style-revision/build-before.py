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
 text(label.upper(),246,762,7,color=MUTED);text(f'{n:02d} / 10',W-80,761,8,color=MUTED)
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


def body(sections,y=220,size=10.3,limit=728):
 def height(sz):
  h=0
  for title,content in sections:
   if title:
    p=Paragraph(title,ParagraphStyle('t',fontName='SpaceBold',fontSize=12.5,leading=15));h+=p.wrap(CW,700)[1]+5
   p=Paragraph(content,ParagraphStyle('b',fontName='Space',fontSize=sz,leading=sz*1.29));h+=p.wrap(CW,700)[1]+11
  return h
 while y+height(size)>limit and size>9.5:size-=.1
 assert y+height(size)<=limit,('body overflow',y+height(size))
 for title,content in sections:
  if title:y=para(title,M,y,CW,12.5,'SpaceBold',leading=15)+5
  y=para(content,M,y,CW,size,leading=size*1.29)+11
 return y

def page(n,label,kicker,title,lead,sections,reference=None,asset=None):
 base(n,label)
 y=heading(kicker,title)+15
 if asset:
  img(ROOT/'public'/asset,438,y,130,124)
  ly=para(lead,M,y,370,18,'News',leading=22)
  y=max(ly+18,y+132)
 else:
  y=para(lead,M,y,CW,18,'News',leading=23)+23
 y=body(sections,y,limit=655 if reference and len(reference)>1 else 669 if reference else 728)
 if reference:
  assert y<675,('no room for references',n,y)
  refs(reference,max(y+3,675 if len(reference)==1 else 645))
 c.showPage()
base(1,'Introduction')
text('hi.',M,76,76,'SpaceBold')
c.saveState();path=c.beginPath();path.circle(476,H-162,70);c.clipPath(path,stroke=0,fill=0)
im=Image.open(ROOT/'src/assets/evey-profile.png');iw,ih=im.size;scale=max(140/iw,140/ih);c.drawImage(raster(im,iw*scale,ih*scale),406-(iw*scale-140)/2,H-232-(ih*scale-140)/2,iw*scale,ih*scale,mask='auto');c.restoreState()
text('Evey Huang, PhD.',M,183,24,'SpaceBold',ACC)
para('Research Assistant Professor<br/>Kellogg School of Management, Northwestern University',M,222,340,10.2,leading=15)
para('Human-AI collaboration in teams and organizations',M,287,CW,27,'News',leading=31)
body([
('', 'I study human-AI collaboration where the human is part of a team or organization, working with others to tackle complex problems in science, entrepreneurship, and knowledge work. Most AI systems are designed around an individual user: helping one person generate an idea, make a decision, or complete a task. Yet the most challenging work is collective. People bring different knowledge and perspectives, build on and challenge one another\'s inputs, and coordinate interdependent actions.'),
('', 'My research asks how AI changes the way people work together and how we can design it to support collective work. I investigate how AI can make tacit and distributed expertise available in collaboration; how multimodal AI can make collaboration processes observable at scale; and how AI reshapes the ideas and judgments groups produce.'),
('', 'I bring methods from human-computer interaction, design, and computational social science to organizational questions. Close observation identifies work that is difficult to articulate. Computational analysis reveals patterns at scale. System design allows me to intervene in those processes and study how people use the resulting support in practice.'),
('', 'The projects that follow connect long-term field partnerships with coaches and entrepreneurs, AI system design and exploratory deployment, behavioral data from real teams, and computational studies of scientific knowledge production. Together, they examine AI\'s value through the collaboration and collective outcomes it enables.')
],370,10.5)
rule(694);para('<link href="mailto:jiaxinh.evey@gmail.com">jiaxinh.evey@gmail.com</link>  /  <link href="https://www.eveyhuang.com/">eveyhuang.com</link>',M,708,CW,10)
c.showPage()
page(2,'Research overview','RESEARCH OVERVIEW','AI in collective work',
'What changes when the unit of value is a collaboration, a team, or a collection of ideas rather than a single AI output?',[
('01 / Making expertise usable', 'People do not automatically benefit from the expertise distributed around them. They must recognize what is relevant, locate who knows it, articulate requests, and translate experience across different problems. My coaching research identifies the practices that make this possible and uses an empirical model of those practices to guide AI behavior. The resulting system prepares novices and mentors differently for a shared conversation, while allowing mentors to revise the knowledge guiding the AI. Related work examines collaboration skills and representations of tacit judgment. <b>Pages 3-5.</b>'),
('02 / Understanding collaboration', 'Organizational processes such as coordination and knowledge integration unfold through interaction, but continuous observation in real work settings is expensive. I develop a methodological agenda for using language, audio, and visible behavior to study these processes at greater scale and temporal resolution. Ongoing studies in scientific teams, entrepreneur-investor exchanges, and professional volleyball examine what people do with one another\'s contributions and how interaction relates to outcomes. Measurement validity is an empirical requirement for each construct and setting. <b>Pages 6-7.</b>'),
('03 / AI and collective outcomes', 'An individually plausible AI contribution may still narrow the range of ideas or judgments available to a group. My work on scientific proposals and reviews treats collections of outputs as the unit of analysis, distinguishing compression in idea generation from compression in evaluation. Earlier research on harassment tools adds a complementary question: does supplying information give people influence over how it is interpreted and acted upon? <b>Pages 8-9.</b>'),
('What connects the streams', 'These projects examine different levels of collective work: preparing a conversation, tracing an unfolding interaction, and evaluating the distribution of ideas and decisions. They also connect questions of capability with questions of authority. Who defines the expertise encoded in a system? Who can contest a behavioral measurement? Whose perspectives survive a shared evaluation process?'),
('', 'The studies provide complementary foundations for designing AI support. The coaching work shows how empirical knowledge of human practice can guide an intervention. The team research develops ways to observe collaboration. The collective-outcomes work establishes why the consequences of shared AI support must be assessed beyond individual productivity. The portfolio closes with my research and applied experience. <b>Page 10.</b>')])
page(3,'Coaching expertise','STREAM 01 / EMPIRICAL FOUNDATION','Making expertise usable',
'How do mentors turn separate experiences into a resource that a learning community can actually use?',[
('The setting and problem', 'In a university incubator, a coach simultaneously supported novice entrepreneurs working on different ventures, at different stages, with no single correct solution. These novices were not necessarily members of the same venture team. Even when useful experience existed in the community, novices struggled to recognize its relevance, find the right person, formulate a request, or adapt advice from another project to their own.'),
('What we studied', 'My coauthors and I analyzed 24 virtual coaching sessions involving three coaches and 30 novices, supplemented by retrospective coach interviews and observations of Slack communication. The recordings covered 14 hours across eight weeks. We asked what challenges novices encountered, which strategies coaches used, and how supporting several people with different problems shaped the work of coaching.'),
('What the model captures', 'Coaches supported reasoning by questioning assumptions, identifying missing evidence, and helping novices plan actions to resolve uncertainty. They translated project-specific accounts into transferable lessons about methods and processes. They remembered who had relevant experience, connected novices to those peers, retold useful examples, and helped articulate what assistance was needed and why.'),
('', 'Coaches also organized the conditions for learning. Supportive peer testing, normalizing setbacks, and reframing unexpected results helped novices experiment. Public commitments and progress updates created accountability, but visible behavior could also spread weak norms when vague goals or low effort went uncorrected. The barriers to learning were therefore relational and emotional as well as informational.'),
('Contribution and scope', 'The resulting cognitive model explains the interactional work required to make distributed expertise usable. It provides an empirical foundation for intelligent coaching systems; this paper itself did not deploy an LLM system. The qualitative findings describe one incubator and do not causally establish improved venture performance or psychological safety. Accounts of novice challenges came primarily from observation and coaches\' interpretations rather than novice interviews.')],
['[1] Huang, E., Rees Lewis, D., Gaudani, S., Easterday, M., &amp; Gerber, E. (2023). Intelligent Coaching Systems: Understanding One-to-many Coaching for Ill-defined Problem Solving. Proceedings of the ACM on Human-Computer Interaction, 7(CSCW1). <link href="https://doi.org/10.1145/3579614">doi:10.1145/3579614</link>.'])
page(4,'AI coaching system','STREAM 01 / DESIGN AND FIELD DEPLOYMENT','AI that helps us help each other',
'Using an empirical model of coaching expertise to prepare both sides of a human relationship.',[
('From an empirical model to a system', 'I translated the coaching model into a proactive AI system for mentor-novice meetings. The system combines an LLM with explicit project and risk models, a reflective chatbot, dashboards, and an interface through which mentors can revise the model. The goal is to help participants prepare for collaboration: elicit reasoning that is not yet visible, surface neglected risks, and support human interpretation of the resulting context.'),
('Different roles need different support', 'For novices, the system asks questions grounded in their project context and helps them articulate assumptions, uncertainties, and meeting agendas. For mentors, it brings together that context and suggests coaching strategies informed by mentor-specified goals. This is personalization around a relationship and joint task, not simply an individual user profile. Mentors retain control over the explicit domain model guiding the questions.'),
('Design and evaluation', 'Using Research through Design within an action-research framework, we iterated prototypes with four mentors and four novices. A subsequent exploratory deployment involved a different group: one mentor and 11 novices, each using the system for one real coaching meeting. Evidence included interviews, think-aloud interaction, surveys, recordings, and comparisons of articulated risks and plans.'),
('What we learned', 'Novices reported identifying overlooked risks and reconsidering tasks that felt productive but did not address critical uncertainties. Different preparation for each role helped novices clarify concerns and helped the mentor connect information before the meeting. Participants described their conversations as more focused, intentional, and in-depth. The mentor could also revise the underlying model, adding missed teamwork risks and refining what counted as adequate testing.'),
('Tensions and evidence boundaries', 'Incomplete input sometimes produced misleading diagnoses and extra verification work. Some users expected immediate answers and found reflective questioning less helpful. The findings are exploratory and situated: there was no randomized comparison with a generic chatbot, no demonstrated long-term skill transfer, and no measured effect on venture success. The one-to-one deployment also did not test every peer-learning mechanism from the earlier one-to-many model. A continuing question is when repeated scaffolding develops judgment and when it may create dependency.')],
['[2] Huang, E., Easterday, M., &amp; Gerber, E. (2025). AI That Helps Us Help Each Other: A Proactive System for Scaffolding Mentor-Novice Collaboration in Entrepreneurship Coaching. Proceedings of the ACM on Human-Computer Interaction, 9(7). <link href="https://doi.org/10.1145/3757549">doi:10.1145/3757549</link>. <link href="https://arxiv.org/abs/2508.11052">Open-access paper</link> / <link href="https://github.com/eveyhuang/coaching_assistant">System code</link>.'])
page(5,'Learning and tacit judgment','STREAM 01 / RELATED FOUNDATIONS','Learning to collaborate',
'Helping people articulate what they know also raises a longer-term question: what do they learn to notice and do for themselves?',[
('Workplace learning during complex work [3]', 'With an interdisciplinary group of collaborators, I developed a workshop proposal and research agenda about supporting collaboration skills in design, engineering, research, and other complex work. Access to colleagues and communication tools does not by itself teach people how to use those opportunities. Effective collaboration requires learning to articulate requests, seek and provide help, form relationships, coordinate expertise, and reflect on work practices.'),
('', 'The agenda considers organizational structures, everyday routines, and collaboration technologies together. It asks how these arrangements can support capability development alongside immediate productivity. This provides a learning-oriented foundation for my coaching research: an AI system can help someone prepare for a meeting today, but whether that support changes their capacity to collaborate over time is a separate empirical question. The paper is a workshop proposal and research agenda, not a report of completed workshop outcomes or a new intervention trial.'),
('Making tacit literary judgments inspectable [4]', 'My earlier work with Sarah Sterman, Vivian Liu, and Eric Paulos studied literary style, a quality people often recognize but struggle to describe formally. A formative interview study with 14 participants showed that people communicated stylistic impressions through comparisons and examples. We used crowdsourced comparative judgments to build a neural representation of stylistic similarity, paired with Explorer and Editor interfaces.'),
('', 'An exploratory study with six users examined how these interfaces supported interpretation. Visual patterns prompted people to articulate distinctions, question assumptions, and explore relationships within and across texts. Some valued the overall pattern more than precise positions or colors. The representation captured a partial shared signal; low agreement among judgments and model or projection errors limited what could be inferred.'),
('Connection to the broader program', 'The contribution was not a universal model of style or proof of better writing or teamwork. It was an approach to eliciting difficult-to-articulate judgments, building representations that people could inspect, and preserving human interpretation. This methodological thread continues in my later work: make relevant knowledge visible, study how people use it, and examine what the representation leaves out.')],
['[3] Huang, E., Garg, K., Gómez-Zará, D., Hui, J., Kulkarni, C., Massimi, M., Churchill, E. F., &amp; Gerber, E. (2023). Supporting Workers in Developing Effective Collaboration Skills for Complex Work. CSCW Companion, 486-489. <link href="https://doi.org/10.1145/3584931.3611290">doi:10.1145/3584931.3611290</link>.','[4] Sterman, S., Huang, E., Liu, V., &amp; Paulos, E. (2020). Interacting with Literary Style through Computational Tools. CHI. <link href="https://doi.org/10.1145/3313831.3376730">doi:10.1145/3313831.3376730</link>.'])
page(6,'Multimodal research agenda','STREAM 02 / METHODOLOGICAL AGENDA','Understanding collaboration',
'How can we observe collective work as an unfolding process, rather than reduce a team to one aggregate score?',[
('The measurement problem', 'Organizational research has long examined coordination, knowledge integration, participation, and psychological safety. Yet observing these processes continuously in real work is difficult and expensive. Surveys and aggregate impressions capture important aspects of experience, but cannot alone show how members respond to disagreement, take up expertise, recover from breakdowns, or change their behavior over time.'),
('Measuring what matters in teams [5]', 'With Brian Uzzi and Matt Groh, I develop a methodological agenda for using multimodal AI to connect language, vocal cues, and visible behavior at individual, dyadic, and team levels. The article distinguishes three opportunities. <b>Scale</b> could support tests of when behavioral relationships generalize across settings. <b>Resolution</b> could connect organizational constructs to enacted behavior, including responses to dissent, mistakes, and requests for help. <b>Temporal continuity</b> could make it possible to trace escalation, repair, and turning points.'),
('Validity is specific to the construct and setting', 'The opportunity is more than cheaper coding. It is to investigate collaboration as a process and compare reported experience with observable practice. But performance on a general video benchmark does not establish that a model validly measures an organizational construct. Our empirical program develops theory-grounded behavioral codebooks, compares AI annotations with human judgments, examines errors and boundary conditions, and relates interaction patterns to outcomes.'),
('Measurement also changes organizational life', 'The article considers how hidden ratings, managerial surveillance, or narrow participation norms could undermine trust or encourage people to optimize visible signals. Bounded uses, participation in defining measurements, contestability, and human interpretation matter alongside technical accuracy. How a measure is designed and used is part of the organizational question.'),
('What this article establishes', 'This is a perspective and methodological agenda, not a report of original validation or outcome results from our team datasets. The ongoing studies on the next page develop and test applications. They use AI to study human interaction; they do not yet establish the effects of an AI teammate participating in that interaction. Valid behavioral models could later inform the design and evaluation of such interventions.')],
['[5] Huang, E., Uzzi, B., &amp; Groh, M. (2026). Measuring What Matters in Teams with Multimodal AI. Journal of Organization Design. To appear.'])
page(7,'Team interaction studies','STREAM 02 / ONGOING EMPIRICAL PROJECTS','Three settings, connected questions',
'Across more than 1,000 hours of recorded interaction, I study how the demands of a task shape effective collaboration.',[
('Scientific teams / Integration behavior', 'In a manuscript in preparation with Max Chalekson, Matt Groh, D. Abrams, and Brian Uzzi, we examine how members build on, connect, evaluate, and extend one another\'s contributions. The distinction is between producing more ideas and doing something useful with the ideas already present. Current analyses suggest that what distinguishes effective teams includes how the team subsequently works with its members\' contributions. We study how these interaction patterns relate to collective outcomes, providing an empirical foundation for support that helps teams integrate existing knowledge.'),
('Entrepreneurs and investors / Revealed preparedness', 'With Ava Grey, Brian Uzzi, and Matt Groh, I extend the approach to the back-and-forth between entrepreneurs and investors. We investigate how questions, challenges, and responses reveal preparedness, build rapport, and relate to evaluators\' judgments. The unit of analysis is the founder-evaluator exchange, rather than only the prepared presentation or the entrepreneur\'s internal team coordination. Studying the exchange makes it possible to ask how preparedness becomes visible when a claim is questioned or a response invites further discussion. Findings and their boundary conditions remain to be established.'),
('Professional volleyball / Enacted cohesion', 'We use team huddles to examine how cohesion is expressed through observable interaction and how those dynamics relate to subsequent performance. Volleyball provides a setting of tightly interdependent action and coordination under time pressure. The project examines behavioral relationships; it does not yet establish that intervening on a particular behavior improves team performance.'),
('Why compare these settings?', 'Scientific collaboration, investor evaluation, and professional sport place different demands on knowledge integration, response to challenge, and coordination. Together, they let us ask which patterns generalize and which depend on the task, interdependence, or evaluative pressure. The recordings are a research resource; their availability does not imply that all have already been annotated or that every construct is validated.'),
('Research support and collaborations', 'The project Building Behavioral Process Models from Real Teams with Multimodal AI received $75,000 from Microsoft\'s AI and the New Future of Work program. I independently wrote the proposal, with Brian Uzzi as PI. Our related TeamLens proposal was recognized as a finalist in the Stanford HAI and Google DeepMind AI for Organizations Grand Challenge. This work brings together collaborators across management, HCI, computer science, and engineering.')])
page(8,'Double compression','STREAM 03 / WORKING MANUSCRIPT','AI and collective outcomes',
'Individually plausible contributions can accumulate into a narrower collective search over ideas and perspectives.',[
('Double compression in scientific knowledge production', 'With Matt Groh and Brian Uzzi, I study a process with two consequential stages: generating scientific possibilities and deciding which deserve support. We compare 23 proposals and 85 expert reviews from a real molecular and cellular bioscience grant competition with proposals and reviews generated by Claude, Gemini, and GPT under the same call and evaluation criteria.'),
('Comparing collections, not only individual outputs', 'The computational experiments vary batch generation, independent calls, and independent calls conditioned on scientist personas. We use biomedical text embeddings, diversity and geometric-coverage measures, topic modeling of relevant literature, matched set and panel sizes, and original and style-normalized text. The central unit is the collection of ideas or judgments. An output can appear useful in isolation while adding little difference to the set around it.'),
('Two forms of compression', '<b>During generation,</b> AI sets cover broadly similar scientific territory but concentrate more heavily around common ideas. Some distinctive human proposals have no nearby AI counterpart under the manuscript\'s distance-based definition. This is underrepresentation within a computational representation, not proof that those human proposals are more valuable or scientifically novel.<br/><br/><b>During evaluation,</b> AI panels can cover much of the semantic territory of human reviews while producing more similar judgments among themselves. Convergence is especially pronounced in criticisms. Broad coverage therefore does not imply the same range of reasons for questioning a proposal.'),
('Robustness and interpretation', 'Independent calls and persona conditioning do not restore human-level semantic diversity in the conditions tested. Several findings persist after style normalization, though some displacement and coverage differences change. Effects vary across models, prompts, and measures; the argument is not that every model or condition compresses every aspect equally. The two stages also imply different design challenges: broaden the sources of candidate ideas and preserve nonredundant evaluation.'),
('What the study does and does not show', 'The manuscript motivates evaluating scientific AI by the range of possibilities and judgments it contributes to a collective process. It compares human and AI outputs from one competition, rather than assigning scientists to AI assistance. It does not test an end-to-end automated pipeline or measure realized innovation. How generation and evaluation compression interact in real AI-supported scientific work remains an open question.')])
page(9,'Participation and influence','STREAM 03 / PUBLISHED FOUNDATION','Whose judgments shape the response?',
'Inviting people to supply information does not necessarily give them influence over how that information is classified or acted upon.',[
('Online harassment tools as a setting [6]', 'With Abhraneel Sarma, Sohyeon Hwang, Eshwar Chandrasekharan, and Stevie Chancellor, I examined computational approaches to online harassment. The question was whether interventions reflected the identities and risks of intended beneficiaries, their definitions of harm, and their preferred forms of recourse. The work received an Honorable Mention at DIS 2024.'),
('Approach and scope', 'We conducted a scoping literature review and close qualitative analysis of 17 research papers, including both new systems and studies of existing tools. We organized the analysis around identity, definitions of harassment, and preferred responses. This was not a new AI deployment or an experiment comparing intervention effectiveness.'),
('Participation, interpretation, and authority', 'Papers often motivated systems through disproportionate harm to marginalized groups without clearly documenting how implemented features addressed those groups\' specific needs. Users might identify an experience as harmful while platforms or other actors retained authority to classify whether it counted as harassment. Different definitions, opaque processes, and distance from decision makers could prevent lived experience from shaping the response.'),
('', 'The review identified five response strategies: punishment, distancing from perpetrators, educating perpetrators, documenting and reporting evidence, and emotional or social support. What people could do depended on which responses the system made available. Configurable tools and community-based moderation offered ways to bring decisions closer to users, but configurability alone did not establish meaningful agency. Shared filters, trusted moderation, collective warnings, and supportive spaces also showed how tools could support a community\'s capacity to respond.'),
('Implications for my research on collective AI', 'The findings concern gaps in documented alignment between beneficiaries and systems; some gaps may reflect reporting rather than proof that the systems failed their users. My broader interpretation is that AI changes the distribution of authority as well as the distribution of information. This connects to mentors revising the coaching model, teams contesting behavioral measurements, and the perspectives retained in scientific evaluation. Across these settings, the question is who can shape the categories, judgments, and actions embedded in a shared system.')],
['[6] Huang, E., Sarma, A., Hwang, S., Chandrasekharan, E., &amp; Chancellor, S. (2024). Opportunities, Tensions, and Challenges in Computational Approaches to Addressing Online Harassment. DIS, 1483-1498. <link href="https://doi.org/10.1145/3643834.3661623">doi:10.1145/3643834.3661623</link>.'])
page(10,'Experience','A LITTLE MORE ABOUT ME','Research, design, and practice',
'I move between understanding how people collaborate and building systems they can inspect, revise, and use together.',[
('Research at Northwestern', 'I am a Research Assistant Professor at Northwestern University\'s Kellogg School of Management (July 2026-present). My research connects multimodal studies of team interaction with computational experiments on AI in scientific knowledge production. This builds on my postdoctoral work at Kellogg with Brian Uzzi and Matthew Groh (February 2025-June 2026).'),
('Building shared AI workflows / Novohaven', 'Since October 2025, I have worked as an AI Advisor and Forward Deployment Engineer. In an international e-commerce business, employees already used AI, but the quality and structure of complex deliverables depended on how each person supplied context and articulated a request. I designed and developed an agentic platform that turns company expertise into shared workflows, accessible through a web interface or Lark.'),
('', 'For market research, a workflow organizes information gathering, synthesis, company context, and a formatted report. Execution histories make the process inspectable. Domain experts can describe and revise how tasks should be done through natural-language instructions or direct specification of steps. The system is designed to treat recurring revision requests as signals for improvement, with human review before changes become shared practice. This is an applied system and a set of design goals; its effects on learning, quality, and coordination require dedicated empirical evaluation.'),
('A foundation in field partnerships and design', 'My PhD in Technology and Social Behavior at Northwestern (2024) bridged computer science and communication studies. A sustained partnership with an entrepreneurship incubator grounded my doctoral work, from observation and cognitive modeling to system design and exploratory deployment. I also coached undergraduate engineering students in human-centered design and engineering practices. I earned an MS in the same program (2023) and a BA in Economics from UC Berkeley (2017).'),
('Other applied experience', 'As an AI Technical Advisor to Spark AI (December 2024-December 2025), I advised product and engineering teams on AI feature design, integration, and deployment for K-12 learning products. At Northwestern Memorial Hospital (summer 2022), I studied older adults\' electronic health-record workflows, including medication and scheduling tasks, and translated usability findings into design recommendations.'),
('Outside work', 'I play guitar and tennis, take film and digital photographs, read, doodle, and cook spicy food. If you are thinking about similar research questions, I would love to connect: <link href="mailto:jiaxinh.evey@gmail.com">jiaxinh.evey@gmail.com</link>.')])
c.save();print(OUT)
