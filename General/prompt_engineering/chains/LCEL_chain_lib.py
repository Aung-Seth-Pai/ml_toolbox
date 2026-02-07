from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from llm_providers.ollama_client import get_ollama_model
from llm_providers.groq_client import get_groq_model
from output_parsers.trim_think import TrimThinkOutputParser
from output_parsers.json_output import JsonOutputParser

def say_hello_chain():
    '''
        This function builds a simple chain that takes a name as input and returns a greeting message.    
    '''
     # define the prompt template
    prompt = ChatPromptTemplate.from_template(
        "Display a short greetings to Player ({name}) in World of Warcraft Elven style."
    )
    model = get_groq_model() # call llm client to get the model
    parser = TrimThinkOutputParser() 
    return prompt | model | parser

def display_character_info_chain():
    '''
        This function follows the greeting chain and continue conversation by displaying fictional character information.    
    '''
     # define the prompt template
    prompt = ChatPromptTemplate.from_template(
        "Based on the follwing greeting >>> {greeting_message}. " \
        "display a brief character information of the person we greeted." \
    )
    model = get_groq_model() # call llm client to get the model
    parser = TrimThinkOutputParser() 
    return prompt | model | parser

def sequential_composition_chain():
    '''
         Compose greeting >>> character info sequentially 
    '''
    hello_chain = say_hello_chain()
    info_chain = display_character_info_chain()
    chain = (
        {"greeting_message": hello_chain} 
        | info_chain
    )
    return chain


def combined_greeting_chain(model_provider="groq"):
    """
    Builds a single chain that:
    1. Greets the player in WoW Elf style
    2. Provides character info of the player
    Returns a single JSON string ONLY, with this structure:
        {"greeting": "<greeting_text>", "character_info": "<character_info_text>"}
    """
    prompt = ChatPromptTemplate.from_template(
        "You are a World of Warcraft Elf NPC.\n"
        "Task: Given the player's name `{name}`:\n"
        "1. Write a short greeting in Elf style.\n"
        "2. Continue the conversation by describing fictional character info "
        "of the player, in the same style.\n\n"
        "**Important:**\n"
        "- Output ONLY a valid JSON string.\n"
        "- The JSON must have exactly these keys: `greeting` and `character_info`.\n"
        "- Do NOT include any extra text, commentary, explanations, or <think> blocks.\n"
        "- Escape curly braces with double braces for template purposes: `{{` and `}}`.\n"
        "- Example format (do NOT copy content, only structure):\n"
        "`{{\"greeting\": \"<greeting text>\", \"character_info\": \"<character info text>\"}}`"
    )

    model = get_groq_model() if model_provider == "groq" else get_ollama_model()

    return prompt | model | TrimThinkOutputParser() | JsonOutputParser()