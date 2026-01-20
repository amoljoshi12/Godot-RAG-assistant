import json
import requests
import sys
from search_chunks import search, initialize

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"
TOP_K = 5


def build_prompt(question: str, docs: list[str]) -> str:
    context = "\n\n".join(docs)

    return f"""You are a Godot 4 expert.

Answer the question using ONLY the information below.
You are specialized in Godot game engine.
You are developed by Amol Joshi.
You are trained on a specific dataset made by godot documentation.
Do NOT mention documentation.
Do NOT repeat the question.
Do NOT quote headings.
Be concise and direct.

If the answer is not present, say:
"I don't know based on the documentation."

Information:
{context}

Answer:"""


def ask_ollama(prompt: str) -> str:
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "temperature": 0.2,
            "stream": False
        },
        timeout=120
    )
    resp.raise_for_status()
    return resp.json()["response"].strip()


def main():
    initialize()

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        print("Godot RAG assistant ready. Type 'exit' to quit.")
        while True:
            question = input("> ").strip()
            if question.lower() in {"exit", "quit"}:
                return
            if question:
                break

    results = search(question, top_k=TOP_K)

    docs = [r["text"] for r in results if "text" in r]

    if not docs:
        print("I don't know based on the documentation.")
        return

    prompt = build_prompt(question, docs)
    answer = ask_ollama(prompt)

    print("\n" + answer)


if __name__ == "__main__":
    main()
