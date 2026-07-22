import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolResult:
    call_id: str
    status: str
    value: Any = None
    error: str | None = None


@dataclass(frozen=True)
class BatchResult:
    status: str
    results: list[ToolResult]

async def query_weather() -> str:
    await asyncio.sleep(0.1)
    return "晴天"


async def query_calendar() -> str:
    await asyncio.sleep(0.1)
    raise RuntimeError("calendar timeout")


async def execute_one(
    call_id: str,
    handler: Callable[[], Awaitable[Any]],
) -> ToolResult:
    try:
        value = await handler()
        return ToolResult(
            call_id=call_id,
            status="success",
            value=value,
            error=None,
        )
    except RuntimeError as error:
        return ToolResult(
            call_id=call_id,
            status="error",
            value=None,
            error=str(error),
        )


async def execute_batch() -> list[ToolResult]:
    weather_result, calendar_result = await asyncio.gather(
        execute_one("call-weather", query_weather),
        execute_one("call-calendar", query_calendar),
    )

    return [weather_result, calendar_result]


def get_batch_status(results: list[ToolResult]) -> str:
    if not results:
        raise ValueError("results must not be empty")

    count_success = 0
    for result in results:
        if result.status == "success":
            count_success += 1

    if count_success == len(results):
        return "success"
    if count_success == 0:
        return "error"
    return "partial_success"


def build_batch_result(results: list[ToolResult]) -> BatchResult:
    status = get_batch_status(results=results)
    return BatchResult(status=status, results=results)


if __name__ == "__main__":
    result = asyncio.run(execute_batch())
    print(result)
