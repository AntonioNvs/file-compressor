import pytest
from src.huffman.encoder import encode
from src.huffman.decoder import decode

@pytest.mark.unit
def test_roundtrip_simple():
    original = "hello world"
    bitstring, tree = encode(original)
    decoded = decode(bitstring, tree)
    assert decoded == original

@pytest.mark.unit
def test_roundtrip_phrase():
    original = "This is a much longer phrase, with punctuation! And it has numbers like 1, 2, 3."
    bitstring, tree = encode(original)
    decoded = decode(bitstring, tree)
    assert decoded == original

@pytest.mark.unit
def test_roundtrip_unicode():
    original = "coração é vida! 🌟"
    bitstring, tree = encode(original)
    decoded = decode(bitstring, tree)
    assert decoded == original

@pytest.mark.unit
def test_empty_input():
    decoded = decode("", None)
    assert decoded == ""
