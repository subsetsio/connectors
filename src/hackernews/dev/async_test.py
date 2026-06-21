import asyncio
import time
import httpx
from nodes.hackernews import _afetch_range, _parse_item, USER_AGENT, CONCURRENCY


async def main():
    limits = httpx.Limits(max_connections=CONCURRENCY, max_keepalive_connections=CONCURRENCY)
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=10.0),
                                 limits=limits, headers={"User-Agent": USER_AGENT}) as client:
        sem = asyncio.Semaphore(CONCURRENCY)
        t0 = time.time()
        rows = await _afetch_range(client, sem, 1, 5000)
        dt = time.time() - t0
        print(f"fetched {len(rows)} non-null of 5000 in {dt:.1f}s ({5000/dt:.0f}/s)")
        types = {}
        for r in rows:
            types[r["type"]] = types.get(r["type"], 0) + 1
        print("types:", types)
        print("sample:", {k: rows[0][k] for k in ("id", "type", "by", "time", "kids")})


asyncio.run(main())
