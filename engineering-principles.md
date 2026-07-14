# Future-Proof Agent Engineering Principles

## Objective

Build agent systems that survive model upgrades, provider changes, framework churn, process restarts, tool failures, and stricter security requirements.

## Stable layers

### Domain layer

Contains business rules and deterministic operations. It must not depend on an agent framework.

### Tool contract layer

Exposes domain operations through typed input and output schemas. Contracts include side-effect level, idempotency behavior, timeout, retry policy, and authorization requirements.

### Agent runtime layer

Owns the execution loop, event stream, state transitions, cancellation, budgets, model calls, tool dispatch, and termination.

### Persistence layer

Stores runs, steps, checkpoints, approvals, tool-call results, and audit events. In-memory message history is not durable execution.

### Model adapter layer

Normalizes provider-specific messages, tool calls, streaming events, usage, and errors. Business logic must not depend directly on a provider response object.

### Observability and evaluation layer

Emits traces and metrics, supports deterministic replay where possible, and evaluates both final outcomes and execution trajectories.

## Non-negotiable runtime properties

- Explicit run and step identifiers
- Typed state and result objects
- Maximum steps, time, token, and monetary budgets
- Cancellation and timeout propagation
- Tool-call idempotency for side effects
- Retry policies based on error class
- Human approval for privileged actions
- Checkpointing and restart recovery
- Structured event and audit logs
- Provider-independent model interface
- Test doubles for models and tools

## Knowledge depreciation test

A topic is core when it remains useful after changing the model provider and agent framework.

A topic is secondary when it mainly teaches one library's decorators, prompt format, or configuration syntax.

Before studying a repository feature, ask:

1. What production failure does this feature prevent?
2. What is its framework-independent abstraction?
3. Which state and invariants does it maintain?
4. How is it tested and observed?
5. Can the design be reimplemented using ordinary Python and standard infrastructure?

