# Die Konvergenz der Agenten-Architekturen: Warum alle das gleiche Zwei-Ebenen-System bauen

> **Published:** 2026-09-02  
> **Author:** Marian Stancik  
> **Summary:** NVIDIA AVO, die AOS-Referenzarchitektur und Auton einigten sich auf das gleiche Muster: Trennung von Governance und Ausführung.

---

Over the last three months, three independent research efforts — NVIDIA's AVO, the AOS reference architecture (arXiv 2608.03214), and the Auton Agentic AI Framework (arXiv 2602.23720) — converged on the same core architectural pattern for production autonomous agents. A two-plane design that separates control and governance from runtime and coordination.

    

This is not a coincidence. It is the field maturing.

    

When independent teams working on GPU kernel optimization, interactive reasoning benchmarks, and enterprise agent governance independently arrive at the same architectural split, you are looking at an emerging standard. The names differ — AVO calls it "supervision loop + agent loop," AOS calls it "Control & Governance Plane + Runtime & Coordination Plane," Auton calls it "Cognitive Blueprint + Runtime Engine" — but the structural division is identical across all three.

    

Here is what the two-plane architecture is, why it matters for anyone deploying agents in production, and how to build your own.

    

### The Pattern, Named Differently by Each Team

    

Each effort uses different terminology, but the structural split is the same:

    
      
        
          Framework
          Plane 1 — Control
          Plane 2 — Runtime
        
      
      
        
          NVIDIA AVO
          Supervision loop + policy enforcement
          Agent loop + persistent memory + tool interface
        
        
          AOS Paper
          Control & Governance: intent, policy, trust, audit
          Runtime & Coordination: lifecycle, routing, memory, scheduling
        
        
          Auton Framework
          Cognitive Blueprint + constraint manifold
          Runtime Engine + MCP integration + parallel execution
        
      
    

    

The names vary, but the semantic split is the same: one plane answers what should happen, the other answers how to make it happen. The control plane is the source of truth for intent, policy, and authority. The runtime plane is the execution substrate that translates those decisions into coordinated action across agents, tools, models, and memory systems.

    

### Why Two Planes?

    

Current agent systems collapse control logic and execution logic into a single LLM call. The model decides and acts in one shot. This works for single-turn chatbots. It breaks for multi-day autonomous operations where you need audit trails, policy enforcement, recovery from failure, and human oversight.

    

The AOS paper makes the case formally, defining what belongs in each plane.

    

The Control & Governance Plane owns:
    
      
- Intent: what the user actually wants, not what the model inferred from ambiguous context
      
- Policy: permitted actions, resource budgets, safety constraints, allowed tool categories
      
- Trust and authority: delegated scope, credential management, revocation chain
      
- Confidence: does the accumulated evidence support proceeding with this action?
      
- Auditability: who authorized what, when, with which evidence, and under what constraints
      
- Human oversight: stop buttons, approval gates, escalation paths, override controls
      
- State reconciliation: when observed state diverges from authorized state, cancel or escalate
    

    

The Runtime & Coordination Plane owns:
    
      
- Agent lifecycle: spawn, schedule, pause, resume, terminate sub-agents and workers
      
- Model routing: select and dispatch to the optimal model per task type and budget
      
- Tool execution: call MCP servers, validate responses against schemas, handle errors and retries
      
- Memory coordination: episodic, semantic, procedural context delivery across sessions
      
- Workflow progress: state machines, retry policies, circuit breakers, timeout enforcement
      
- Telemetry emission: what actually happened, with what latency, at what cost
    

    

The separation matters because these planes scale differently. The control plane is throughput-light but correctness-critical — one bad policy decision corrupts everything downstream. The runtime plane is throughput-heavy but failure-tolerant — a failed tool call retries, a misrouted model call wastes compute but does not violate policy. Running them in the same process means you cannot scale one without the other, and you cannot audit without replaying execution.

    

