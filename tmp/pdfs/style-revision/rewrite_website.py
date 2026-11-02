from pathlib import Path
import re
root=Path.cwd()
content={
'AI-coaching.md':('We examine how coaches make distributed expertise usable and translate those practices into AI that scaffolds novice reflection, mentor preparation, and the development of collaboration skills.', '''Entrepreneurs must articulate uncertain goals, evaluate incomplete evidence, and identify whose experience can help them decide what to do next. These demands make coaching valuable, because mentors can diagnose gaps in reasoning and connect novices to expertise they would otherwise struggle to locate. Providing access to that expertise requires sustained interactional work: relevant knowledge must be identified, translated across projects, and connected to a request that another person can address. Across this research, we study how coaches perform that work and how AI can scaffold the reasoning and preparation on which it depends.

## Understanding coaching expertise

**CSCW 2023 · Empirical study.** We examined a university incubator in which coaches supported several novice entrepreneurs working on different ventures, stages, and timelines. Through interaction analysis of 24 virtual coaching sessions involving three coaches and 30 novices, supplemented by retrospective coach interviews and Slack observations, we developed a cognitive model of one-to-many coaching. The recordings covered 14 hours across eight weeks; the novices formed a learning community rather than necessarily belonging to one venture team.

Our analysis identified several practices through which coaches made distributed experience usable. Coaches questioned assumptions and missing evidence, translated project-specific experiences into transferable lessons, and connected novices to peers with relevant expertise. They also helped novices articulate what assistance they needed and why, making it easier for others to recognize where they could contribute. For example, an account of a venture's particular testing problem could become a lesson about how to design an experiment that other entrepreneurs could apply.

Coaches also organized the conditions under which novices experimented and learned from one another. Supportive peer testing and reframing setbacks helped novices engage with uncertain results, while public commitments provided accountability. Visibility could also reproduce weak norms when vague goals went uncorrected. These findings suggest that intelligent coaching systems should attend to the practices that make knowledge transferable and requests actionable, alongside the information available about each project. The study provides a qualitative account of one incubator; it does not establish causal effects on venture performance or psychological safety.

Evey Huang, Daniel Rees Lewis, Shubhanshi Gaudani, Matthew Easterday, and Elizabeth Gerber. [Intelligent Coaching Systems: Understanding One-to-many Coaching for Ill-defined Problem Solving](https://doi.org/10.1145/3579614).

## AI that helps us help each other

**CSCW 2025 · System design and exploratory deployment.** Preparing a coaching meeting requires novices to externalize reasoning that mentors cannot directly observe, while mentors must interpret sparse updates and plan assistance under limited time. We translated the cognitive coaching model into a proactive AI system that scaffolds these complementary activities. The system combines an LLM with project and risk models, a reflective chatbot, dashboards, and an authoring interface through which mentors can revise the knowledge guiding AI behavior.

For novices, the system uses project context to diagnose possible risks, generate reflective questions, and support the selection of a meeting agenda. For mentors, it presents project updates, selected and omitted risks, and suggestions informed by mentor-specified coaching goals. Mentors can inspect the underlying responses and revise risk definitions when the existing model misses an important concern. This division of labor makes the system's support responsive to both participants, while leaving the interpretation of incomplete or ambiguous context with the mentor.

We iterated prototypes with four mentors and four novices before conducting an exploratory deployment with a different group of one mentor and 11 novices, each preparing for one actual coaching meeting. Interviews, think-aloud sessions, surveys, recordings, and comparisons of articulated risks and plans provided situated evidence of how the system shaped preparation. Novices reported identifying neglected risks and reconsidering tasks that did not address critical uncertainties; participants described subsequent conversations as more focused, intentional, and in-depth.

The deployment also exposed constraints on this support. Incomplete novice input could produce misleading diagnoses and additional verification work, and expectations of immediate answers sometimes conflicted with reflective questioning. These findings inform the design of context-sensitive preparation, but do not establish long-term skill transfer, venture success, or superiority to a generic chatbot. Future evaluations should examine whether repeated scaffolding develops collaborators' own diagnostic judgment and when it may create dependency.

Evey Huang, Matthew Easterday, and Elizabeth Gerber. [AI That Helps Us Help Each Other: A Proactive System for Scaffolding Mentor-Novice Collaboration in Entrepreneurship Coaching](https://doi.org/10.1145/3757549). [Open-access paper](https://arxiv.org/abs/2508.11052) · [System code](https://github.com/eveyhuang/coaching_assistant).

## Learning to collaborate

**CSCW Companion 2023 · Workshop proposal and research agenda.** Complex work requires people to articulate requests, seek and provide assistance, and coordinate expertise as their understanding of a problem changes. Access to colleagues and communication tools creates opportunities for collaboration, but developing the skills to use those opportunities requires support within everyday work. We developed an interdisciplinary agenda examining how organizational structures, routines, and technologies can scaffold that learning. This agenda connects the immediate value of AI-supported preparation to a longer-term question: how does repeated assistance change what people learn to notice, articulate, and coordinate independently? The paper proposes a workshop and research agenda, rather than reporting an intervention trial.

[Supporting Workers in Developing Effective Collaboration Skills for Complex Work](https://doi.org/10.1145/3584931.3611290).

## Early work on tacit judgment

**CHI 2020 · Computational representations and interactive tools.** Literary style provides an earlier setting for studying judgments that people can recognize but struggle to articulate. With Sarah Sterman, Vivian Liu, and Eric Paulos, we used formative interviews, crowdsourced comparisons, and a neural model of stylistic similarity to develop Explorer and Editor interfaces. An exploratory study with six users examined how these representations supported reflection on patterns within and across texts.

Participants used the visualizations to articulate distinctions and question assumptions, although model and projection errors could also create confusion. The representation captured aspects of shared judgment without establishing a universal ground truth for style. This work informs an approach carried into the later projects: elicit tacit reasoning, make aspects of it inspectable, and retain space for human interpretation when the computational representation loses context or nuance.

[Interacting with Literary Style through Computational Tools](https://doi.org/10.1145/3313831.3376730).

[All research](/posts/) · [Publications](/publications/)
'''),
'AI-team-science.md':('We develop multimodal measures of team interaction to examine how people integrate expertise, respond to evaluation, and coordinate under different task demands, with validity assessed for each setting.', '''Teams coordinate work through sequences of contributions, responses, and adjustments that are difficult to reconstruct from aggregate outcomes or retrospective reports. Surveys and close observation provide valuable evidence, but observing these processes continuously across real work settings requires substantial time and interpretive labor. We examine how multimodal AI can make selected interaction processes observable at greater scale, while preserving the distinctions needed to interpret behavior in context.

## Measuring what matters in teams

**Journal of Organization Design · To appear, 2026.** With Brian Uzzi and Matt Groh, we develop a methodological agenda organized around three dimensions: scale, resolution, and temporal continuity. Linking language, vocal cues, and visible behavior could allow researchers to compare patterns across settings, connect organizational constructs to enacted behavior, and trace how collaboration changes over an interaction.

Each dimension addresses a different limitation of current observation. Scale creates opportunities to test when behavioral relationships generalize; resolution makes responses to disagreement, mistakes, and requests for help available for analysis; temporal continuity allows researchers to examine escalation, repair, and turning points. For example, comparing reported psychological safety with observed responses to dissent would make the relationship between perceptions and practice an empirical question.

These opportunities depend on construct-specific validation. Performance on a general video benchmark does not establish that a model reliably measures knowledge integration or cohesion in organizational settings. Our empirical program develops theory-grounded codebooks, compares AI annotations with human judgments, examines errors, and relates interaction patterns to collective outcomes. Organizations using such measurements should also establish who can define, inspect, and contest them, because behavioral visibility can otherwise become surveillance or encourage people to optimize narrow signals of performance.

The article presents a perspective and research agenda; it does not report validation or outcome results from the empirical projects below. Those projects use AI to study human interaction and provide a potential foundation for later interventions in which AI participates in collaboration.

Evey Huang, Brian Uzzi, and Matt Groh. *Measuring What Matters in Teams with Multimodal AI.*

## Scientific teams

**Manuscript in preparation.** Scientific collaboration requires members to evaluate and connect contributions whose relevance may become apparent only through discussion. We examine integration behavior: how members build on, connect, evaluate, and extend one another's ideas. Current analyses suggest that effective teamwork is distinguished in part by what the team subsequently does with its members' contributions, alongside the ideas they initially produce. Relating these patterns to collective outcomes may help identify when AI should surface missing information or scaffold integration, although the effects of such interventions require separate evaluation.

Evey Huang, Max Chalekson, Matt Groh, D. Abrams, and Brian Uzzi. *Multimodal AI for Large-Scale Scientific Team Behavior Analysis.*

## Entrepreneur–investor interaction

**Ongoing study.** Evaluators encounter entrepreneurial claims through both prepared presentations and the exchanges that follow them. Questions and challenges require founders to clarify assumptions, substantiate claims, and respond to concerns that may not have appeared in their presentation. We study how this interaction reveals preparedness, develops rapport, and relates to evaluators' judgments, focusing on the founder-evaluator exchange as the unit of analysis.

The measurement pipeline uses a codebook to guide multimodal annotation of questions, answers, and other interaction events. Human coding provides a basis for examining annotation agreement, while structured event records preserve who contributed, when, and how a response connects to an earlier question. This structure supports analysis of interaction sequences and interpretable behavioral concepts. The study remains ongoing, and relationships between these measurements and evaluation outcomes have not yet been established as findings.

Evey Huang, Ava Grey, Brian Uzzi, and Matt Groh. *Revealed Preparedness: Measuring Entrepreneur–Investor Interaction at Scale with Multimodal AI.*

## Professional volleyball

**Ongoing study.** Professional volleyball requires tightly interdependent action, with limited time to coordinate between periods of play. We use team huddles to examine how cohesion is enacted through observable interaction and how those dynamics relate to subsequent performance. The setting allows us to study coordination under time pressure, while distinguishing behavioral associations from the effects of interventions intended to improve teamwork.

Across scientific, entrepreneurial, and sports settings, the program draws on more than 1,000 hours of recorded interaction. Comparing these settings allows us to examine which patterns depend on task uncertainty, interdependence, or evaluative pressure; the available recordings do not imply that all have already been annotated or that every construct is validated. Such comparisons can inform context-sensitive support only when the measurements and their boundaries are established for the work being studied.

This stream received **$75,000 from Microsoft's AI and the New Future of Work program** for *Building Behavioral Process Models from Real Teams with Multimodal AI*. The proposal was independently written by Evey Huang, with Brian Uzzi as PI. The related **TeamLens** proposal was also recognized as a [finalist in the Stanford HAI and Google DeepMind AI for Organizations Grand Challenge](https://hai.stanford.edu/industry/ai-for-organizations-grand-challenge).

[All research](/posts/) · [Publications](/publications/)
'''),
'double-compression.md':('We examine how AI changes diversity across scientific proposals and reviews, and how computational systems distribute influence over the categories, judgments, and responses that shape collective decisions.', '''Scientific knowledge production requires researchers to generate different possibilities and preserve distinct evaluative perspectives when deciding which possibilities to pursue. Evaluating the quality of an individual AI output captures only part of this process, because plausible contributions may overlap in ways that narrow the collective set of ideas or judgments. We examine these collection-level properties alongside a related question of authority: whose input can shape how information is interpreted and acted upon?

## Double compression in scientific ideas and reviews

**Working manuscript · In preparation.** With Matt Groh and Brian Uzzi, we compare 23 proposals and 85 expert reviews from a real bioscience grant competition with outputs generated by Claude, Gemini, and GPT under the same call and evaluation criteria. The computational experiments vary batch generation, independent calls, and calls conditioned on scientist personas. Biomedical text embeddings, diversity and geometric-coverage measures, topic modeling, matched set sizes, and style-normalized comparisons allow us to examine the distributions of proposals and reviews.

The working manuscript identifies two forms of compression. During **generation**, AI proposals cover broadly similar scientific territory while concentrating around common ideas, leaving some distinctive human proposals underrepresented. Distinctiveness is defined relative to the computational representation and proposal set; it does not establish that an underrepresented proposal is more novel or scientifically valuable.

During **evaluation**, AI panels can cover much of the semantic territory of human reviews while producing more similar judgments, particularly in their criticisms. Coverage and diversity therefore capture different properties: a panel may address familiar topics without preserving the same range of reasons for questioning a proposal. This distinction suggests that expanding the number of AI-generated reviews may not by itself expand the perspectives available to a decision process.

Several findings persist across original and style-normalized text, although effects vary by model, prompting condition, and measure. Independent calls and persona conditioning do not restore human-level semantic diversity in the tested conditions. These comparisons motivate evaluating AI by its contribution to collective search and evaluation, while limiting the conclusion to the models, prompts, and representations studied.

The study compares human and AI outputs from one competition. It does not test how scientists work with AI assistance, an end-to-end automated funding process, or realized innovation. Future evaluations should examine whether interventions that broaden candidate ideas also preserve independent sources of judgment during selection, since the two forms of compression create different design requirements.

Evey Huang, Matt Groh, and Brian Uzzi. *Double Compression: How AI Narrows Both the Generation and the Gatekeeping of Scientific Ideas.*

## Whose judgments shape the response?

**DIS 2024 · Honorable Mention.** Computational approaches to online harassment depend on decisions about whose experiences matter, what counts as harm, and which responses a system makes available. Through a scoping review and qualitative analysis of 17 papers, we examined how interventions reflected intended beneficiaries' identities, definitions of harassment, and preferred forms of recourse.

Our analysis identified gaps in the documented connection between beneficiaries' needs and implemented systems. Papers could motivate a tool through disproportionate harm to marginalized groups without explaining how its features addressed those groups' specific circumstances. Users could also report an experience while platforms retained authority over whether it counted as harassment and what response followed. Participation in supplying information therefore did not necessarily entail influence over classification or action.

The review identified five response strategies: punishment, distancing from perpetrators, educating perpetrators, documenting and reporting evidence, and emotional or social support. Configurable tools and community-based moderation offered ways to bring decisions closer to users, but meaningful influence depended on whether people could understand and use those options. Some gaps may reflect reporting rather than demonstrated system failures, so the findings concern documented alignment rather than a causal comparison of effectiveness.

This work informs our broader analysis of collective AI by making the allocation of interpretive and decision authority explicit. Systems that collect user input should specify how that input can affect categories, judgments, and available actions. In the wider research program, this question connects mentors' ability to revise a coaching model with teams' ability to interpret behavioral measurements and researchers' ability to preserve different evaluative perspectives.

Evey Huang, Abhraneel Sarma, Sohyeon Hwang, Eshwar Chandrasekharan, and Stevie Chancellor. [Opportunities, Tensions, and Challenges in Computational Approaches to Addressing Online Harassment](https://doi.org/10.1145/3643834.3661623).

[All research](/posts/) · [Publications](/publications/)
'''),
'AI-business.md':('This applied project encodes company expertise in shared AI workflows, allowing domain experts to specify task requirements and review revisions as organizational practices change.', '''## The problem in practice

Employees undertaking complex knowledge work must interpret a request, gather relevant information, and apply organizational context and standards to the resulting output. In an international e-commerce business, employees had adopted AI, but the quality and structure of deliverables still depended on how each person articulated the task and supplied company context. Useful practices remained distributed across employees, making them difficult to inspect, share, or revise as a common resource.

This project examined how an agentic AI platform could encode those practices in shared workflows while retaining domain experts' authority over the requirements and standards guiding the work.

## What the system makes inspectable

The platform, designed and developed by Evey Huang in collaboration with Novohaven, organizes tasks as sequences of steps with explicit information requirements and company standards. Employees access these workflows through a web interface or Lark, the team's messaging tool. For market research, a workflow can organize information gathering, synthesis, the application of company context, and delivery of a formatted report. A recorded execution history allows users to inspect how an output was produced and identify the step at which revision is needed.

Domain experts can describe how a task should be performed and work with AI to translate that description into an executable workflow. They can refine the workflow through natural-language instructions or specify individual steps directly. This arrangement makes aspects of expert practice available across the organization while preserving an interface through which those practices can be questioned and revised.

## Keeping shared knowledge revisable

Organizational practices change as teams encounter new tasks, exceptions, and requirements, creating a risk that a reusable workflow will continue applying assumptions that no longer hold. The system is designed to use recurring revision requests as signals of where a workflow may need improvement, with proposed changes undergoing human review before becoming shared practice. This division of labor assigns the system a role in surfacing recurring problems while retaining human responsibility for deciding which changes should guide subsequent work.

Shared workflows also concentrate authority over how tasks are framed and evaluated. Their design therefore requires explicit decisions about who can contribute expertise, who reviews revisions, and how users can inspect or contest the standards embedded in the workflow. These decisions shape whether shared support remains responsive to contextual differences across tasks.

## Connection to the research

The project extends the concern with making distributed expertise usable into an applied organizational setting. It connects to the [coaching research](/posts/ai-coaching/), where an explicit expert model guides AI behavior and mentors can revise that model when important context is missing. The [collective-outcomes research](/posts/double-compression/) adds a complementary evaluation criterion: common support should be examined for its effects on variation across outputs and judgments, alongside consistency within a task.

The platform and its design goals provide a setting for investigating these questions; effects on organizational learning, output quality, and coordination require dedicated empirical evaluation. Future studies could examine whether shared workflows reduce repeated articulation of company context while preserving employees' ability to adapt the process to unfamiliar cases.

## Partner and system

Industry collaborator: Novohaven Inc.

[System code](https://github.com/eveyhuang/novohaven) · [All research and projects](/posts/)
''')}
for filename,(desc,body) in content.items():
 path=root/'src/content/post'/filename
 front=path.read_text().split('---',2)[1]
 front=re.sub(r'^description:.*$', 'description: "'+desc+'"',front,flags=re.M)
 path.write_text('---'+front+'---\n\n'+body)
