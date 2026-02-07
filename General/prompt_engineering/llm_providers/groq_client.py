from langchain_groq import ChatGroq
from config.settings import GROQ_MODEL

def get_groq_model():
    return ChatGroq(
        model=GROQ_MODEL,
        temperature=0,
        # api_key is automatically read from GROQ_API_KEY env var
    )
