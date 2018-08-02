import aiohttp
from aiomultiprocess import Process, Pool
import multiprocessing
import asyncio
import time
import uuid

async def fetch(url):
    # return await request("GET", url)

    async with aiohttp.ClientSession() as session:
        async with session.get("{url}".format(url=url)) as resp:
            # async with session.get("{url}/{uuid}".format(url=url, uuid=uuid.uuid4())) as resp:
            # print(resp.status)
            return (resp.status, await resp.json())

async def run_aiomultiprocess(req_num=10):
    # urls = ["http://localhost:8000/", ...]
    urls = ["http://localhost:8000"]*req_num
    start = time.time()
    async with Pool(processes=(multiprocessing.cpu_count()-1)) as pool:
        results = await pool.map(fetch, urls)
        # print(results)
        print("Num of results = ", len(list(results)))

    end = time.time()
    total_time = end - start
    # req_per_sec = total_time/60
    print("time = ", total_time)

async def run_async_only(req_num=10):
    urls = ["http://localhost:8000", ...]
    # tasks = [fetch(urls[0])]*req_num
    tasks = [fetch(urls[0]) for x in range(0,req_num)]
    start = time.time()
    results = asyncio.gather(*tasks)
    results = await results
    print(results)
    end = time.time()
    total_time = end - start
    # req_per_sec = total_time/60
    print("Num of results = ", len(list(results)))
    print("time = ", total_time)

# if __name__ == "__main__":

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_async_only(req_num=5000))
    loop.run_until_complete(run_aiomultiprocess(req_num=5000))
    loop.close()