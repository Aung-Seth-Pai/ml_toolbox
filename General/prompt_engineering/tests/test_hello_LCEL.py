from chains.hello_LCEL import build_hello_chain

# this only tests that the chain runs and returns a string output
def test_hello_LCEL_chain():
    chain = build_hello_chain()
    out = chain.invoke({"name": "Test"})
    assert isinstance(out, str)
    assert len(out) > 0