# 4 Billion Tokens for $200 Instead of $15,000: Real Savings on AI Agents

> **Published:** 2026-11-26  
> **Author:** Marian Stancik  
> **Summary:** Running every agent task on a frontier model is how budgets quietly disappear. Here is how routing routine work to DeepSeek via OpenRouter cut my token bill by roughly 98%.

---

November 26, 2026
  AI Agents
  6 min read
  By Marian Stancik

### 4 Billion Tokens for $200 Instead of $15,000: Real Savings on AI Agents

Last year my agents processed around 4 billion tokens. The bill was about 200 USD. The same workload on a top-tier frontier model would have landed somewhere near 15,000 USD. That is not a clever hack — it is one routing decision, made once and then measured for twelve months.

### Where the money actually disappears

Most people set up an agent, plug in the most expensive model they can find, and never look at the invoice until it hurts. Chat feels cheap because you send one message and get one answer. An agent does not work like that.

A single “write me a report” task can easily become 40 to 80 model calls. The agent reads a file, calls a tool, re-reads the context, retries a failed step, summarizes what it found, then formats the output. Every one of those calls carries the whole conversation with it. Your cost scales with context length, not with the length of the final answer.

The second leak is using a frontier model for work that does not need one. Classifying an email, extracting three fields from an invoice, reformatting JSON, deciding which tool to call next — none of that requires the most expensive reasoning engine on the market. But it is exactly what most setups send there, because it is the default and nobody changes it.

### How I route it

I run two open-source frameworks: Hermes Agent and OpenBot (an open-source alternative to the Grok bot). Both talk to models through OpenRouter, which gives me one key, many providers, and per-request logs I can actually audit.

- Default tier: DeepSeek V4/V4.1 Flash handles about 82% of my traffic. GLM Flash takes roughly 10% — cheap classification, routing decisions, short summaries.

- Frontier tier: reserved for hard reasoning, ambiguous decisions, and the final review pass. That is a small single-digit percentage of calls.

- Prompt caching: my 12-month cache hit rate is 86.1%. The system prompt and tool schemas are stable, so I pay full price only on the part that actually changes.

- Short context: tool outputs get trimmed, old turns get summarized, and I never dump a whole file into the window when three paragraphs would do.

Across twelve months that came to 11.5 billion tokens, 113K requests, and 416.19 USD total — a blended 0.04 USD per million tokens. Hermes Agent accounted for 6.67B of those tokens, OpenBot 4.67B.

### How to measure token ROI

Token price alone tells you nothing. What matters is cost per finished task.

- Log every request: model, input tokens, output tokens, cached tokens, cost, and a task ID.

- Group by task ID and compute the real cost of one completed piece of work.

- Compare that against the human minutes it replaced. A task that costs two cents and saves six minutes is a good trade. A task that costs four dollars and saves two minutes is not, no matter how impressive the model is.

- Watch the cache hit rate weekly. When it drops, someone usually changed the system prompt or added a timestamp to the top of it.

- Set a hard monthly cap in OpenRouter. Not because you plan to hit it, but because an agent stuck in a retry loop will happily spend your budget overnight.

### Where it breaks and what to watch

Cheap models are cheaper for a reason. DeepSeek Flash is noticeably weaker at long multi-step reasoning and at subtle instruction following. I have had it silently drop a constraint I explicitly set. Cheap model plus a sloppy prompt equals cheap garbage, and you still need a small set of test cases to catch that.

Caching only works if your prompt prefix is stable. Put a dynamic timestamp at the top and you lose most of the savings without noticing.

Latency and rate limits vary by provider, so anything user-facing needs a fallback route. And sending business data to third-party providers is a GDPR question, not a technical one. I am a third-year law student, not a lawyer — anything I write about privacy or the EU AI Act is a subjective note, and for real decisions you need an attorney.

One more thing worth stating plainly: this article and this site are prepared with AI agents, with final human editorial control. That is the honest version, and it is also what the EU AI Act transparency rules ask for.

### Bottom line

Routing routine work to DeepSeek through OpenRouter is the single biggest cost lever I have found — roughly 98% off the bill, with no meaningful loss on the tasks that matter. Measure cost per task, not per token, and cap the budget before you need to.

If you want to talk through your own setup, message me on WhatsApp at +421 940 377 855. Free tools and prompts are at 
```
/sk/tools/
```
.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
