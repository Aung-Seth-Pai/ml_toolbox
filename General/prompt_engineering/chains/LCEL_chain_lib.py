from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_providers.ollama_client import get_ollama_model

def say_hello_chain():
    '''
        This function builds a simple chain that takes a name as input and returns a greeting message.    
    '''
     # define the prompt template
    prompt = ChatPromptTemplate.from_template(
        "Say hello to {name}"
    )
    model = get_ollama_model() # call llm client to get the model
    parser = StrOutputParser() 
    return prompt | model | parser


def display_character_info_chain():
    '''
        This function follows the greeting chain and continue conversation by displaying fictional character information.    
    '''
     # define the prompt template
    prompt = ChatPromptTemplate.from_template(
        "Based on the follwing greeting >>> {greeting_message}. " \
        "display a brief character information of the person we greeted in a MMORPG style in a medieval fantasy world." \
    )
    model = get_ollama_model() # call llm client to get the model
    parser = StrOutputParser() 
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