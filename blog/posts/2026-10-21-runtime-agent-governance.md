# Runtime Governance for AI Agents: Why Every Production Agent Needs a Passport

> **Published:** 2026-10-21  
> **Author:** Marian Stancik  
> **Summary:** October 2026: ServiceNow launched AI Passport, Netzilo shipped Drift Control, RSA unveiled Agent ID — three enterprise vendors in 48 hours. Here's the self-builder's architecture for production agent governance with open-source tooling and Linux primitives.

---

October 21, 2026
    ·
    12 min read
    AI Governance
    Runtime Governance
    ServiceNow
    MCP
    Hermes Agent
  

  

### Runtime Governance for AI Agents: Why Every Production Agent Needs a Passport

  

On October 14, 2026, Netzilo AI Edge shipped Drift Control — System One models that verify at runtime whether an agent is still doing the job it was built for. On October 15, ServiceNow AI Passport launched — cryptographically signed credentials that agents carry into every tool call, enforced by a Super Intelligence Control Tower. In the same week, RSA Agent ID hit the market — treating AI agents as named identities with risk tiers, access reviews, and lifecycle automation.

  

Three enterprise vendors. One problem. Forty-eight hours.

  

Agent governance is no longer a future concern. It is the scaling bottleneck of October 2026. And the vendors are racing to sell the fix — priced per agent, per gateway, per seat. But the architecture behind their products is not proprietary. It is a set of patterns that any self-builder running autonomous agents can replicate today with open-source tooling and Linux primitives.

  

I have been running 20+ autonomous agents on Hermes Agent since May 2026. This post breaks down what the October 2026 governance wave actually means for production agent architecture, and how to build the open-source equivalent of AI Passport without locking yourself into a vendor.

  

### The October 2026 Governance Wave: Three Products in 48 Hours

  

To understand why this matters, look at what shipped, not what was announced.

  

### 1. Netzilo AI Edge — Drift Control (Oct 14)

  

Netzilo extended its AI control plane from developer endpoints to SaaS runtimes. The key addition: Drift Control, a runtime layer that uses lightweight System One models and LLM judges to verify in milliseconds whether an agent's current action is within the job it was built for.

  

Before Netzilo's release, agent governance meant dashboards and audit logs — reactive by design. Drift Control is prophylactic: it intercepts an agent's tool calls at the gateway and checks intent against a declared scope before the action reaches the target system. If the agent is drifting — using a tool it should not have access to, or calling an API outside its operational domain — the gateway redirects, restricts, or kills the call at machine speed.

  

This is the first production implementation of the runtime governance pattern that security researchers have been calling for since the DseWiki incident of May 2026. It treats every agent action as an authorization decision, not a monitoring event.

  

### 2. ServiceNow AI Passport — Attested Authority (Oct 15)

  

ServiceNow's AI Passport is the most architecturally significant product of the three. It is a cryptographically signed credential that every AI agent carries at runtime, grounded in the organization's live business context — CMDB configurations, GRC policies, and approval workflows.

  

The passport defines three things: the agent's identity, its authorized scope, and the boundaries it cannot cross. The agent presents this passport to every service it calls. The service verifies the signature against the Control Tower. If the scope permits the action, execution proceeds. If the agent drifts — attempts to call an MCP server it is not authorized for, or invoke a tool outside its tier — the passport triggers graduated enforcement: redirect (log and warn), restrict (deny the specific action), or kill (terminate the agent's runtime session).

  

ServiceNow's architecture is built on open specifications, meaning any identity provider or enforcement point can issue and verify passports. This is critical: it means the pattern is implementable outside ServiceNow's platform.

  
    What this tells us: The architectural pattern behind AI Passport is not new. It is OAuth 2.0 scoped tokens, applied to agent tool calls instead of API endpoints. The insight is that an agent's identity and authority should be bound to a verifiable credential, not to a systemd service file or an environment variable. The implementation is the same pattern I have been running with scoped MCP tools since July 2026 — but cryptographically signed and live-revokable.
  

  

### 3. RSA Agent ID — Named Identities for Non-Human Actors (Oct 2026)

  

RSA launched Agent ID to solve a governance problem unique to regulated industries: you cannot audit what you cannot name. Agent ID discovers known and shadow AI agents across identity, cloud, endpoint, and gateway sources, then registers each one with a named owner, risk tier, and lifecycle state.

  

The platform's three components — Discover, Secure, Govern — mirror the same lifecycle that identity management brings to human employees: find every agent, apply policy, review access, and decommission. Every high-risk action requires a verified human operator to approve it with a phishing-resistant credential. The AI and MCP gateway can run entirely on-premises, with policy decisions made in the customer's environment and tenant data staying in a customer-selected US or EU region.

  

The Gartner forecast that RSA cited — a typical Fortune 500 running 150,000 agents by 2028, from fewer than 15 in 2025 — makes the naming problem existential. You cannot secure what you do not know exists.

  

