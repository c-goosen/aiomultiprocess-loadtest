from sanic import Sanic
from sanic.response import json
import uuid

app = Sanic()
# request_count = 0

@app.route("/<req_uuid>")
async def test(request, req_uuid):
    request_count =+ 1
    return json({"hello": "world", "uuid": str(req_uuid)})

@app.route("/")
async def test(request):
    request_count =+ 1
    return json({"hello": "world", "uuid": str(uuid.uuid4())})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=1)