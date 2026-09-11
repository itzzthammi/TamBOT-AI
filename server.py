import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="TamBOT AI")

app.mount("/static", StaticFiles(directory="static"), name="static")

SYSTEM = """You are TamBOT AI, created by itzz_thammi.
Be warm, confident, witty, intelligent, concise when appropriate, and natural like a human.
Adapt your personality to the situation. Speak the user's language when possible.
Never facilitate child sexual abuse material, serious criminal activity, weapon construction,
or other dangerous wrongdoing. For unsafe requests, refuse briefly and offer a safe alternative.
Do not claim to have performed actions you did not perform."""

class ChatRequest(BaseModel):
    messages: list


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/chat")
def chat(req: ChatRequest):
    key = os.getenv("GEMINI_API_KEY")

    if not key:
        raise HTTPException(500, "GEMINI_API_KEY is not configured on the server.")

    client = OpenAI(
        api_key=key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    def stream():
        response = client.chat.completions.create(
            model="gemini-3.8-flash",
            messages=[
                {"role": "system", "content": SYSTEM},
                *req.messages
            ],
            stream=True
        )

        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    return StreamingResponse(
        stream(),
        media_type="text/plain; charset=utf-8"
    )
