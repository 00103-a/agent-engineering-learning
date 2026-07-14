from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol


class TransientToolError(Exception):
    """A temporary failure that may succeed on a later attempt."""


class PermanentToolError(Exception):
    """A failure that retrying with the same arguments cannot fix."""


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
        """Register a unique, non-empty tool name."""
        # TODO: Reject empty names and duplicate registrations.
        raise NotImplementedError

    def get(self, name: str) -> ToolSpec:
        """Return a tool or raise KeyError for an unknown name."""
        # TODO: Implement lookup.
        raise NotImplementedError


async def execute_tool(spec: ToolSpec, arguments: dict[str, Any]) -> ToolExecution:
    """Execute a tool with timeout and bounded retries.

    Retry TransientToolError and asyncio.TimeoutError up to max_retries.
    Do not retry PermanentToolError. Unexpected exceptions are classified as
    unexpected and are not retried.
    """
    # TODO: Implement attempts, timeout, retry, and error classification.
    raise NotImplementedError


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
        """Run until final_answer or max_steps is reached.

        Unknown tools and tool execution failures must be recorded in the
        current Step so that the next model call can observe them.
        """
        # TODO: Implement the bounded agent loop.
        raise NotImplementedError
