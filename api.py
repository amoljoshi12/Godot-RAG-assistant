from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

from search_chunks import search, initialize

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:latest"
TOP_K = 5

PREDEFINED_ANSWERS = {
    "who made you": "I was developed by Amol as a personal on-device AI assistant focused on Godot game development.",
    "who developed you": "I was developed by Amol as a personal on-device AI assistant focused on Godot game development. Though not fully responsive I can till help in ome queries",
    "what are you good at": "I am trained on a dataset made by godot documentation so i am focused on Godot game development.",
    "what are you": "I am a domain-specific AI assistant designed to help with Godot 4 game development using curated documentation.",
    "are you chatgpt": "No. I am a locally running, less powerful, domain-specific AI assistant developed by Amol."
}

app = FastAPI(title="Godot RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str


def build_prompt(question: str, docs: list[str]) -> str:
    context = "\n\n".join(docs)

    return (
        "You are a Godot 4 expert assistant.\n\n"
        "Rules:\n"
        "- Answer ONLY using the information below\n"
        "- Do NOT mention documentation\n"
        "- Do NOT repeat the question\n"
        "- Be concise\n"
        "- If the answer is missing, say:\n"
        "\"I don't know based on the documentation.\"\n\n"
        "Information:\n"
        f"{context}\n\n"
        "Answer:"
    )


def ask_ollama(prompt: str) -> str:
    res = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.2,
        },
        timeout=120,
    )
    res.raise_for_status()
    return res.json()["response"].strip()


@app.on_event("startup")
def startup():
    initialize()


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    question = req.message.strip()

    if not question:
        return {"answer": ""}

    q_lower = question.lower()

    for key, value in PREDEFINED_ANSWERS.items():
        if key in q_lower:
            return {"answer": value}

    results = search(question, top_k=TOP_K)
    docs = [r["text"] for r in results if "text" in r]

    if not docs:
        return {"answer": "I don't know based on the documentation."}

    prompt = build_prompt(question, docs)
    answer = ask_ollama(prompt)

    return {"answer": answer}