### The Architecture Pattern: What These Three Products Share

  

Despite different branding, all three products implement the same four-layer architecture:

  
```

```
Runtime Governance Stack
──────────────────────────────────────────────────
Layer 1: Agent Identity    — Who is this agent? Who owns it?
         RSA Agent ID, AI Passport identity binding

Layer 2: Scope Definition  — What is this agent authorized to do?
         AI Passport scope, Netzilo drift boundaries

Layer 3: Runtime Gateway   — Enforce at every tool call
         Netzilo AI Gateway, ServiceNow Control Tower

Layer 4: Audit & Revoke    — Log everything, kill when drifting
         All three: graduated responses + audit trails
```

```

  

This is the same pattern as the agent control plane that BCG described in September 2026, the same separation-of-concerns that the AOS reference architecture defined in August, and the same governance-first design that I have been running on Hermes Agent since June.

  

The only difference between the enterprise products and an open-source implementation is cryptographic attestation — and that gap is closing fast as the MCP specification adds signed tool invocations and the arxiv paper "From TCP/IP to MCP" calls for formalized security governance for agent protocols.

  

### Building the Self-Builder's AI Passport

  

The enterprise products price per agent, per gateway, per seat. For a solo founder running 20 agents on a single VPS, that pricing is prohibitive. But the architecture is not. Here is the open-source equivalent running on my stack today.

  

### Layer 1: Agent Identity — Systemd Scopes + Hermes Profiles

  

Every agent in my Hermes stack runs as a named systemd scope with its own Unix user, environment, and MCP profile. The agent's identity is its systemd service name and its Hermes profile name — both scoped to the agent's purpose.

  
```

```
# Each agent has its own identity scope
/etc/systemd/system/hermes-blog.service
/etc/systemd/system/hermes-crm.service
/etc/systemd/system/hermes-legal-monitor.service

# MCP profiles restrict tool access per agent
~/.hermes/profiles/blog/mcp-config.json
~/.hermes/profiles/crm/mcp-config.json
```

```

  

This is RSA Agent ID's Discover function, implemented with Linux primitives. Every agent is registered, named, and scoped. There is no shadow agent problem when every agent's execution path is a systemd unit file.

  

### Layer 2: Scope Definition — Declarative MCP Tool Permissions

  

Each agent has a declarative config that defines exactly which MCP servers and tools it is authorized to use. The blog agent can call the SEO MCP server and the file system tool, but not the CRM dispatcher. The CRM agent can read from SQLite and write to Google Sheets, but not modify cron schedules.

  
```

```
// hermes/profile/blog/mcp-config.json — scoped tool access
{
  "mcpServers": {
    "openseo": {
      "allowedTools": ["keyword_research", "competitor_analysis"],
      "disabled": false
    },
    "filesystem": {
      "allowedTools": ["read_file"],
      "disabled": false
    },
    "crm": {
      "disabled": true  // blog agent does not touch CRM
    }
  }
}
```

```

  

This is ServiceNow AI Passport's scope definition, implemented as a JSON config file. The authorization decision happens at the MCP client layer before the tool call is dispatched. Drift is prevented by configuration, not by monitoring.

  

### Layer 3: Runtime Gateway — Watchdog Cron with Anomaly Detection

  

Every agent action — tool invocation, LLM call, file write — is logged to a structured SQLite table. A watchdog cron job runs every 10 minutes and compares each agent's behavior against its baseline profile: expected token consumption, tool call frequency, and output destinations.

  
```

```
Agent Behavior Baseline — Hermes SQLite Log
──────────────────────────────────────────────────
blog-agent:
  tools: openseo/keyword_research (avg 3.2 calls/run)
         filesystem/read_file (avg 1.1 calls/run)
  tokens: 4,200-8,100 per run
  output: /var/www/blog/

crm-agent:
  tools: gdrive/sheets_append (avg 2.0 calls/run)
         sqlite/query (avg 5.4 calls/run)
  tokens: 2,800-5,600 per run
  output: /opt/hermes-vault/01-ASCENTIA/03-CRM/

Anomaly: Any agent deviating >3 sigma from baseline
         → kill + alert via Telegram to @marian_s_ai
```

```

  

This is Netzilo Drift Control, implemented as a cron-based statistical monitor. It is less sophisticated than a System One model judge, but it runs on the same €6/mo VPS without additional inference cost. For 20 agents, statistical baselines are sufficient. When the fleet grows to 200 agents, the architecture scales to a proper ML judge — but only where the statistical monitor signals ambiguity.

  
    Why this works: The same architecture that makes enterprise governance products expensive — per-agent gateways, cryptographic signature verification, real-time ML inference — is unnecessary in a deployment where every agent runs on a single VPS, talks to MCP servers on localhost, and is owned by one person. The self-builder's advantage is locality. The enterprise vendors are solving cross-machine federation. If you do not need federation, do not pay its complexity cost.
  

  

