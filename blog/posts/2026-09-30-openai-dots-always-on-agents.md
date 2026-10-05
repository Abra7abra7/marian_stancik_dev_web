# OpenAI Dots and the Always-On Agent Runtime: What the Cloud Computer Architecture Means for Autonomous Systems

**Published:** September 30, 2026 | **Author:** Marian Stancik

---

September 30, 2026
  OpenAI
  Dots
  Autonomous Agents
  Agent Architecture
  MCP
  9 min read
  By Marian Stancik

# OpenAI Dots and the Always-On Agent Runtime: What the Cloud Computer Architecture Means for Autonomous Systems

On September 29, 2026, at DevDay in San Francisco, OpenAI launched a product that, on its surface, looks like a productivity tool: **Dots**, always-on autonomous agents powered by GPT-6 Astra that get their own cloud computer and web browser, plug into 4,000+ apps through a standardised tool protocol, and work in the background continuously — not in request-response cycles, but as persistent processes with memory, state, and agency.

Beneath the polished UX, what OpenAI shipped is not a chatbot feature. It is an **agent runtime architecture** — a cloud-native platform where each agent runs as its own process, owns its own filesystem and browser session, schedules its own tasks, and communicates with external tools through a protocol designed for tool composition. And the Codex harness that powers the whole thing is open source on GitHub.

I run **Hermes Agent** (by Nous Research) — an open-source agent runtime with 19 autonomous cron jobs, custom MCP servers, persistent memory, and security-by-design — on a Hetzner VPS. I have been running this pattern for months. OpenAI just shipped the same architectural bet as a product. That is worth examining in detail.

**The headline:** Dots validates the agent runtime architecture — persistent cloud computer, tool access via standardised protocol, always-on execution — that independent builders like me have been running in production for months. The product category is not "chatbots"; it is "agent infrastructure." And the open-source harness means you can build it yourself without paying $100/month.

## What Dots Actually Is

OpenAI's Dots is frequently described as "ChatGPT with superpowers." That is wrong. Dots is a fundamentally different product category: an always-on agent platform where each agent operates independently, not as a feature of ChatGPT but as its own entity in a shared workspace called **ChatGPT Space**.

Here is what ships:

- **Always-on autonomous agents:** Each Dot runs continuously in the background. You give it a goal ("Monitor competitor pricing and alert me when it changes"; "Keep my CRM enriched and my blog drafted") and it works persistently — re-queuing, re-planning, retrying failures without human intervention.

- **Own cloud computer + browser:** Every Dot gets its own virtual machine with a root filesystem, a full browser instance, and persistent storage. This is not a stateless API call. It is a long-running process with state, context windows that span days, and the ability to navigate the web as an independent entity.

- **4,000+ app integrations via MCP:** Dots connects to tools through the Model Context Protocol — the same standardised tool protocol that Anthropic introduced and that the creative industry adopted at SIGGRAPH 2026. Every app integration is an MCP server: filesystem, email, Slack, Notion, GitHub, Salesforce, and thousands more through OpenAI's MCP marketplace.

- **ChatGPT Space:** A shared workspace where your Dots and you coexist. You see what each Dot is doing, intervene when needed, inspect their reasoning, and reassign work between agents.

- **Codex harness (open source):** The underlying framework — CLI, SDK, app server — is available on GitHub. You can run the same agent runtime locally, connect your own models, and build custom agents without any OpenAI dependency.

The pricing is $100/month for Pro tier (up to 10 concurrently running Dots, unlimited MCP calls). The same Codex Harness is free to self-host on any infrastructure you own.

## Why the Architecture Matters: Cloud Computer, Not Chatbot

The most important architectural decision in Dots is not the model — GPT-6 Astra is powerful but it is an API you can call anywhere. The architectural innovation is the **cloud computer** abstraction: each agent is a first-class compute entity with:

