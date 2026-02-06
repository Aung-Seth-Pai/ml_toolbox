from chains.LCEL_chain_lib import say_hello_chain, display_character_info_chain, sequential_composition_chain

# this only tests that the chain runs and returns a string output
def test_say_hello_chain():
    chain = say_hello_chain()
    out = chain.invoke({"name": "Test"})
    assert isinstance(out, str)
    assert len(out) > 0

def test_sequential_composition_chain():
    chain = sequential_composition_chain()
    out = chain.invoke({"name": "Test"})
    assert isinstance(out, str)
    assert len(out) > 0

def test_display_character_info_chain():
    chain = display_character_info_chain()
    out = chain.invoke({"greeting_message": "Hello Test!"})
    assert isinstance(out, str)
    assert len(out) > 0
