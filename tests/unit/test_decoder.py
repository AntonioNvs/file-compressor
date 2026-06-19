import pytest
from src.huffman.encoder import encode
from src.huffman.decoder import decode
from src.huffman.node import Node

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

@pytest.mark.unit
def test_degenerate_tree():
    # Tree with only left children (e.g., frequencies: A=1, B=2)
    # A -> 00, B -> 01
    root = Node(char=None, freq=3, 
                left=Node(char=None, freq=2, 
                          left=Node(char='A', freq=1), 
                          right=Node(char='B', freq=1)), 
                right=Node(char=None, freq=0))
    # Test valid decode
    assert decode("0001", root) == "AB"

@pytest.mark.unit
def test_incomplete_bitstring():
    root = Node(char=None, freq=2,
                left=Node(char=None, freq=1, 
                          left=Node(char='A', freq=1), 
                          right=Node(char='B', freq=1)),
                right=Node(char='C', freq=1))
    # C=1, A=00, B=01
    # '0' goes to left child but doesn't reach a leaf. 
    # Decode ignores incomplete character.
    assert decode("0", root) == ""
    assert decode("10", root) == "C" # 1 decodes C, 0 is incomplete
