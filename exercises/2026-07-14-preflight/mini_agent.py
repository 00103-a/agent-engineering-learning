from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol


class TransientToolError(Exception):
    """暂时性失败：后续尝试可能成功。"""


class PermanentToolError(Exception):
    """永久性失败：使用相同参数重试无法解决。"""


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class ModelReply:
    tool_calls: list[ToolCall] = field(default_factory=list)
    final_answer: str | None = None


@dataclass
class Step:
    index: int
    tool_calls: list[ToolCall] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ToolExecution:
    ok: bool
    attempts: int
    value: Any = None
    error_type: str | None = None
    error_message: str | None = None


@dataclass(frozen=True)
class RunResult:
    status: Literal["success", "max_steps"]
    output: str | None
    steps: list[Step]


class Model(Protocol):
    async def generate(self, task: str, steps: list[Step]) -> ModelReply: ...


ToolHandler = Callable[[dict[str, Any]], Awaitable[Any]]


@dataclass(frozen=True)
class ToolSpec:
    name: str
    handler: ToolHandler
    timeout_seconds: float = 1.0
    max_retries: int = 0


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        """注册一个名称非空且唯一的工具。"""
        if spec.name == "":
            raise ValueError("工具名不能为空")
        if spec.name in self._tools:
            raise ValueError("名称重复")
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec:
        """返回对应工具；名称不存在时抛出 KeyError。"""
        return self._tools[name]


async def execute_tool(spec: ToolSpec, arguments: dict[str, Any]) -> ToolExecution:
    """带超时和有限重试地执行工具。

    对 TransientToolError 和 asyncio.TimeoutError 最多重试 max_retries 次。
    PermanentToolError 不重试。未预期异常归类为 unexpected，也不重试。
    """
    for attempts in range(1, spec.max_retries + 2):
        try:
            value = await asyncio.wait_for(
                spec.handler(arguments),
                timeout=spec.timeout_seconds,
            )
            return ToolExecution(
                ok=True,
                attempts=attempts,
                value=value,
            )
        except PermanentToolError as error:
            return ToolExecution(
                ok=False,
                attempts=attempts,
                error_type="permanent",
                error_message=str(error),
            )
        except TransientToolError as error:
            if attempts == spec.max_retries + 1:
                return ToolExecution(
                    ok=False,
                    attempts=attempts,
                    error_type="transient",
                    error_message=str(error),
                )
        except asyncio.TimeoutError as error:
            if attempts == spec.max_retries + 1:
                return ToolExecution(
                    ok=False,
                    attempts=attempts,
                    error_type="timeout",
                    error_message=str(error),
                )
        except Exception as error:
            return ToolExecution(
                ok=False,
                attempts=attempts,
                error_type="unexpected",
                error_message=str(error),
            )


class MiniAgent:
    def __init__(
        self,
        model: Model,
        registry: ToolRegistry,
        max_steps: int = 5,
    ) -> None:
        if max_steps <= 0:
            raise ValueError("max_steps must be positive")
        self.model = model
        self.registry = registry
        self.max_steps = max_steps

    async def run(self, task: str) -> RunResult:
        """运行到收到 final_answer 或达到 max_steps 为止。

        未知工具和工具执行失败必须记录到当前 Step，
        让下一次模型调用能够看到这些信息。
        """
        steps: list[Step] = []
        for index in range(1, self.max_steps + 1):
            reply = await self.model.generate(task, steps)
            step = Step(index=index, tool_calls=reply.tool_calls)
            steps.append(step)
            if reply.final_answer is not None:
                return RunResult(
                    status="success",
                    output=reply.final_answer,
                    steps=steps,
                )
            for tool_call in reply.tool_calls:
                try:
                    spec = self.registry.get(tool_call.name)
                except KeyError:
                    step.errors.append(f"unknown_tool: {tool_call.name}")
                    continue

                execution = await execute_tool(spec, tool_call.arguments)

                if execution.ok:
                    step.observations.append(str(execution.value))
                else:
                    step.errors.append(
                        f"{execution.error_type}: {execution.error_message}"
                    )
        return RunResult(
            status="max_steps",
            output=None,
            steps=steps,
        )


def validate_weather_arguments(
    arguments: dict[str, Any],
) -> str:
    if "city" not in arguments:
        raise PermanentToolError("必须有 city 参数")
    city = arguments["city"]
    if not isinstance(city, str):
        raise PermanentToolError("city 参数必须是字符串")
    return city
