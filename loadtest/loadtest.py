import aiohttp
import httpx
from aiomultiprocess import Pool
import asyncio
import multiprocessing
import os
import random
import string
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from itertools import chain

BASE_URL = os.environ.get("TEST_BASE_URL", "http://127.0.0.1:8000")


def print_runtime():
    gil = sys._is_gil_enabled()
    build = "free-threaded" if "free-threading" in sys.version else "default"
    print(f"Python {sys.version.split()[0]} ({build}) | GIL {'on' if gil else 'off'}")

async def fetch(url):
    # return await request("GET", url)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return (resp.status, await resp.json())

async def id_generator(size=2, chars=string.ascii_uppercase):
    ...
    return ''.join(random.choice(chars) for _ in range(size))

async def run_aiomultiprocess(req_num=10):

    # urls = ["http://localhost:8000/", ...]
    urls_root = [BASE_URL] * int(req_num / 2)
    # urls_query = [ 'http://localhost:8000/complaints/{}'.format(
    #     await id_generator()) for x in range(0,int(req_num/2)
    #                                          )
    # ]
    urls_query = list()
    urls = list(chain(urls_root, urls_query))

    start = time.time()
    async with Pool(processes=(multiprocessing.cpu_count()-1)) as pool:
        results = await pool.map(fetch, urls)
        # print(results)
        print("Num of results = ", len(list(results)))

    end = time.time()
    total_time = end - start
    # req_per_sec = total_time/60
    print("run_aiomultiprocess")
    print("time = ", total_time)
    print(len(list(results))/total_time, "req/s")


async def run_async_only(req_num=10):
    urls_root = [BASE_URL] * int(req_num / 2)
    # urls_query = ['http://localhost:8000/complaints/{}'.format(
    #     await id_generator()) for x in range(0, int(req_num /2))]
    urls_query = list()
    urls = list(chain(urls_root, urls_query))

    # tasks = [fetch(urls[0])]*req_num
    tasks = [fetch(x) for x in urls]
    start = time.time()
    results = asyncio.gather(*tasks)
    results = await results
    end = time.time()
    total_time = end - start
    # req_per_sec = total_time/60
    print("run_async_only")
    print("Num of results = ", len(list(results)))
    print("time = ", total_time)
    print(len(list(results))/total_time, "req/s")


def fetch_sync(url: str) -> tuple[int, object]:
    with httpx.Client() as client:
        response = client.get(url)
        return response.status_code, response.json()


def run_threaded(req_num: int = 10) -> None:
    urls_root = [BASE_URL] * int(req_num / 2)
    urls = list(chain(urls_root, []))
    workers = max(1, multiprocessing.cpu_count() - 1)

    start = time.time()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(fetch_sync, urls))

    total_time = time.time() - start
    print("run_threaded")
    print("Num of results = ", len(results))
    print("time = ", total_time)
    print(len(results) / total_time, "req/s")


if __name__ == "__main__":
    print_runtime()
    # Import stack used by the API server; some C extensions opt back into the GIL.
    import ujson  # noqa: F401

    print_runtime()
    asyncio.run(run_async_only(req_num=2000))
    asyncio.run(run_aiomultiprocess(req_num=2000))
    run_threaded(req_num=2000)
