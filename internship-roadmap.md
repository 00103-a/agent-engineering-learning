# Internship-Oriented Agent Engineering Roadmap

## Positioning

The full engineering map describes the concerns of a mature agent platform. It is not a checklist to implement in parallel. The learning sequence should maximize demonstrable engineering ability for an internship while preserving a path toward deeper infrastructure work.

## Priority 0: Build Python-for-Agent fluency

The 2026-07-15 preflight showed that the learner can follow agent control flow but still needs guided practice with dictionaries, dataclasses, function contracts, exceptions, async execution, and pytest. These foundations should be trained through small agent components before framework runtime source becomes the main material.

Progress through three levels:

1. Read and modify a focused implementation.
2. Complete an implementation from interfaces, tests, and graded hints.
3. Rebuild it without the previous solution and explain the trade-offs.

Passing tests after line-by-line guidance is evidence of understanding, not yet evidence of independent implementation.

AI-assisted implementation is expected, but ownership must remain explicit. Boilerplate, UI styling, configuration, and routine API glue may be AI-led. Agent loops, failure boundaries, context selection, and evaluation logic require the learner to predict behavior, modify at least one path, verify it with tests, and explain the trade-offs.

## Priority 1: Build and explain one reliable agent path

Study and implement together:

- Minimal tool-calling loop
- Typed tool inputs and outputs
- Argument validation
- Error classification
- Timeout and bounded retry
- Structured run and step logs
- Deterministic tests using fake models and fake tools

The custom runtime is an X-ray exercise, not a replacement framework or primary portfolio claim. Its purpose is to expose what frameworks hide.

## Priority 2: Context and memory with evaluation

Study context and memory as one data lifecycle:

```text
raw events
-> selection and normalization
-> working context
-> derived memory
-> retrieval
-> model decision
-> user or evaluator feedback
```

Required topics:

- Working context versus persisted memory
- Episodic events versus derived semantic profile
- Selection, compaction, recency, and provenance
- Memory write policy, expiry, correction, and deletion
- Retrieval quality and context usefulness
- A small evaluation dataset that measures whether memory improves decisions

Memory without evaluation is only additional storage and prompt complexity.

## Priority 3: Observability as a development tool

Implement a small but real trace model:

- `run_id` and `step_id`
- Model latency and token usage
- Tool name, arguments summary, duration, status, and error class
- Final run status
- Replayable structured events

OpenTelemetry integration can follow later. The immediate goal is to answer: what happened, where did it fail, and did a change improve it?

## Priority 4: Learn one current mainstream orchestration framework

Choose the primary framework when this phase begins, based on current maintenance, job relevance, documentation, and fit for the target workflow. LangGraph is a current candidate, not a permanent commitment. Use it only after understanding the minimal loop.

Focus on:

- Typed state
- Conditional transitions
- Checkpoints
- Interrupt and resume
- Human approval
- Failure recovery

Do not prioritize memorizing decorators or vendor-specific deployment APIs. The durable outputs are typed state, conditional transitions, checkpoints, interrupts, approvals, recovery, and traceability; remap these concepts if the selected framework changes.

## Priority 5: Selective production engineering

Implement now:

- FastAPI service boundaries
- PostgreSQL persistence
- Redis only for a demonstrated cache, queue, or coordination need
- Docker
- Configuration and secret handling
- Unit and integration tests
- Basic CI

Understand but defer until needed:

- Distributed leases
- Multi-worker task ownership
- Kubernetes sandbox provisioners
- Complex multi-agent scheduling
- Large-scale event buses

Full-stack learning begins as a light companion to the Agent track instead of a separate prerequisite. During the foundation stage, the learner only needs to understand and modify thin HTTP and UI integrations with AI assistance. Independent React, database, and deployment fluency is deferred until the Agent core reaches transferable proficiency.

## Priority 6: Protocol literacy

Treat MCP as a current mainstream interoperability convention, not an immutable foundation.

Build one small MCP server to understand tools, resources, transports, and authorization boundaries. Do not migrate an application to MCP without a real interoperability requirement.

A2A and ACP remain conceptual until cross-agent or cross-host boundaries appear.

## Minimum security baseline

Even a small project should distinguish read-only and side-effecting tools.

Implement or model explicitly:

- Tool side-effect metadata
- Approval requirement for privileged actions
- Secret isolation
- Argument validation
- Audit events

Full capability systems and container sandboxes can be deferred, but the boundaries must be visible in the design.

## Learning order

```text
0. Python-for-Agent components: contracts, errors, async, and tests
1. Minimal loop + tool contract + deterministic tests
2. Independent rebuild of the minimal runtime
3. Structured traces
4. Context selection and compaction
5. Memory layers and write/retrieval policy
6. Context/memory evaluation dataset
7. LangGraph state, checkpoints, and interrupts
8. Small MCP implementation
9. Architecture study of long-running harnesses
```

## Portfolio evidence

A portfolio project should demonstrate:

- A concrete user workflow
- Typed tools and structured outputs
- Failure handling and bounded execution
- Context and memory design with explicit policies
- Reproducible tests and eval cases
- Traceable execution
- Clear architecture documentation and tradeoff analysis

It does not need to implement every concern of a distributed agent platform.
