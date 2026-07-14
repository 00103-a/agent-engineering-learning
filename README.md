# 个人 Agent 工程学习知识库

这是本文件夹的统一入口，用于沉淀经过源码核对、实现验证和复盘后的 Agent 工程知识。

## 从这里开始

- [学习设计文档](./00-学习设计文档.md)：目标、边界、能力层次、方法和阶段性成果
- [未来可迁移的工程原则](./engineering-principles.md)：框架变化后仍然成立的设计原则
- [交互式源码学习协议](./learning-method.md)：预测、跟踪、实现、测试、对比和复述
- [实习导向路线](./internship-roadmap.md)：当前优先实现、理解和暂缓的内容

## 仓库学习顺序

1. `smolagents`：最小 Agent Loop、Tool、Memory Step、Code Agent
2. `openai-agents-python`：Runner、Session、Guardrail、Handoff、Tracing
3. `langgraph`：Typed State、Checkpoint、Interrupt、持久执行
4. `pydantic-ai`：类型安全、结构化输出、依赖注入、Evals
5. `modelcontextprotocol/servers`：MCP 工具、资源、传输与安全边界
6. `deer-flow`：长任务 Harness、Sandbox、Skills、Subagents、Gateway
7. `hermes-agent`：个人 Agent、长期记忆、Cron、Skills、消息入口

仓库是设计证据和实现案例，不是要求逐行读完的教材。

## 知识库规则

- 优先读取并扩充本地笔记，不重复进行相同搜索。
- 只有源码细节缺失、版本变化或结论需要核实时才访问外部资料。
- 明确区分源码事实、个人分析和未来预测。
- 框架 API 只是案例，学习目标是可迁移的工程抽象。
- 优先使用 JSON Schema、HTTP、SQL、MCP、OpenTelemetry、类型化 Python 等标准能力。
- 每项实现都应显式考虑状态、错误、预算、权限和测试入口。
- 默认不读取或修改 DayAgent，也不添加 DayAgent 映射，除非用户明确要求。

## 当前状态

学习边界与路线已经确定，当前进入课前诊断阶段：

- [课前诊断说明](./lessons/2026-07-14-课前诊断.md)
- [诊断答题记录](./notes/2026-07-14-preflight-answers.md)
- [Mini Agent 编码练习](./exercises/2026-07-14-preflight/mini_agent.py)

