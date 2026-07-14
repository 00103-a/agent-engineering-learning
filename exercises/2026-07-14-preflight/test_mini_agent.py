import asyncio

import pytest

from mini_agent import (
    MiniAgent,
    ModelReply,
    PermanentToolError,
    ToolCall,
    ToolRegistry,
    ToolSpec,
    TransientToolError,
    execute_tool,
)


class ScriptedModel:
    def __init__(self, replies: list[ModelReply]) -> None:
        self.replies = replies
        self.calls = 0

    async def generate(self, task, steps):
        reply = self.replies[self.calls]
        self.calls += 1
        return reply


def test_registry_rejects_invalid_and_duplicate_names():
    async def handler(arguments):
        return arguments

    registry = ToolRegistry()

    with pytest.raises(ValueError):
        registry.register(ToolSpec(name="", handler=handler))

    registry.register(ToolSpec(name="echo", handler=handler))

    with pytest.raises(ValueError):
        registry.register(ToolSpec(name="echo", handler=handler))

    assert registry.get("echo").name == "echo"

    with pytest.raises(KeyError):
        registry.get("missing")


def test_execute_tool_retries_transient_error():
    calls = 0

    async def flaky(arguments):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise TransientToolError("temporary")
        return arguments["value"]

    result = asyncio.run(
        execute_tool(
            ToolSpec(name="flaky", handler=flaky, max_retries=1),
            {"value": 42},
        )
    )

    assert result.ok is True
    assert result.value == 42
    assert result.attempts == 2


def test_execute_tool_does_not_retry_permanent_error():
    calls = 0

    async def broken(arguments):
        nonlocal calls
        calls += 1
        raise PermanentToolError("bad arguments")

    result = asyncio.run(
        execute_tool(
            ToolSpec(name="broken", handler=broken, max_retries=3),
            {},
        )
    )

    assert result.ok is False
    assert result.error_type == "permanent"
    assert result.attempts == 1
    assert calls == 1


def test_execute_tool_retries_timeout_with_a_bound():
    async def slow(arguments):
        await asyncio.sleep(0.05)
        return "late"

    result = asyncio.run(
        execute_tool(
            ToolSpec(
                name="slow",
                handler=slow,
                timeout_seconds=0.001,
                max_retries=1,
            ),
            {},
        )
    )

    assert result.ok is False
    assert result.error_type == "timeout"
    assert result.attempts == 2


def test_agent_executes_tool_then_returns_final_answer():
    async def weather(arguments):
        return f"sunny in {arguments['city']}"

    registry = ToolRegistry()
    registry.register(ToolSpec(name="weather", handler=weather))
    model = ScriptedModel(
        [
            ModelReply(
                tool_calls=[
                    ToolCall(
                        id="call-1",
                        name="weather",
                        arguments={"city": "Nanchang"},
                    )
                ]
            ),
            ModelReply(final_answer="Go outside."),
        ]
    )

    result = asyncio.run(MiniAgent(model, registry).run("Plan my afternoon"))

    assert result.status == "success"
    assert result.output == "Go outside."
    assert len(result.steps) == 2
    assert result.steps[0].observations == ["sunny in Nanchang"]


def test_agent_records_unknown_tool_and_can_recover():
    registry = ToolRegistry()
    model = ScriptedModel(
        [
            ModelReply(
                tool_calls=[
                    ToolCall(id="call-1", name="missing", arguments={})
                ]
            ),
            ModelReply(final_answer="Recovered."),
        ]
    )

    result = asyncio.run(MiniAgent(model, registry).run("Do something"))

    assert result.status == "success"
    assert len(result.steps) == 2
    assert result.steps[0].errors
    assert "unknown_tool" in result.steps[0].errors[0]


def test_agent_stops_at_max_steps():
    registry = ToolRegistry()
    model = ScriptedModel([ModelReply(), ModelReply(), ModelReply()])

    result = asyncio.run(
        MiniAgent(model, registry, max_steps=2).run("Never finishes")
    )

    assert result.status == "max_steps"
    assert result.output is None
    assert len(result.steps) == 2
    assert model.calls == 2
