# 2026-07-22 学习记录：工具批次身份、部分失败与 HTTP 入门

## 今日目标

在新的工具场景中保留并发结果身份，处理部分失败并形成批次状态；在完成核心编码后开始第一节轻量全栈知识。

## 已验证的代码练习

- `ToolResult` 使用 `call_id`、`status`、`value` 和 `error` 记录单个工具执行事实。
- 通用 `execute_one()` 接收异步 Handler，将 `RuntimeError` 转换为结构化错误结果。
- `execute_batch()` 使用 `asyncio.gather()` 并发执行天气和日历工具；日历失败不会丢失天气成功结果。
- `get_batch_status()` 区分 `success`、`partial_success` 和 `error`，并拒绝空结果列表。
- `BatchResult` 同时保留总体状态和全部具体结果。

## 测试证据

- 验证成功与失败结果分别保留正确的 `call_id`、状态、值和错误信息。
- 验证部分成功、全部成功和全部失败三条正常分支。
- 使用 `pytest.raises(ValueError)` 验证空结果异常。
- 仓库全量测试为 17 passed；pytest 缓存目录仍有一个不影响结果的 Windows 警告。

## 提示等级

- `call_id` 与部分失败概念：B 级。
- `Callable[[], Awaitable[Any]]`、函数对象传递和 `execute_one()` 包装结构：C 级。
- `get_batch_status()` 最初使用了 Java/C 风格循环，需要 Python 结构提示；修正后能独立完成分支。
- 全成功、全失败测试及 `build_batch_result()`：局部 A 级。
- 整体主题处于 B/C 级向 B 级过渡，不能标记为独立掌握。

## Agent 知识输入

- 工具依赖图决定哪些调用可并发，依赖失败的后续调用应区分 `blocked` 与 `failed`。
- fail-fast、best-effort 和 fallback 是不同失败策略；异常事实与任务终止策略不能混为一谈。
- Trace 保存完整执行事实，Observation 只提供模型下一步决策所需的摘要。
- Agent 评估同时关注最终结果和执行轨迹，不能只看最终答案是否碰巧正确。

以上内容只标记为已接触，尚未实现依赖调度、Trace 或评估器。

## 全栈知识输入

- 客户端/服务端是一次通信中的角色；Agent 后端面对浏览器是服务端，调用模型和工具时又是客户端。
- HTTP `2xx` 表示请求被正常处理，Agent 内部工具失败仍可通过 `200 + partial_success` 表达。
- 一次 `POST /runs` 通常创建一个 Run 并返回一个 `run_id`；Run 内可包含多个 Step 和 ToolCall。
- 长任务可先返回 `202 Accepted`，前端再通过 `GET /runs/{run_id}` 自动轮询，直到 Run 进入终态。
- 轮询会结束第一次 HTTP 请求；它不同于保持连接的 SSE、WebSocket 或流式响应。

全栈部分只标记为已接触，尚未编写 HTTP 接口。

## 下一步

1. 使用新场景实现带 `call_id`、`attempts` 和错误类型的有限重试。
2. 复现 `max_retries` 与总尝试次数的关系。
3. 永久错误立即返回，暂时错误只在预算内重试。
4. 不叠加 Registry、并发批次或 Agent Loop。
