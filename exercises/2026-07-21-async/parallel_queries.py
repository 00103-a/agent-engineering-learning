import asyncio


async def query_weather() -> str:
    print("weather start")
    try:
        await asyncio.sleep(0.2)
        print("weather end")
        return "晴天"
    finally:
        print("weather cleanup")


async def query_activities() -> list[str]:
    print("activities start")
    await asyncio.sleep(0.1)
    print("activities end")
    return ["骑行", "看展"]


async def collect_trip_info() -> tuple[str, list[str]]:
    # 并发执行上面两个函数
    # 返回 (weather, activities)
    weather, activities = await asyncio.gather(
        query_weather(), query_activities()
    )
    return (weather, activities)


async def collect_trip_info_serial() -> tuple[str, list[str]]:
    # 先等待天气查询完成
    # 再等待活动查询完成
    # 返回 (weather, activities)
    weather = await query_weather()
    activities = await query_activities()
    return (weather, activities)


async def query_weather_with_timeout() -> str:
    result = await asyncio.wait_for(
        query_weather(),
        timeout=0.1,
    )
    return result


async def safe_query_weather() -> tuple[bool, str | None]:
    try:
        # 等待 query_weather_with_timeout()
        # 成功时返回 (True, 天气结果)
        result = await query_weather_with_timeout()
        return (True, result)
    except asyncio.TimeoutError:
        # 超时时返回 (False, None)
        return (False, None)


async def collect_in_completion_order() -> list[object]:
    results: list[object] = []

    for completed in asyncio.as_completed([query_weather(), query_activities()]):
        result = await completed
        results.append(result)

    return results

async def run_limited_tool(
    name: str,
    semaphore: asyncio.Semaphore,
    delay: float,
) -> str:
    async with semaphore:
        print(f"{name} start")
        await asyncio.sleep(delay)
        print(f"{name} end")
        return name


async def run_limited_batch() -> list[str]:
    semaphore = asyncio.Semaphore(2)

    results = await asyncio.gather(
        # 分别调用 A、B、C、D
        # 四次调用必须共享同一个 semaphore
        run_limited_tool("A", semaphore, 0.3),
        run_limited_tool("B", semaphore, 0.1),
        run_limited_tool("C", semaphore, 0.1),
        run_limited_tool("D", semaphore, 0.1),
    )

    return list(results)


if __name__ == "__main__":
    result = asyncio.run(run_limited_batch())
    print(result)