NVIDIA AVO's 7-day autonomous GPU kernel optimization run demonstrates this in practice. The main agent (runtime) decides what to inspect, change, test, and evaluate. The supervisor (control) monitors for stagnation, resource budget violations, and unproductive cycles. When the search plateaus, the supervisor redirects. The control plane does not need to understand GPU kernel optimization — it only needs to detect that progress has stopped and trigger a corrective action.

    

### The Three Mechanisms Everyone Agrees On

    

Across all three architectures, three mechanisms emerge as non-negotiable for production-grade autonomous agents.

    

### 1. Persistent Memory Beyond the Context Window

    

Every architecture agrees: an agent that resets to zero at the end of each context window cannot sustain long-horizon work. LLMs are stateless across sessions — when the context window fills or the session terminates, all session-specific experience is lost unless explicitly preserved.

    

AVO uses a persistent store for code changes, compiler outputs, profiler results, and accumulated reasoning across 7-day runs. The AOS paper defines four state types — intended state, authorized state, observed state, and resulting state — that survive across invocations and form the basis for audit and reconciliation. The Auton framework introduces a reflector-driven consolidation protocol, inspired by biological hippocampal replay, that compresses episodic experience into semantic and procedural memory during idle cycles.

    

Implementation pattern: store structured state in SQLite or a vector database. When the context window approaches capacity, the runtime plane writes a checkpoint. The control plane validates the resulting state against policy before the next cycle begins. This turns the context window limitation from a bug into a feature — each window becomes a bounded atomic unit of work.

    

### 2. Supervision and Constraint-Based Guardrails

    

All three architectures reject the idea that prompt engineering alone can keep agents safe at production scale. Prompt-based safety is brittle, ungovernable, and produces no audit trail. The alternatives each team built are structurally similar.

    

NVIDIA AVO uses a dedicated supervisor process that runs in parallel with the main agent. Its only job is detecting stagnation — repeated error patterns, plateauing metrics, unproductive cycles — and triggering redirection. The supervisor does not need to understand the domain. It needs a clear definition of "stuck" and an escalation path.

    

The Auton framework introduces a constraint manifold — a formally defined subspace of the action space onto which the agent's policy is projected before action emission. Safety is enforced by construction, not by post-hoc filtering. Privilege escalation and unsafe operations are structurally impossible within the manifold.

    "Safety enforcement is not delegated to prompt engineering or post-hoc output filtering. Instead, constraints are expressed as code-level specifications, ensuring that privilege escalation and unsafe operations are excluded by construction." — Auton Agentic AI Framework (arXiv 2602.23720)

    

The AOS paper goes further, defining reconciliation controllers that continuously compare observed state against authorized state. When they diverge — the agent exceeded its budget, accessed a restricted tool, or operated outside its delegated scope — the controller cancels the operation, isolates the agent, and escalates to a human. This is not a guardrail prompt. It is a deterministic control loop.

    

This maps directly to what I deploy: watchdog cron jobs and Python monitor scripts that check for stagnation and budget overruns. A 50-line Python script that kills a task when it exceeds its iteration budget is infinitely more reliable than any prompt-based guardrail. The constraint-manifold approach suggests we should push this further — define the allowed action space in code, not in prompts.

    

### 3. Typed, Discoverable Tool Interfaces

    

All three frameworks use typed tool interfaces bound through the Model Context Protocol (MCP) or an equivalent. The evolution from unstructured prompt patterns to typed tool registries mirrors the evolution from REST without schema to OpenAPI — and the industry is at the same inflection point.

    

The AOS paper explicitly calls tool registries "the agentic analogue of API gateways" — they enumerate, version, and access-control every tool available to the agent. The Auton framework makes MCP integration its primary external interface, treating tools as typed contracts with input/output schemas and preconditions. AVO's tool interface is the most constrained of the three, precisely because its GPU kernel optimization domain demands strict schema validation for compiler flags, profiler parameters, and test configurations.

    

The practical implication: if your agent calls tools via free-text prompts, you have an integration, not an architecture. You cannot audit tool usage, validate tool output, or enforce tool access policies without a typed interface layer. MCP is emerging as the standard for this layer — the tool registry, as the AOS paper notes, is "where the agent meets the enterprise."

    

