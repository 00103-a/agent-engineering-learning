# smolagents: Agent Loop

## Core modules

- `agents.py`: lifecycle and control loop
- `tools.py`: tool definitions, schemas, and argument validation
- `models.py`: provider-independent model interface
- `memory.py`: structured execution steps
- `monitoring.py`: logging, callbacks, timing, and token usage
- `local_python_executor.py` and `remote_executors.py`: CodeAgent execution environments

## Main class hierarchy

```text
MultiStepAgent
|- ToolCallingAgent
`- CodeAgent
```

`MultiStepAgent` owns the lifecycle. Subclasses implement how one action step is produced and executed through `_step_stream()`.

## Execution path

```text
run(task)
`- _run_stream(task, max_steps)
   |- optional _generate_planning_step()
   `- _step_stream(action_step)
      |- write_memory_to_messages()
      |- model.generate(..., tools_to_call_from=...)
      |- parse tool calls
      |- process_tool_calls()
      |  `- execute_tool_call()
      |     |- check tool name
      |     |- substitute state variables
      |     |- validate arguments
      |     `- invoke tool
      |- store observations or errors in ActionStep
      `- detect final_answer
```

## Lifecycle

`run()` performs the following work:

1. Select the effective maximum step count.
2. Set the current task and clear the interrupt flag.
3. Merge additional arguments into transient state.
4. Optionally reset memory and monitoring.
5. Append a `TaskStep`.
6. Consume `_run_stream()` until a `FinalAnswerStep` is produced.
7. Optionally aggregate steps, token usage, timing, and status into `RunResult`.

## Memory model

The memory is a structured execution trace, not long-term user memory.

Important step types:

- `SystemPromptStep`
- `TaskStep`
- `PlanningStep`
- `ActionStep`
- `FinalAnswerStep`

An `ActionStep` can record model input, model output, tool calls, observations, errors, token usage, timing, action output, and final-answer status.

Each step implements `to_messages()`. This separates internal trace representation from the messages sent back to the model.

## ToolCallingAgent step

One `_step_stream()` iteration:

1. Convert memory into model messages.
2. Ask the model to generate with available tools and managed agents.
3. Parse native or text-derived tool calls.
4. Validate and execute each tool call.
5. Run independent calls concurrently when several calls are returned.
6. Store observations in the current `ActionStep`.
7. Treat the `final_answer` tool as an explicit termination signal.

## Tool execution safeguards

`execute_tool_call()` checks:

- The requested tool exists.
- State-variable references are substituted.
- Arguments conform to the tool schema.
- Execution failures are wrapped as agent-specific errors.

Tool errors are written back into memory as tool responses. The next model call can then change arguments or choose another tool.

## Termination

Normal termination occurs when the model calls `final_answer` and all configured final-answer checks pass.

If the maximum step count is reached, the framework records `AgentMaxStepsError` and asks the model to produce a fallback answer from the existing trace.

## Planning

Planning is optional and controlled by `planning_interval`.

- At the first scheduled planning step, the model creates an initial plan.
- At later intervals, summary mode removes some earlier planning material and asks for an updated plan using remaining steps and current evidence.

Planning is therefore an auxiliary periodic operation, not the core loop itself.

## ToolCallingAgent versus CodeAgent

`ToolCallingAgent` expresses actions as structured function calls. It is easier to validate, constrain, and audit.

`CodeAgent` expresses actions as generated Python code. It supports richer composition and data processing but requires restricted imports and an isolated executor.

## Engineering observations

- An agent is an application-controlled loop around repeated model calls.
- Explicit termination is safer than inferring completion from prose.
- Execution errors become observations, enabling model-level correction.
- `max_steps` is both a reliability boundary and a cost boundary.
- Concurrent tool calls require semantic independence, not only technical concurrency.
- Current memory is an in-process trace; durable state and long-term memory require additional infrastructure.

