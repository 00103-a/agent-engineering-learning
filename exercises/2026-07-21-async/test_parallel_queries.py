import asyncio

from parallel_queries import collect_trip_info, safe_query_weather


def test_collect_trip_info() -> None:
    # 使用 asyncio.run 执行 collect_trip_info()
    # 断言结果等于 ("晴天", ["骑行", "看展"])
    result = asyncio.run(collect_trip_info())
    assert result == ("晴天", ["骑行", "看展"])


def test_safe_query_weather() -> None:
    result = asyncio.run(safe_query_weather())
    assert result == (False, None)
