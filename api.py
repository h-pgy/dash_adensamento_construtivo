from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import json

app = FastAPI()
#with open('data.geojson', 'r') as f:
#    data = json.load(f)


@app.get("/data.geojson")
async def get_data(response:Response):

    headers = {'Access-Control-Allow-Origin' : "*"}
    def iterfile():  # 
        with open('data.geojson', mode="rb") as file_like:  # 
            yield from file_like
    return StreamingResponse(iterfile(), media_type="application/geo+json", headers =headers)