from chains.hello_LCEL import build_hello_chain

def main():
    chain = build_hello_chain()
    response = chain.invoke({"name": "Aung"})
    print(response)

if __name__ == "__main__":
    main()