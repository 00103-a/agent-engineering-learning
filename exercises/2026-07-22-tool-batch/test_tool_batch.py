import asyncio

import pytest

from tool_batch import BatchResult, ToolResult, build_batch_result, execute_batch, get_batch_status


def test_execute_batch() -> None:
    weather_result, calendar_result = asyncio.run(execute_batch())
    assert weather_result.call_id == "call-weather"
    assert weather_result.status == "success"
    assert calendar_result.call_id == "call-calendar"
    assert calendar_result.status == "error"
    assert weather_result.value == "晴天"
    assert calendar_result.error == "calendar timeout"
    result = [weather_result, calendar_result]
    batch_status = get_batch_status(result)
    assert batch_status == "partial_success"


def test_get_batch_status_rejects_empty_results() -> None:
    with pytest.raises(ValueError):
        get_batch_status([])


def test_get_batch_status_success() -> None:
    result = [
        ToolResult(call_id="call-weather", status="success", value="yes", error=None),
        ToolResult(call_id="call-calendar", status="success", value="yes", error=None),
    ]
    batch_status = get_batch_status(result)
    batch_result = build_batch_result(result)
    assert batch_status == "success"
    assert batch_result.status == "success"
    assert batch_result.results == result


def test_get_batch_status_error() -> None:
    result = [
        ToolResult(call_id="call-weather", status="error", value=None, error="no"),
        ToolResult(call_id="call-calendar", status="error", value=None, error="no"),
    ]
    batch_status = get_batch_status(result)
    batch_result = build_batch_result(result)
    assert batch_status == "error"
    assert batch_result.status == "error"
    assert batch_result.results == result