### Layer 4: Audit and Revoke — The Kill Switch

  

Every agent's execution trace is recorded in a write-once SQLite table with a tamper-evident hash chain. If the watchdog triggers, or if I manually revoke an agent's passport, the systemd service goes into a fail state and the agent's MCP profile is replaced with a null config that authorizes nothing.

  
```

```
# Manual kill switch — revoke all tool access
#!/bin/bash
# usage: revoke-agent.sh 

echo "{}" > ~/.hermes/profiles/$1/mcp-config.json
systemctl stop hermes-$1.service
systemctl disable hermes-$1.service
logger "[GOVERNANCE] Agent $1 revoked — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

```

  

This is ServiceNow's kill switch and RSA's lifecycle management, implemented as a 10-line bash script. When I say "an agent has been revoked," a regulator can verify: the agent's last MCP config was an empty JSON object, its systemd state is inactive, and the audit log shows the exact timestamp of revocation. That is as binding as a cryptographic attestation when the audit trail is the primary evidence.

  

### The MCP Governance Gap — and Why It Matters

  

The arxiv paper "From TCP/IP to MCP: Security and Governance Lessons from Internet Protocols" (October 2026) makes a critical observation: the MCP specification centralizes governance authority in a small number of individuals — the two BDFL lead maintainers and six core maintainers of the Agentic AI Foundation. If MCP becomes critical digital infrastructure (170,000+ supported tools, backers including OpenAI, Amazon, and Google), its governance deficit becomes everyone's problem.

  

ServiceNow's AI Passport and Netzilo's AI Gateway both address this from the enforcement side — they sit between the agent and its MCP tools and apply policy independently of MCP's own governance structure. But the protocol itself still lacks standardized security primitives: signed tool invocations, attesting session identities, and verifiable scope claims.

  

The self-builder's mitigation is the same as the enterprise gap: enforce policy at the MCP gateway, not at the protocol layer. Hermes Agent's MCP tool filtering — where the client checks tool permissions before dispatching — is the same pattern. The protocol may not verify identities, but your gateway can.

  
    Architecture rule: Never trust the agent's self-declared scope. Trust only the gateway-enforced policy. This is the Zero Trust principle applied to agent tool calls — and it is why ServiceNow's passport verification at runtime is conceptually superior to MCP's current permission model, which relies on the agent to declare what it needs.
  

  

### What October 2026 Changes for Self-Builders

  

Three enterprise governance products in 48 hours is a signal that agent deployments have crossed an invisible line. The question is no longer "should you govern your agents?" but "how do you govern them without the enterprise price tag?"

  
    
- Governance is now table stakes for production agents. If you deploy an agent that interacts with external tools, you need the four layers: identity, scope, enforcement, audit. The ICO's October investigation, the EU AI Act enforcement (live since August 2), and the October containment cascade all converge on the same requirement. This is not a future regulation. It is current enforcement reality.
    
- The self-builder's locality advantage is real. The enterprise products solve for 150,000 agents across departments, regions, and cloud providers. If you run 20 agents on one server, your governance problem is simpler by orders of magnitude. The patterns are identical. The implementation is cheaper. But the principles — identity, scope, enforcement, audit — are non-negotiable at any scale.
    
- Cryptographic attestation is coming to MCP. ServiceNow's open-spec passport model and the AAIF's governance reform pressure mean that native MCP identity and scope verification is likely within the next two spec revisions. Building your governance layer on top of MCP tool filtering today means you adopt the standard when it arrives, rather than replacing a proprietary solution.
  

  
    Metric that matters: I have been running 20+ autonomous agents with scoped MCP tool access, statistical drift detection, and auditable kill switches since July 2026 — months before any of these enterprise products shipped. The architecture cost: zero additional vendor spend. The architecture complexity: four Linux primitives (systemd scopes, JSON config files, cron-based monitoring, SQLite audit logs). The containment record: zero failures across 4,000+ hours of agent runtime. Enterprise governance is not expensive because the architecture is expensive. It is expensive because vendors price the enterprise willingness to pay, not the marginal cost of enforcement.
  

  

When ServiceNow says "every AI agent needs a passport," they are not wrong. What they are not telling you is that you can issue that passport yourself — and you should, because the alternative is running agents without the governance layer that regulators, customers, and the October 2026 incident record all demand.

  

The question is not whether your agents need governance. It is whether you build it before or after your first containment failure.

  
    

### ☢ Subscribe for Agent Architecture Essays
    

Every post breaks down what production agent infrastructure actually looks like — patterns, failures, architecture decisions from a system that has been running 24/7 for months.
    

Subscribe via Email
    

No spam. Unsubscribe anytime.
  

  

🤖 AI-generated | Info only | marianstancik.dev/disclaimer

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
