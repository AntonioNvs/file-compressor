import pytest
from src.huffman.tree import build_tree

@pytest.mark.unit
def test_single_char():
    freqs = {"x": 5}
    root = build_tree(freqs)
    
    assert root is not None
    assert root.char == "x"
    assert root.freq == 5
    assert root.left is None
    assert root.right is None

@pytest.mark.unit
def test_two_chars():
    freqs = {"a": 1, "b": 2}
    root = build_tree(freqs)
    
    assert root is not None
    assert root.char is None
    assert root.freq == 3
    
    # Left should be the one with lowest freq ('a')
    assert root.left is not None
    assert root.left.char == "a"
    assert root.left.freq == 1
    
    # Right should be 'b'
    assert root.right is not None
    assert root.right.char == "b"
    assert root.right.freq == 2

@pytest.mark.unit
def test_multiple_chars():
    freqs = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
    root = build_tree(freqs)
    
    assert root is not None
    assert root.char is None
    assert root.freq == sum(freqs.values())
    assert root.freq == 100
    
    assert root.left is not None
    assert root.right is not None
