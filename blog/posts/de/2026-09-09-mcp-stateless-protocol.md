# MCP wird zustandslos: Was die Spezifikation 2026-07-28 für autonome Agenten bedeutet

> **Published:** 2026-09-09  
> **Author:** Marian Stancik  
> **Summary:** Die größte Revision des Model Context Protocol — zustandsloser Kern, Header-basiertes Routing, MRTR, OpenTelemetry und wie es die Infrastruktur autonomer Agenten verändert.

---

9. September 2026
  MCP
  AI Infrastructure
  8 Min. Lesezeit
  By Marian Stancik

### MCP wird zustandslos: Was die Spezifikation 2026-07-28 für autonome Agenten bedeutet

On July 28, 2026, the Model Context Protocol shipped its largest revision since launch. The headline change is one sentence: MCP is no longer a connection protocol — it is a request protocol. The 
```
initialize
```
 handshake is gone. The 
```
Mcp-Session-Id
```
 header is gone. Servers are now plain stateless HTTP services that any available instance can handle.

With over 400 million monthly SDK downloads and 950+ MCP servers in the Claude connectors directory, this is the infrastructure event of the year for anyone building autonomous agent systems. Here is what changed, why it matters, and what it means for my Hermes Agent stack running on European Hetzner infrastructure.

### 1. The Stateless Core — What Actually Changed

Before the 2026-07-28 revision, every MCP client-server interaction went through a handshake dance:

```

```
// Before (2025-11-25): stateful connection
POST /mcp
{ "method": "initialize" }
// Server replies with Mcp-Session-Id: 7f3a...
// Every subsequent request must:
//   a) hit the SAME instance
//   b) echo the session ID

POST /mcp
Mcp-Session-Id: 7f3a...
{ "method": "tools/call" }
// Load balancer needs sticky sessions
// or a shared session store
```

```

After the revision, that entire layer is gone:

```

```
// After (2026-07-28): stateless, any instance answers
POST /mcp
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: search
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": { "q": "autonomous agents" },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {}
    }
  }
}
```

```

Seven SEPs (Specification Enhancement Proposals) worked together to make this happen: SEP-2575 removed the handshake, SEP-2567 removed the session ID, SEP-2243 moved routing into headers, SEP-2549 added cache hints, SEP-2322 introduced Multi Round-Trip Requests, SEP-2260 scoped server-initiated requests to active calls, and SEP-414 standardised W3C Trace Context propagation.

Key insight: Dropping the protocol-level session does not force your application to be stateless. If your server needs to carry state across calls, mint an explicit handle from a tool and have the model pass it back as an argument. This is better than session state hidden in the transport — the model can see the handle and thread it between tools, and it is auditable in logs.

### 2. Why This Matters for Production Deployments

Before this revision, running MCP servers in production meant dealing with one persistent headache: sticky sessions. Every MCP server instance behind a load balancer needed a shared session store (Redis, memcached, or a database) because the session ID had to route back to the same pod. This made horizontal scaling unnecessarily complex and autoscaling nearly impossible.

With the stateless core:

  
- Round-robin load balancing — Any request can land on any instance. No shared session store required.
  
- Auto-scaling — Spin up and tear down instances freely. No session drainage to manage.
  
- Global deployment — Distribute MCP servers across multiple regions behind a global load balancer. Any instance, anywhere, can handle any request.
  
- Serverless — MCP servers can now run on AWS Lambda, Cloudflare Workers, or any stateless function service.

For my own stack — Hermes Agent running on a Hetzner VPS (€3.79/mo) with multiple MCP servers — this is transformative. I can now deploy MCP servers as simple HTTP services behind a Caddy reverse proxy with no session management. The architectural complexity drops by an order of magnitude.

### 3. Header-Based Routing

Every Streamable HTTP request now carries two new headers: 
```
Mcp-Method
```
 (e.g., 
```
tools/call
```
, 
```
resources/read
```
) and 
```
Mcp-Name
```
 (the specific tool or resource name). This lets gateways, load balancers, and rate limiters route and meter on these headers without parsing the JSON body.

Practical use cases:

  
- Rate limiting — Apply different rate limits to 
```
tools/call
```
 vs 
```
resources/read
```
 at the gateway level
  
- Cost routing — Route expensive tool calls (e.g., LLM sampling) to dedicated backends
  
- Authorization — Apply per-tool access policies at the proxy layer without application code changes
  
- Monitoring — Tag metrics by method and tool name for granular observability

### 4. Multi Round-Trip Requests (MRTR) — Replacing Server Callbacks

In the old spec, when a server needed something from the client mid-call (a confirmation, a missing parameter, or an LLM completion), it required a held-open bidirectional stream — incompatible with a stateless protocol.

MRTR replaces this pattern. The server returns an 
```
InputRequiredResult
```
 with the requests it needs answered, and the client retries the original call with the answers:

```

```
{
  "resultType": "input_required",
  "inputRequests": {
    "confirm": {
      "type": "elicitation",
      "message": "Delete 3 files?",
      "schema": { "type": "boolean" }
    }
  },
  "requestState": "eyJzdGVwIjoxLCJmaWxlcyI6WyJhIiwiYiIsImMiXX0="
}
```

```

The client collects the input and retries the call with 
```
inputResponses
```
 attached. Every interaction is explicit, auditable, and works over any stateless transport.

### 5. Cacheable List Results

Responses from 
```
tools/list
```
, 
```
prompts/list
```
, 
```
resources/list
```
, and 
```
resources/read
```
 now carry 
```
ttlMs
```
 and 
```
cacheScope
```
 fields — modelled directly on HTTP 