### From Architectural Pattern to Compliance Architecture

    

The convergence is not just technically interesting. It directly maps to regulatory requirements that took effect in August 2026.

    

The EU AI Act requires exactly the capabilities a two-plane architecture provides as built-in structural properties, not as bolt-on documentation exercises:

    
      
- Article 9 — Risk management: the control plane's policy enforcement and constraint-based guardrails implement risk mitigation by construction
      
- Article 12 — Record-keeping: the control plane already logs every authorization decision, every delegation, every policy override — these are not separate compliance records, they are the system's native audit trail
      
- Article 13 — Transparency: the control plane can reconstruct why a decision was made by replaying the authorized state before action, the policy that governed it, and the resulting state after execution
      
- Article 14 — Human oversight: the control plane's stop button, approval gates, and escalation paths are native architectural elements, not afterthoughts
    

    

The May 2026 Digital Omnibus agreement clarified that multi-agent systems are treated as a single regulated system. This makes the two-plane architecture even more relevant: the control plane governs the entire multi-agent cluster, not individual agents. The runtime plane executes across the cluster. Compliance applies to the system, not to each agent independently.

    

Systems without a separate control plane will struggle to demonstrate any of this. Audit trails bolted onto a monolithic agent architecture produce records that say what happened but not why — and the "why" is what the AI Act demands.

    

### Building Your Own Two-Plane Stack

    

Here is the practical deployment pattern I use, which mirrors the emerging standard. It runs on a Hetzner CX33 VPS at €8.49/month and currently executes 19 autonomous cron jobs with 99.7% uptime.

    

Control Plane (runs on Hermes Agent + cron):
    
      
- Policy-as-code in AGENTS.md files — declares what each agent can and cannot do, its permitted tool set, and its budget limits
      
- Watchdog cron + monitor scripts — detect stagnation, iteration overruns, and policy violations; restart, redirect, or escalate
      
- Checkpoint validation — verify resulting state against authorized state before the next execution cycle
      
- SQLite audit log — every authorization, every delegation, every failure, with structured metadata for replay
    

    

Runtime Plane (runs on MCP servers + OpenRouter):
    
      
- MCP tool servers — typed, discoverable, versioned interfaces. Each tool declares its input schema, output schema, and access requirements up front
      
- OpenRouter dynamic routing — select the optimal model per task type. Cheap models for routine classification, frontier models for complex reasoning
      
- SQLite memory — episodic store for session history, semantic store for knowledge triples, procedural store for successful tool chains
      
- Parallel execution via cognitive map-reduce — independent tool calls execute concurrently, bounding total runtime by the critical path rather than the sum of all steps
    

    

This is not a hypothetical architecture. The same principles that NVIDIA applied to 7-day GPU kernel optimization apply at this scale — just with a smaller budget and a shorter horizon.

    

The key difference from a monolithic approach: when a cron job fails, the control plane knows it failed, knows which policy it violated, and knows whether to retry, escalate, or shut down. The runtime plane does not need to make that decision. It just reports the failure. This separation of concerns is what makes autonomous operation maintainable without 24/7 human supervision.

    

### The Emerging Standard

    

The AOS paper captures the convergence best: "AOS does not declare one interpretation invalid. It provides a layered model in which each implementation can state which responsibilities it supplies."

    

The agent architecture landscape is standardizing around this two-plane design. Whether you operate at NVIDIA's scale — 7-day GPU kernel optimization runs on DGX B200 clusters — or at the scale of a single VPS running 19 cron jobs, the architectural pattern is the same. Persistent memory, constraint-based guardrails, and typed tool interfaces are non-negotiable mechanisms. Control and governance separate from runtime and coordination.

    

The convergence is happening faster than most builders realize. Three independent teams, three different problem domains, one architectural answer. Build on the pattern. The industry is converging whether or not individual builders have noticed yet.

    
      🤖 AI-generated — This article was generated with the assistance of an autonomous AI agent (Hermes Agent by Nous Research) and reviewed by Marian Stancik before publication. Full disclaimer.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
