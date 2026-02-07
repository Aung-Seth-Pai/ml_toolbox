import os

OLLAMA_MODEL = "deepseek-r1:1.5b"
OLLAMA_HOST = "http://localhost:11434"

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")