# Interactive Source-Learning Protocol

## Goal

Turn repository reading into the ability to locate, explain, implement, test, and critique agent infrastructure.

## Lesson loop

### 1. Orient

Define one concrete engineering question and identify no more than three source files and five symbols relevant to it.

### 2. Predict

Show a short source excerpt or interface before explaining it. The learner predicts control flow, state changes, output, and failure behavior.

### 3. Trace

Walk one concrete input through the real call chain. Record function calls, state mutations, emitted events, and termination conditions.

### 4. Rebuild

Implement a framework-independent minimal version. Prefer incomplete starter code with explicit TODOs over a finished solution.

### 5. Test

Write and run tests for the success path and at least two failure paths. Use fake models and fake tools so tests are deterministic and inexpensive.

### 6. Compare

Compare the learner implementation with the repository implementation. Identify what the framework adds, hides, or constrains.

### 7. Critique

Evaluate portability, reliability, security, observability, and scalability. Distinguish tutorial shortcuts from production requirements.

### 8. Consolidate

The learner explains the mechanism in their own words and answers a small interview-style question. Store verified conclusions and unresolved questions in the knowledge base.

## Teaching constraints

- Do not lead with a long prose explanation.
- Use source excerpts small enough to reason about locally.
- Ask for a prediction before revealing behavior when practical.
- Give one primary coding task per lesson.
- Keep framework-specific syntax secondary to stable abstractions.
- Do not add project-specific mappings unless requested.
- Do not silently complete the learner's exercise before they attempt it.
- When the learner is blocked, provide the smallest useful hint first.

## Evidence of learning

A topic is complete only when the learner can:

1. Locate the relevant source symbols.
2. Trace one successful and one failed execution.
3. Implement the core abstraction without the source framework.
4. Test it with deterministic doubles.
5. Explain one design tradeoff in an interview-ready form.