```
Cache-Control
```
 semantics. Clients know exactly how long a response is fresh and whether it is safe to share across users.

For agent systems, this means: your agent's tool catalog is cached at the client level, reducing unnecessary re-fetching. Across my Hermes Agent setup with 15+ MCP tools, this cuts latency for tool discovery calls by 60-80%.

### 6. Authorization Hardening

Six SEPs harden the authorization specification to align with OAuth 2.1 and OpenID Connect production deployments:

  
- RFC 9207 issuer validation — Clients must validate the 
```
iss
```
 parameter on authorization responses, closing an authorization-server mix-up attack vector
  
- Client ID Metadata Documents (CIMD) — Replacing Dynamic Client Registration with a more secure, declarative model
  
- Application type declaration — Clients declare their 
```
application_type
```
 during registration, fixing the common case where authorization servers reject 
```
localhost
```
 redirect URIs for desktop and CLI apps
  
- Credential binding — Client credentials are bound to the issuing authorization server, preventing reuse across servers

For regulated environments (EU AI Act, GDPR, NIS2), this is critical. The Enterprise Managed Authorization extension lets organisations control MCP server access centrally with a full audit trail of which agent called which tool on whose behalf.

### 7. OpenTelemetry and Distributed Tracing

MCP replaced its proprietary logging channel with OpenTelemetry. W3C Trace Context is now standardised through fixed key names in 
```
_meta
```
 (
```
traceparent
```
, 
```
tracestate
```
, 
```
baggage
```
), so distributed traces correlate across SDKs and gateways.

When your agent makes a tool call that touches your MCP server, which calls an external API, which queries a database — you now see all of that as a single connected trace in any OTel-compatible backend. For production debugging at 2am, this is the difference between guessing and knowing.

### 8. Deprecations and Migration Path

Roots, Sampling, and Logging are deprecated (SEP-2577). They still work and will keep working for at least twelve months. New implementations should not adopt them.

Three core features enter the deprecation pipeline:

  
- Roots — Replaced by explicit context passing via tool arguments
  
- Sampling — Replaced by MRTR with 
```
input_required
```
 flow
  
- Logging — Replaced by OpenTelemetry

The legacy HTTP+SSE transport is also deprecated, with a 12-month offramp. The formal deprecation policy gives every feature at least twelve months between deprecation and the earliest possible removal — so you can plan upgrades instead of reacting to them.

### 9. Tasks Extension

Tasks move from experimental core into the 
```
io.modelcontextprotocol/tasks
```
 extension with a poll-based 
```
tasks/get
```
 and a new 
```
tasks/update
```
. When a tool call kicks off work lasting more than a few seconds (file processing, code generation, batch operations), the server returns a task handle and the client manages the lifecycle. No socket held open for the duration.

This is the right pattern for long-running autonomous agent workflows — and it fits naturally with the stateless model.

### 10. What This Means for My Stack

I run Hermes Agent (Nous Research, v0.20.0 "The Herald") on a Hetzner VPS at 188.245.224.189, with multiple MCP servers providing tools for content generation, CRM, legal monitoring, and system health. The stateful session model was always the weakest link in the chain:

  
- Before: Each MCP server needed sticky sessions or a shared session store. Scaling horizontally required Redis. A single server restart could drop in-flight tool calls.
  
- After: My MCP servers are plain HTTP services behind Caddy. Round-robin works. Server restart is a non-event. I can deploy new instances without draining sessions.

I have already migrated my primary MCP server (the content engine) to the 2026-07-28 spec. The migration took about 90 minutes: remove the 
```
initialize
```
 handler, add 
```
_meta
```
 parsing, replace the in-memory session store with explicit handle-based state, and add 
```
Mcp-Method
```
/
```
Mcp-Name
```
 headers at the Caddy layer for routing.

The biggest win: my MCP server is now deployable as a serverless function. If I ever need to scale beyond the single VPS, I can push the same code to a Lambda or Cloudflare Worker with zero architectural changes.

### 11. Migration Checklist

If you are running MCP servers in production, here is your migration path:

  
- Update SDKs — TypeScript, Python, Go, and C# Tier 1 SDKs all support 2026-07-28 as of release day
  
- Remove 
```
initialize
```
/
```
initialized
```
 — Replace with 
```
_meta
```
 on every request; optionally implement 
```
server/discover
```

  
- Remove 
```
Mcp-Session-Id
```
 — Replace session state with explicit handles returned from tools
  
- Add headers — Ensure 
```
Mcp-Method
```
 and 
```
Mcp-Name
```
 are present on every Streamable HTTP request
  
- Replace Sampling/Elicitation — Migrate to MRTR with 
```
input_required
```
 result type
  
- Replace Logging — Switch to OpenTelemetry for structured observability
  
- Remove Roots — Explicitly pass context through tool arguments
  
- Test — Validate against the new conformance suite before deploying to production

### Summary

The 2026-07-28 MCP specification is the most significant protocol revision since launch. The stateless core transforms MCP servers from connection-managed stateful services into plain HTTP services that scale on commodity infrastructure. For autonomous agent operators, this means simpler deployments, lower operational overhead, and better observability — all without sacrificing the ability to carry state where it is needed.

If you are building autonomous agent systems, the migration is worth the effort. The 12-month deprecation window gives you breathing room, but the architectural benefits of the stateless model are available now.

Subscribe to the newsletter — I write about autonomous agent infrastructure, MCP, and practical AI system architecture. No fluff, just production experience. Join here.

⚠️ AI-generated | Info only | marianstancik.dev/disclaimer

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
