from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_providers.ollama_client import get_ollama_model

def build_hello_chain():
    prompt = ChatPromptTemplate.from_template("Say hello to {name}")
    model = get_ollama_model()
    parser = StrOutputParser()
    return prompt | model | parser