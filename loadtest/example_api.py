from sanic import Sanic
from sanic import response
import asyncpg
import uuid
import json
import time
app = Sanic()
# pool = await asyncpg.create_pool(user='goose',
#                                  database='pagila', host='127.0.0.1')
# con = await pool.acquire()
# request_count = 0

@app.route("/<req_uuid>")
async def test(request, req_uuid):
    request_count =+ 1
    return response.json({"hello": "world", "uuid": str(req_uuid)})

@app.route("/")
async def root(request):
    request_count =+ 1
    return response.json({"hello": "world", "uuid": str(uuid.uuid4())})

#`@app.route("complaints/")
@app.route("/complaints/<state>")
async def complaints(request, state):
    conn = await asyncpg.connect(user='goose', database='consumer_complaints', host='127.0.0.1')
    # pool = await asyncpg.create_pool(user='goose', database='consumer_complaints', host='127.0.0.1',
    #                                  min_size=2,
    #                                  max_size=2,
    #                                  )
    # conn = await pool.acquire()
    try:
        start = time.time()
        query = '''SELECT index,state,company,product FROM complaints WHERE state LIKE $1 LIMIT 5;'''
        result = await conn.fetch(query, state)
        await conn.close()
        return response.json({
            "data": result,
            "query_received": state,
            "query_time": "% seconds" % (time.time() - start)
        })
    except Exception as e:

        return response.json({
            "error": e
        })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, workers=1)
