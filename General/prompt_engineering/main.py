from chains.LCEL_chain_lib import say_hello_chain, display_character_info_chain, sequential_composition_chain

def main():
    # call indivual chain
    chain = display_character_info_chain()
    response = chain.invoke({"name": "Aung"})
    print(response)

    # call sequential chain
    # sequential_chain = sequential_composition_chain()
    # sequential_response = sequential_chain.invoke({"name": "Julius"})
    # print(sequential_response)

if __name__ == "__main__":
    main()