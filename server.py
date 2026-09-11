import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai

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
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured on the server."
        )

    client = genai.Client(api_key=key)

    conversation = SYSTEM + "\n\n"

    for message in req.messages:
        role = message.get("role", "user")
        content = message.get("content", "")

        if role == "user":
            conversation += f"User: {content}\n"
        elif role == "assistant":
            conversation += f"TamBOT: {content}\n"

    conversation += "\nTamBOT:"

    def stream():
        response = client.models.generate_content_stream(
            model="gemini-3.5-flash-lite",
            contents=conversation
        )

        for chunk in response:
            if chunk.text:
                yield chunk.text

    return StreamingResponse(
        stream(),
        media_type="text/plain; charset=utf-8"
    )
