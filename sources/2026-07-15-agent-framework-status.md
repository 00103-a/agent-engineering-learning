# 2026-07-15 Agent 框架状态记录

## 记录目的

本文件只保存调整学习路线所需的版本事实，避免把某个框架的当前热度误写成长期能力。

## 已核实事实

- LangGraph 在 2026 年仍维护并发布 1.2.x 版本。
- LangGraph 当前文档仍把 Persistence、Checkpoint、Interrupt、Resume 和 Human-in-the-loop 作为核心能力。
- OpenAI Agents SDK 当前覆盖 Agent Loop、Runner、工具调用、Session、Tracing、使用量跟踪和可恢复执行集成。
- 两套框架的 API 和运行载体不同，但都在解决状态、工具、终止、持久化、恢复和可观测问题。

## 学习决策

- 不把 LangGraph、OpenAI Agents SDK 或其他框架写成永久主线。
- 在进入框架阶段时重新检查维护活跃度、岗位需求、文档质量和项目适配度。
- 只深入一个当前主框架，其他框架用于对照同一组稳定抽象。
- 框架被替代时更新映射和案例，不推翻 Python、状态机、工具契约、持久化和测试基础。

## 官方来源

- LangGraph releases: https://github.com/langchain-ai/langgraph/releases
- LangGraph interrupts: https://docs.langchain.com/oss/python/langgraph/interrupts
- LangGraph persistence: https://docs.langchain.com/oss/javascript/langgraph/persistence
- OpenAI Agents SDK running agents: https://openai.github.io/openai-agents-python/running_agents/
- OpenAI Agents SDK tracing: https://openai.github.io/openai-agents-python/tracing/
- OpenAI Agents SDK sessions: https://openai.github.io/openai-agents-python/sessions/
