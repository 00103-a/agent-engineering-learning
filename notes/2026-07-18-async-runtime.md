# 2026-07-18 学习记录：异步执行与 Runtime 边界

## 今日目标

把天气参数校验接入真实工具调用链，并理解协程、Task、并发、超时、取消和 Runtime 执行状态之间的关系。

## 已验证实现

- 天气 handler 在业务逻辑前调用 `validate_weather_arguments()`。
- 无效 `city` 参数被转换为 `PermanentToolError`，由 `execute_tool()` 归类为 `permanent`。
- `MiniAgent` 将第一轮工具错误写入 `Step.errors`，Fake Model 在第二轮返回最终答案，整个 Run 可同时满足“第一步失败、最终 success”。
- `MiniAgent.run()` 中 Registry 查找的 `try/except KeyError` 已缩小范围，工具执行继续由 `execute_tool()` 负责异常分类。

## 异步执行结论

- 调用 `async def` 函数只创建 Coroutine；`await` 后才等待最终结果。
- `asyncio.create_task(coroutine)` 将协程注册为由事件循环管理的 Task，可取消、查询状态并稍后等待结果。
- 未被 `await` 或调度的 Coroutine 不会运行；已创建的 Task 在当前协程通过 `await` 让出控制权后可以推进。
- `await task` 主要用于可靠等待 Task 完成并取得结果或异常；刚创建 Task 时，`task.done()` 不保证为 `True`。
- 连续两个 `await` 默认串行执行；`async def` 不会让代码自动并发。
- `asyncio.gather()` 并发调度多个协程，结果按传入顺序返回，而不是按完成顺序。
- `return_exceptions=True` 会把异常对象放进结果列表；结构化 `ToolExecution` 用固定字段表达成功和失败，调用方更容易处理。
- `asyncio.wait_for()` 超时后会取消正在等待的协程并向调用方抛出超时异常；`finally` 仍用于清理本地资源。
- 取消本地 Task 不会撤销已经发生的邮件、订单等外部副作用。

## Runtime 与可靠执行

- LLM 提出 `ToolCall`；Runtime 控制工具白名单、参数校验、超时、重试、取消、状态和预算。
- `max_retries` 限制单次工具执行内部重试，`max_steps` 限制 Agent Loop，两者不能替代全局工具调用预算。
- 聊天历史表示用户意图和对话上下文，不能证明外部副作用是否发生。
- 长任务执行副作用前应持久化 `tool_call_id`、幂等键和 `pending` 状态；恢复时依据状态和外部证据查询或安全重试。
- 用户取消时 Run 可以记录为 `cancelled`，而工具副作用可能处于 `unknown_outcome`，不能无证据标记为成功。

## 今日暴露的薄弱点

- 曾把 `gather()` 的第二个查询重复写成天气查询，需要继续练习变量与任务的顺序对应。
- 对 `RunResult.status`、`RunResult.output`、`Step.observations` 和 `Step.errors` 的层次需要多做执行轨迹推演。
- 缩进调整曾让工具循环退出 Agent Step 循环，说明嵌套控制流还需要独立编码验证。
- 对 Runtime、持久化、`pending` 和执行证据的理解经过具体邮件案例后才建立，暂不视为独立掌握。
- 低状态复习时曾判断已调度 Task 没有运行机会；通过 `create_task()` 与 `await sleep()` 的时间线已修正，后续仍需实际实验巩固。

## 今日提示等级

整体为 B/C：概念推演多为 B，涉及缩进和完整代码结构时需要 C 级结构提示。

## 下一步

1. 不看对话答案，独立写串行 `await`、`gather` 并发和 `wait_for` 超时三个小实验。
2. 为三个实验写结果断言或可观察输出。
3. 复述 Coroutine、Task、ToolExecution、Step 和 RunResult 的职责。
4. 完成后再进入有限重试的独立实现，不直接沿用诊断答案。
