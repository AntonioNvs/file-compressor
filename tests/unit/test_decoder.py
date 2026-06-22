import pytest
from src.huffman.encoder import encode
from src.huffman.decoder import decode
from src.huffman.node import Node

@pytest.mark.unit
def test_roundtrip_simple():
    original = b"hello world"
    bitstring, tree = encode(original)
    decoded = decode(bitstring, tree)
    assert decoded == original

@pytest.mark.unit
def test_roundtrip_phrase():
    original = b"This is a much longer phrase, with punctuation! And it has numbers like 1, 2, 3."
    bitstring, tree = encode(original)
    decoded = decode(bitstring, tree)
    assert decoded == original

@pytest.mark.unit
def test_roundtrip_unicode_bytes():
    original = "coração é vida! 🌟".encode("utf-8")
    bitstring, tree = encode(original)
    decoded = decode(bitstring, tree)
    assert decoded == original

@pytest.mark.unit
def test_empty_input():
    decoded = decode("", None)
    assert decoded == b""

# --- Binary roundtrip tests ---

@pytest.mark.unit
def test_roundtrip_binary_data():
    """Roundtrip com dados binários puros."""
    original = bytes(range(256))
    bitstring, tree = encode(original)
    decoded = decode(bitstring, tree)
    assert decoded == original

@pytest.mark.unit
def test_roundtrip_large_binary():
    """Roundtrip com 5000 bytes binários aleatórios."""
    import random
    random.seed(77)
    original = bytes(random.randint(0, 255) for _ in range(5000))
    bitstring, tree = encode(original)
    decoded = decode(bitstring, tree)
    assert decoded == original
