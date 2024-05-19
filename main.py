from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import StreamingResponse, JSONResponse
from openai_types import *
import httpx
import json

DEEPSEEK_BASE_URL = 'https://api.deepseek.com/chat/completions'

app = FastAPI()

async def get_streaming_data(url, request, headers):
    try:
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url=url, data=request, headers=headers, timeout=10.0) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk
    except Exception as e:
        yield b""
        

@app.post("/chat/completions")
async def chat(request: OpenAIRequest, authorization: str = Header(...)):
    try:
        url = DEEPSEEK_BASE_URL

        if request.model == "deepseek-chat":
            request_data = request.model_dump()
            for i in range(len(request_data["messages"])):
                if type(request_data["messages"][i]["content"]) == list :
                    request_data["messages"][i]["content"] = request_data["messages"][i]["content"][0]["text"]
            request = OpenAIRequest.model_validate(request_data)

        headers = {
            "Authorization": authorization,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if not request.stream:
            response = httpx.post(url, headers=headers, json=request.model_dump(), timeout=1.0)
            if response.status_code == 200:
                response_data = response.json()
                return response_data
            else:
                return response.text
        else:
            async def generate(url, request, headers):
                async for chunk in get_streaming_data(url=url, request=request, headers=headers):
                    yield chunk.decode('utf-8').replace(',"role":null', '').encode('utf-8')
            return StreamingResponse(generate(url=url, request=json.dumps(request.model_dump()), headers=headers))
    except Exception as e:
        return JSONResponse(content=str(e), status_code=500)