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

@pytest.mark.unit
def test_degenerate_tree():
    root = Node(byte_val=None, freq=3, 
                left=Node(byte_val=None, freq=2, 
                          left=Node(byte_val=ord('A'), freq=1), 
                          right=Node(byte_val=ord('B'), freq=1)), 
                right=Node(byte_val=None, freq=0))
    assert decode("0001", root) == b"AB"

@pytest.mark.unit
def test_incomplete_bitstring():
    root = Node(byte_val=None, freq=2,
                left=Node(byte_val=None, freq=1, 
                          left=Node(byte_val=ord('A'), freq=1), 
                          right=Node(byte_val=ord('B'), freq=1)),
                right=Node(byte_val=ord('C'), freq=1))
    assert decode("0", root) == b""
    assert decode("10", root) == b"C"

# --- Binary roundtrip tests ---

@pytest.mark.unit
def test_roundtrip_binary_data():
    """Roundtrip com dados binários puros."""
    original = bytes(range(256))
    bitstring, tree = encode(original)
    decoded = decode(bitstring, tree)
    assert decoded == original

@pytest.mark.unit
def test_roundtrip_null_bytes():
    """Roundtrip com bytes nulos."""
    original = b"\x00\x00\x00\x01\x01\x02"
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