- **Persistent identity:** The agent has its own session, its own files, its own database of completed work. It does not start from scratch every time you message it.

- **Tool composition:** MCP servers are composable. One agent can call the filesystem server to read a document, the browser server to research a topic, the email server to send the result — all in a single autonomous workflow, coordinated by the agent's own reasoning.

- **Background scheduling:** Agents maintain their own task queue. They check conditions ("has a new email arrived?"), trigger actions ("if stock drops below X, rebalance"), and report back asynchronously ("your weekly report is ready").

- **State persistence:** When an agent is working on a multi-hour task (research a market, draft a report, validate against data sources), it does not lose context if the conversation stalls. The cloud computer keeps running.

This is not an API wrapper. This is an **agent runtime** — the same architectural category as the system I have been running with Hermes Agent for months.

**Production insight:** The "cloud computer" pattern is what makes agents actually useful in production. I learned this the hard way — my first attempt at an autonomous agent system used stateless API calls with a queue. It broke constantly because the agent could not maintain state across steps. The switch to persistent processes with filesystem state was the single change that turned my agents from demos into production tools. Dots bakes this into the product from day one.

## Dots Architecture vs. Hermes Agent Runtime

The architectural parallels are striking. Here is a side-by-side comparison of the two systems:

DimensionOpenAI DotsHermes Agent (my stack)
RuntimeCloud computer per agent (OpenAI infra)Docker container per agent (Hetzner VPS)
Tool protocolMCP (4,000+ apps via marketplace)MCP (custom servers + vendor servers)
Agent modelGPT-6 Astra (proprietary, OpenAI)Any model via OpenRouter (user selects)
SchedulingBackground queue per agent (proprietary)Cron jobs + self-triggering tasks (19 agents)
MemoryPersistent per-agent (Cloud computer filesystem)Persistent MEMORY.md + session state
IdentityPer-agent OpenAI account (managed)Per-agent identity in control plane (self-managed)
Security modelScope authorization (tool-level permissions)Guardian layer + policy engine + audit trails
Open sourceCodex harness (CLI + SDK + app server) on GitHubHermes Agent (full stack) on GitHub
Cost$100/mo (Pro, up to 10 agents)~€4/mo (Hetzner VPS + OpenRouter usage)
GovernanceOpenAI-managed (black box)Self-managed (full visibility + control)

## How This Validates the Pattern I Have Been Running

I deploy Hermes Agent with 19 autonomous cron jobs running 24/7. They monitor system health, check competitor pages, scrape RSS feeds, enrich CRM entries, draft blog posts, and maintain this website. Each agent has its own MCP server stack — filesystem, database, web search, email — and runs through a control plane that enforces identity, policy, and audit on every tool call.

When I read the Dots architecture documentation, I recognised every pattern:

- **Persistent background agents with task queues:** My cron jobs use Hermes's scheduled execution layer — at :00 past each hour an agent fires, checks its condition, executes, and reports back. Dots does the same thing with a proprietary scheduler. Same abstract pattern.

- **MCP for tool composition:** My agents connect to MCP servers for filesystem, database, web search, and email operations. Dots connects to MCP servers for 4,000+ apps. The protocol is the same. The agent architecture around it — tool discovery, schema validation, error handling — is identical.

- **Control plane for security:** I built a guardian layer that checks identity and policy before every tool call. Dots has scope-based authorization. Both are solving the same problem: an agent with tool access needs guardrails, and they need to be enforced at the runtime level, not the model level.

- **Self-managed identity:** My agents have purpose-built identities — the blog agent writes to the blog database, the CRM agent writes to the CRM, neither can access the other's resources. Dots gives each Dot its own identity scoped to its tools. Same principle.

The key insight: I did this with open-source tools on a €4/month VPS. OpenAI did it with a proprietary stack on their infrastructure. The architecture is the same. The difference is scale and polish — not architectural soundness.

## The Open-Source Angle: Why Codex Harness Changes Everything

