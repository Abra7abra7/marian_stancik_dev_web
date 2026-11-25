# How I Test an AI Agent Before I Let It Touch Real Work

> **Published:** 2026-11-25  
> **Author:** Marian Stancik  
> **Summary:** An agent that works in a demo and one that works on Monday morning are different things. Here are the five checks I run before any agent gets real work.

---

November 25, 2026
  AI Agents
  6 min read
  By Marian Stancik

### How I Test an AI Agent Before I Let It Touch Real Work

An agent that works in a demo and an agent that works on a normal Monday morning are two different things. Before I let any agent touch real work, it goes through five checks. Most of them take under ten minutes and save hours of cleanup later.

### The problem: we judge agents by the demo

Almost every agent I see presented online is shown the same way: one clean input, a friendly example, a human watching the screen. It looks great. Then you connect it to a real inbox, a real spreadsheet or a real client request and it falls apart — not with a crash, but quietly.

Silent failure is the expensive kind. The agent says “done”, writes a half-correct row into your sheet, sends a reply with the wrong name, or loops through the same tool call fifteen times. Nobody notices for a week.

Cost makes this worse. I run about 4 billion tokens a month for roughly $200 through DeepSeek on OpenRouter. The same volume on the most expensive frontier models would be around $15,000. Cheap tokens are great, but they also mean a looping agent doesn't hurt immediately — so wrong output survives longer before anyone catches it.

### How I test agents before they get real work

I build on open-source frameworks — mostly Hermes Agent and OpenBot (an open-source alternative to the Grok bot) — with DeepSeek via OpenRouter for cheap iteration. The five checks below are the same regardless of framework.

- 1. Start with the ugliest input you have. Not a typed-out example — the real screenshot, the half-written email, the PDF with a table that doesn't parse. If the agent only works with perfect input, you built a script, not an agent.

- 2. Run it twice on the same input. Same task, same data, twice. If the answers differ, find out why before you trust it: temperature, tool order, a timestamp hidden in the prompt. Non-determinism isn't automatically bad, but unexplained non-determinism is.

- 3. Take a tool away. Disconnect one API or revoke one key and run the task again. A good agent fails loudly and tells you what's missing. A bad one invents an answer. Loud failure is a feature you want.

- 4. Count steps and tokens. Log every tool call. A simple task that takes fourteen steps usually means a vague prompt or a badly written tool description, not a hard task.

- 5. Read the output as a stranger. Would a colleague who doesn't know your setup understand the result without asking you? If not, the agent isn't finished — it just moved the work to someone else.

None of this needs a testing framework or a CI pipeline. It needs twenty minutes and the willingness to be unimpressed.

### Where this fails and what to watch

Honest limits: five checks don't cover the real world. An agent can pass all of them and still break on Tuesday when a website changes its HTML or a client sends something you've never seen. Tests reduce surprises; they don't remove them.

Two more traps I've hit:

- Testing on a different model than you ship on. Cheap models for iteration are fine, but behaviour changes between models. The final check has to run on the model that actually does the work.

- Unconscious babysitting. If you're always nearby to nudge it, you're not testing an agent — you're testing yourself. Leave it alone for a day and see what happens.

And the legal side: if your agent touches personal data, GDPR and the EU AI Act come into play. I'm a third-year law student, not a lawyer — anything I write about regulation is a subjective note, and for real decisions you need an advocate.

### Bottom line

AI is a tool, not magic. The difference between an agent that saves you time and one that quietly makes a mess is usually not the model — it's whether you spent twenty minutes trying to break it first.

If you want to compare notes on testing your own setup, message me on WhatsApp at +421 940 377 855, or try the free tools at /en/tools/. This article and the site are prepared with AI agents and final human review.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
