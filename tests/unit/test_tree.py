import pytest
from src.huffman.tree import build_tree, generate_codes

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
    
    assert root.left is not None
    assert root.left.char == "a"
    assert root.left.freq == 1
    
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

@pytest.mark.unit
def test_codes_are_prefix_free():
    freqs = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
    root = build_tree(freqs)
    codes = generate_codes(root)
    
    for char1, code1 in codes.items():
        for char2, code2 in codes.items():
            if char1 != char2:
                assert not code1.startswith(code2)

@pytest.mark.unit
def test_codes_unique():
    freqs = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
    root = build_tree(freqs)
    codes = generate_codes(root)
    
    unique_codes = set(codes.values())
    assert len(unique_codes) == len(codes)

@pytest.mark.unit
def test_variable_length():
    freqs = {"a": 1, "b": 10, "c": 100, "d": 1000}
    root = build_tree(freqs)
    codes = generate_codes(root)
    
    # "d" tem maior frequência, deve ter o menor ou igual código em relação aos outros
    # E "a" deve ser maior ou igual a "d" (com certeza será maior num caso tão extremo)
    assert len(codes["d"]) < len(codes["a"])
