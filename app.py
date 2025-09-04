from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from chatbot import chatbot

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request Schema ---
class ChatRequest(BaseModel):
    session_id: str
    message: str

# --- Routes ---
@app.get("/")
async def dummy_route():
    responses = [
        "Hello!",
        "Welcome to the dummy route!",
        "FastAPI is fun!",
        "Random text here!"
    ]
    return random.choice(responses)

@app.get("/ping")
async def ping():
    return "pong"

@app.post("/chatbot")
async def chat(request: ChatRequest):
    try:
        response = chatbot(session_id=request.session_id, user_input=request.message, llm="Groq")
        return {"output": response}
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500

# Run with: uvicorn app:app --reload --port 3333
