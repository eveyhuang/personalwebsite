---
title: "Can Agentic AI Support Real Business Teams' Complex Workflows?"
description: "When every employee uses AI differently, quality becomes a lottery. I worked with an international business in the e-commerce industry to design and build an agentic AI system that transforms it's best practices into structured, repeatable workflows, so complex work runs consistently, regardless of who's asking."
publishDate: "18 Feb 2026"
featured: true
coverImage: "/3-design.png"
tags: ["Agentic AI", "Business", "Knowledge Work"]
---

A 10-person company operating across continents had already adopted AI. Everyone was using ChatGPT. And yet, something wasn't working.

The problem wasn't access to AI. It was what happened when the task got complex. For a simple, well-defined request, any capable prompt gets the job done. But for something like market research which involves gathering data, synthesizing competitive signals, applying company context, and producing a formatted deliverable — the outcome depended almost entirely on how skilled you were at prompting. Two people doing the same task would produce wildly different results. Institutional knowledge lived in the heads of the best prompters, not in the system.

That's the gap I was brought in to close.

![](public/AI-workflow-infographic.png)

**The Design Challenge**: The company didn't need another chatbot. They needed AI that could carry the company's standards, encode their best workflows, and deliver consistent results across everyone on the team, regardless of individual AI fluency. The question wasn't "what can AI do?" but "how do we make AI work the same way your best employee would, every time?"

**What I Built**: I designed and developed an agentic AI platform where the core unit of value isn't a conversation, it's a reusable, executable workflow. Employees interact through the tools they already use (a web interface and Lark, their team messaging app), but underneath, every complex request is matched to a structured workflow: a multi-step pipeline with specific models, prompts, and execution logic per step. A market research workflow doesn't just "ask AI", it collects data, runs transforms, applies company-defined standards, and delivers a formatted output, all in a governed, traceable sequence.

The key architectural decision was making these workflows genuinely executable, not just descriptive. When the agent selects a workflow like "Product Review Analyzer," it doesn't hand the user a set of instructions, it spawns an actual execution through a workflow engine, running each step with typed inputs, fallback handling, and a traceable run history. This means the workflow is tested and repeatable, not improvised fresh each time.

**The system is also designed to grow** in two distinct ways.
First, the people who hold institutional knowledge finally have a way to encode it. A domain expert on the team, someone who knows exactly how a good market research report should be structured, or what a strong client pitch looks like, can collaborate directly with the AI agent to define that workflow. They don't need to be technical. They can describe the process and goals in plain language, and the agent translates that into a structured, repeatable workflow ready for the whole team to use. Or if they prefer precision, they can provide exact prompts and step-by-step scripts. Either way, expertise that used to live in one person's head becomes institutional infrastructure.

Second, the system learns from how people actually use it. When team members repeatedly request revisions to a workflow's output, asking for a different tone, restructured sections, or missing information, those patterns don't disappear. The agent tracks them, surfaces recurring friction as evidence that something in the underlying workflow may be off, and proposes targeted fixes for the team to review and approve. The platform doesn't just execute work; it pays attention to where the work keeps falling short and gets better over time, with humans staying in control of what changes.

**The Harder Design Problem**: Beyond the technical architecture, the real challenge was organizational: how do you get a small, busy team to trust a system with complex work and actually contribute to making it better? I approached this on two fronts. For everyday users, I kept chat as the interface, familiar and low-friction, while making the underlying complexity invisible by default. They just ask, and the system handles the rest with the consistency of the team's most experienced AI user. For domain experts, I made it easy to put their knowledge in without needing technical skills, describe how the work should go, and the agent handles the translation into something the whole team can run. The result is a system that feels simple to use but grows smarter the more the team engages with it.

**Why This Matters at Scale**: Most organizations deploy AI at the individual level and then wonder why quality is inconsistent. This project made the case for a different model: AI that operates at the institutional level, encoding collective expertise into shared, governable assets. The result isn't just better individual outputs, it's organizational learning that compounds over time.


[Github repo for my system](https://github.com/eveyhuang/novohaven)

Collaborator: Novohaven Inc.