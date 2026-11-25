# Five Tests I Run Before an AI Agent Touches Real Work

> **Published:** 2026-11-25  
> **Author:** Marian Stancik  
> **Summary:** A cheap agent that fails silently costs more than an expensive one that stops. Five boring checks I run before handing over a real task.

---

November 25, 2026
  AI Agents
  5 min read
  By Marian Stancik

### Five Tests I Run Before an AI Agent Touches Real Work

Five checks. That is how long it takes me to decide whether an AI agent gets access to real work or stays in a sandbox. No benchmarks, no leaderboard screenshots — five boring tests that cost a few dollars and one afternoon.

### Why most people test agents the wrong way

Most people judge an agent by its demo. You type a nice question, it answers nicely, everyone nods. The problem is that a demo runs on a clean path: perfect input, no missing fields, no half-broken API, nobody waiting on the other side.

Real work is messy. A form arrives with an empty VAT field. An inbox contains a message in three languages. An API returns 200 OK with an error hidden inside the body. An agent that handles the demo and then fails silently on the messy version is worse than no agent at all — because you stop checking.

The cost is not the tokens. The cost is the email that never went out, the invoice with the wrong number, the client who waited two days for a reply the agent supposedly handled.

### How I test an agent before it touches anything real

I build on open-source frameworks — mostly Hermes Agent and OpenBot (an open-source alternative to Grok bot) — and route the model through DeepSeek on OpenRouter. That combination is cheap enough that testing is basically free. Here is the routine.

- 1. The empty-input test. I send nothing. Then a single space. Then a 40-page PDF. Then a file with the wrong extension. If the agent invents an answer instead of stopping, it fails.

- 2. The stop-and-ask test. I give it a task with one detail deliberately missing — a date, an amount, a recipient. A good agent asks. A bad agent guesses confidently, and confident guessing is the most expensive behaviour in the whole system.

- 3. Cost per finished task, not per token. Token prices are a distraction. What matters is what one completed task costs. Last month I pushed roughly 4 billion tokens for about $200 through DeepSeek on OpenRouter. The same volume on the most expensive frontier models would land near $15,000. Same lesson either way: measure the finished job, not the receipt.

- 4. The repeatability test. I run the identical task ten times and compare the outputs. If the structure moves on every run, the agent is not ready for anything that feeds a database or a client.

- 5. The undo test. Before anything writes, sends or deletes, I need a dry-run mode and a log I can actually read. If I cannot reverse it, I do not switch it on.

None of this is clever. It is the same discipline you would apply to a new employee in their first week — except the employee never gets tired and never learns from being embarrassed.

### Where this breaks down

Passing five tests means the agent worked on the day you tested it. It does not mean it works in week three. Models get updated, prompts rot, an upstream API renames one field and the whole chain quietly produces garbage that still looks correctly formatted.

So the tests are a snapshot, not a certificate. I re-run the cheap ones weekly and keep a human in the loop on anything that leaves the building. AI is a tool, not magic — and a tool needs maintenance.

Two more honest limits. First, I cannot test what I cannot measure, and plenty of tasks (writing, judgement, tone) resist clean measurement. Second, if your agent touches personal data or falls under the EU AI Act, my notes here are exactly that — subjective observations from a third-year law student. I am not a lawyer and I do not provide legal advice. Talk to an attorney.

### Bottom line

Test the boring failures, not the impressive successes. Empty input, missing detail, repeatability, cost per finished task, and a way to undo — that is the whole checklist, and it has saved me more money than any model comparison.

If you want to go through your own setup, message me on WhatsApp at +421 940 377 855 or grab the free tools at /sk/tools/. This article, like the rest of the site, is prepared with AI agents and a final human check.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
