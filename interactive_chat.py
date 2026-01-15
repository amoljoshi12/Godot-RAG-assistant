import requests
from search_chunks import search, initialize

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"
TOP_K = 5


def ask_ollama(prompt: str) -> str:
    res = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.2
        },
        timeout=120
    )
    res.raise_for_status()
    return res.json()["response"].strip()


def build_prompt(question: str, docs: list[str]) -> str:
    context = "\n\n".join(docs)

    return (
        "You are a Godot 4 expert assistant.\n"
        "You were developed by Amol Joshi as a personal on-device AI assistant.\n\n"
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


def main():
    initialize()

    print("Godot RAG Assistant (Interactive)")
    print("Type your question. Type 'exit' to quit.\n")

    while True:
        try:
            question = input("> ").strip()

            if not question:
                continue
            if question.lower() in ("exit", "quit"):
                print("Chat closed")
                break

            results = search(question, top_k=TOP_K)
            docs = [r["text"] for r in results]

            if not docs:
                print("\nI don't know based on the documentation.\n")
                continue

            prompt = build_prompt(question, docs)
            answer = ask_ollama(prompt)

            print("\n" + answer + "\n")

        except KeyboardInterrupt:
            print("\nBye.")
            break
        except Exception as e:
            print(f"\nERROR: {e}\n")


if __name__ == "__main__":
    main()