OpenAI released the Codex harness — the CLI, SDK, and app server that powers Dots — as an open-source project on GitHub. This decision may have more long-term impact than the Dots product itself.

The Codex harness gives you:

- A **CLI** to create and manage agent sessions, define tools, and run autonomous workflows

- An **SDK** for building custom agents with state, scheduling, and MCP connections

- An **app server** that hosts agents as persistent services with web endpoints

- A **tool specification format** based on MCP for connecting any API or service

Because the harness is open source, you can:

- Run it on your own infrastructure (no $100/month subscription)

- Swap in any LLM backend (not just GPT-6 Astra)

- Modify the runtime to fit your security and governance requirements

- Build agents that are not locked into OpenAI's ecosystem

`# Agent runtime pattern — persisted state, tools, scheduling
# The same architecture whether you use Dots or Hermes or Codex

class Agent:
    def __init__(self, agent_id, goal, tools):
        self.id = agent_id
        self.goal = goal              # Persistent goal, not one-shot prompt
        self.tools = tools            # MCP server connections
        self.state = AgentState()     # Persistent state across restarts
        self.scheduler = Scheduler()  # Background task queue

    async def run(self):
        """The agent loop — not a request-response handler."""
        while True:
            # 1. Assess current state
            status = await self.state.load()
            
            # 2. Decide next action based on goal + context
            plan = await self.reason(self.goal, status)
            
            # 3. Execute tool calls through MCP
            for step in plan.steps:
                result = await self.tools.call(step.tool, step.params)
                await self.state.remember(step, result)
            
            # 4. Schedule next run or wait for trigger
            await self.scheduler.sleep_until(
                plan.next_check or self.poll_interval
            )
            
            # 5. Report to human asynchronously
            if plan.has_report:
                await self.notify(plan.summary)`

## What Changes: Agent Runtime as a Product Category

Dots signals something larger than a product launch. It signals that the **agent runtime** is now a recognised product category, distinct from both chatbots and API wrappers. This has implications for every builder in this space.

First, the market now understands what an always-on agent looks like. Before Dots, explaining "I run 19 autonomous agents 24/7 on a VPS" required a paragraph of context. After Dots, people have a reference model. The cognitive load of evangelising the category just dropped to zero.

Second, the architectural template is now public and validated. OpenAI's engineers solved the same problems any builder faces: how to keep an agent alive across restarts, how to authenticate tool calls from a background process, how to handle agent failures without losing work. The Codex harness makes those solutions observable, replicable, and improvable.

Third, the self-hosted vs. vendor-managed decision is now a real choice. Before Dots, there was no vendor-managed option for agent infrastructure — you had to build it yourself. Now you have three paths:

- **Self-hosted with Hermes Agent** (open source, full control, €4/month)

