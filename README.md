A fully offline, domain-specific AI assistant for Godot 4 game development, built using Retrieval-Augmented Generation (RAG).
The assistant answers questions only from curated documentation, preventing hallucinations and ensuring accurate technical support.

Features:

1- Runs completely on-device (no internet, no external APIs)
2- Uses Retrieval-Augmented Generation (RAG) for grounded answers
3- Local LLM inference using Phi-3 via Ollama
4- Fast semantic search with FAISS
5- Deterministic intent-override layer for identity and system questions
6- Clean FastAPI backend
7- Simple web-based chat UI
8- Safe fallback when information is not available

Limitations:

1- Knowledge limited to provided documentation
2- No internet access or live updates
3- No long-term conversation memory
4- Performance depends on local hardware
