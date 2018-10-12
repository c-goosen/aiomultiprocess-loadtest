import aiohttp
from aiomultiprocess import Process, Pool
import multiprocessing
import asyncio
import time
import uuid
import random
import string
from itertools import chain

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
    urls_root = ["http://localhost:8000"]*int(req_num/2)
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
    print("time = ", total_time)
    print(len(list(results))/total_time, "req/s")


async def run_async_only(req_num=10):
    urls_root = ["http://localhost:8000"]*int((req_num / 2))
    # urls_query = ['http://localhost:8000/complaints/{}'.format(
    #     await id_generator()) for x in range(0, int(req_num /2))]
    urls_query = list()
    urls = list(chain(urls_root, urls_query))

    # tasks = [fetch(urls[0])]*req_num
    tasks = [fetch(x) for x in urls]
    start = time.time()
    results = asyncio.gather(*tasks)
    results = await results
    print(results)
    end = time.time()
    total_time = end - start
    # req_per_sec = total_time/60
    print("Num of results = ", len(list(results)))
    print("time = ", total_time)
    print(len(list(results))/total_time, "req/s")

# if __name__ == "__main__":

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_async_only(req_num=100))
    loop.run_until_complete(run_aiomultiprocess(req_num=100))
    loop.close()
