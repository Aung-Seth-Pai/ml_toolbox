from langchain_ollama import ChatOllama
from config.settings import OLLAMA_MODEL, OLLAMA_HOST

def get_ollama_model():
    return ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_HOST,
        temperature=0
    )