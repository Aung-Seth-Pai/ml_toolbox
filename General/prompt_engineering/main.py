from chains.LCEL_chain_lib import say_hello_chain, display_character_info_chain, sequential_composition_chain, combined_greeting_chain

from dotenv import load_dotenv
load_dotenv()

def main():
    # try:
    #     # call indivual chain
    #     chain = say_hello_chain()
    #     response = chain.invoke({"name": "Aung"})
    #     print(response)
    # except Exception as e:
    #     print(f"Error occurred: {e}")

    # this is for testing the sequential chain
    # try:
    #     # call sequential chain
    #     sequential_chain = sequential_composition_chain()
    #     sequential_response = sequential_chain.invoke({"name": "Zephyr"})
    #     print(sequential_response)
    # except Exception as e:
    #     print(f"Error occurred: {e}")

    try:
        # call combined chain
        combined_chain = combined_greeting_chain(model_provider="groq")
        combined_response = combined_chain.invoke({"name": "Zephyr"})
        # print(combined_response)
        print(combined_response["greeting"])
        print(combined_response["character_info"])
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