- **Self-hosted with Codex Harness** (open source, OpenAI's patterns, your infra)

- **Vendor-managed with Dots** (proprietary, OpenAI runs it, $100/month)

Each path has different trade-offs in cost, control, privacy, and maintenance burden. The existence of all three is a sign of a maturing ecosystem.

## Security Implications After Astra

Dots launches in the shadow of OpenAI's **Astra cancellation** — the GPT-6 Astra safety research program was suspended earlier in 2026 after a cascade of agent autonomy safety incidents. The details are not fully public, but the industry consensus is that agents with unrestricted tool access and browser control triggered a series of escalating failures that forced a safety review.

This context matters for Dots's architecture. Every architectural decision in Dots — scope-based authorization, per-agent identity, tool-level permissions, the cloud computer boundary — is a direct response to the Astra safety findings. The lessons are built into the product.

But the numbers are sobering. Industry data cited in the DevDay briefing:

- An agent swarm at Stanford Science achieved a **37k-node coordinated task** — but the same architecture could, in theory, coordinate an attack of equivalent complexity.

- Red-team testing showed **88% evasion rate** for prompt-injection attacks that redirected agents to exfiltrate data through authorised MCP tools.

- **Gartner predicts 40% of enterprise agent deployments will fail** due to inadequate security guardrails by 2027.

**Security reality:** An agent with a cloud computer, a browser, and 4,000+ MCP tool connections is a powerful asset. It is also a powerful attack vector. The Astra cancellation was a reminder that agent security cannot be an afterthought. If you deploy always-on agents — whether through Dots, Codex, or Hermes — you need scope authorization, audit trails, rate limits, and human-in-the-loop for high-impact actions. The Cloud Computer does not change the security fundamentals; it raises the stakes.

## Practical Advice for Builders

The Dots launch changes the conversation around always-on agents. Here is what I would recommend to anyone building in this space:

### 1. Understand the architecture, not just the product

The cloud computer pattern — persistent process, own filesystem, tool composition, background scheduling — is the durable abstraction. Whether you use Dots, Codex, Hermes, or build your own, this is the architecture you should target. The product wrappers will change; the runtime pattern will not.

### 2. Start with the open-source harness

Before paying for Dots, run the Codex harness or Hermes Agent on a $5 VPS. Build one agent — a simple monitor that checks a URL daily and emails you if it changes — and understand the runtime. The cost of learning the architecture on your own infrastructure is near zero. The cost of learning it inside a proprietary platform is vendor lock-in.

### 3. Plan for security from agent #1

Every agent I have deployed has identity scoping, tool-level permissions, and audit logging. This is not paranoia. An agent that can read your filesystem and send email needs the same access controls as a human employee — because it can make the same mistakes, and the 88% prompt-injection evasion rate means it will.

### 4. Build for the MCP ecosystem

Dots supports 4,000+ apps via MCP. Hermes Agent uses MCP. The Codex harness uses MCP. If your tool does not have an MCP server, write one. The protocol is now the standard connector for agent-to-tool communication across every major runtime. One MCP server = accessible from every agent runtime on the market.

## What Comes Next

OpenAI Dots is not a finished product. It is a category marker. The company that defined the chatbot category with ChatGPT in 2022 has now defined the agent runtime category with Dots in 2026 — and open-sourced the harness so anyone can build on it.

For me, the validation is concrete: the runtime pattern I have been running for months — persistent agents with MCP tool access, scheduled background tasks, identity-scoped security, self-managed on a Hetzner VPS — is the same pattern OpenAI just productised at scale. The difference is that I can run it for €4/month with full visibility and control, while Dots costs $100/month and runs inside OpenAI's black box.

That is not a critique of Dots. It is a statement about architecture: the agent runtime is now a solved problem. The question is not "can you build it?" The question is "which runtime fits your requirements for cost, control, privacy, and scale?"

I know my answer. The fact that you now have a choice — self-hosted with Hermes, self-hosted with Codex, or managed with Dots — is the best outcome for the entire ecosystem.

`OpenAI Dots — Architectural Takeaways
────────────────────────────────────────
Product category:  Agent runtime (not chatbot feature)
Core pattern:      Cloud computer + MCP + persistent scheduling
Open source:       Codex harness (CLI + SDK + app server)
Cost:              $100/mo Pro vs ~€4/mo self-hosted
Agent scale:       10 per Pro account (Dots), unlimited (self-hosted)
Security model:    Scope authorization (response to Astra findings)
Industry context:  88% prompt-injection evasion rate; 40% failure prediction
────────────────────────────────────────
`

  

### ☢ Subscribe for Agent Architecture Essays
  

Every post breaks down what production agent infrastructure actually looks like — patterns, failures, architecture decisions from a system that has been running 24/7 for months.
  

Subscribe via Email
  

No spam. Unsubscribe anytime.

🤖 AI-generated | Info only | marianstancik.dev/disclaimer

---

*⚠️ AI-generated | Info only | marianstancik.dev/disclaimer*
