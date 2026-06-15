import pytest
from src.huffman.encoder import encode

@pytest.mark.unit
def test_simple_phrase():
    bitstring, tree = encode("hello")
    assert bitstring != ""
    assert tree is not None
    assert tree.char is None

@pytest.mark.unit
def test_single_char():
    bitstring, tree = encode("aaaa")
    assert bitstring == "0000"
    assert tree is not None
    assert tree.char == "a"
    
@pytest.mark.unit
def test_unicode():
    bitstring, tree = encode("coração 🌟")
    assert bitstring != ""
    assert tree is not None
    
@pytest.mark.unit
def test_empty_string():
    bitstring, tree = encode("")
    assert bitstring == ""
    assert tree is None
