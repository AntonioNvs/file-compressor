import pytest
from src.huffman.tree import build_tree, generate_codes

@pytest.mark.unit
def test_single_byte():
    freqs = {ord('x'): 5}
    root = build_tree(freqs)
    
    assert root is not None
    assert root.byte_val == ord('x')
    assert root.freq == 5
    assert root.left is None
    assert root.right is None

@pytest.mark.unit
def test_two_bytes():
    freqs = {ord('a'): 1, ord('b'): 2}
    root = build_tree(freqs)
    
    assert root is not None
    assert root.byte_val is None
    assert root.freq == 3
    
    assert root.left is not None
    assert root.left.byte_val == ord('a')
    assert root.left.freq == 1
    
    assert root.right is not None
    assert root.right.byte_val == ord('b')
    assert root.right.freq == 2

@pytest.mark.unit
def test_multiple_bytes():
    freqs = {ord('a'): 5, ord('b'): 9, ord('c'): 12, ord('d'): 13, ord('e'): 16, ord('f'): 45}
    root = build_tree(freqs)
    
    assert root is not None
    assert root.byte_val is None
    assert root.freq == sum(freqs.values())
    assert root.freq == 100
    
    assert root.left is not None
    assert root.right is not None

@pytest.mark.unit
def test_codes_are_prefix_free():
    freqs = {ord('a'): 5, ord('b'): 9, ord('c'): 12, ord('d'): 13, ord('e'): 16, ord('f'): 45}
    root = build_tree(freqs)
    codes = generate_codes(root)
    
    for byte1, code1 in codes.items():
        for byte2, code2 in codes.items():
            if byte1 != byte2:
                assert not code1.startswith(code2)

@pytest.mark.unit
def test_codes_unique():
    freqs = {ord('a'): 5, ord('b'): 9, ord('c'): 12, ord('d'): 13, ord('e'): 16, ord('f'): 45}
    root = build_tree(freqs)
    codes = generate_codes(root)
    
    unique_codes = set(codes.values())
    assert len(unique_codes) == len(codes)

@pytest.mark.unit
def test_variable_length():
    freqs = {ord('a'): 1, ord('b'): 10, ord('c'): 100, ord('d'): 1000}
    root = build_tree(freqs)
    codes = generate_codes(root)
    
    assert len(codes[ord('d')]) < len(codes[ord('a')])

@pytest.mark.unit
def test_build_tree_empty_freqs():
    root = build_tree({})
    assert root is None

@pytest.mark.unit
def test_generate_codes_none_root():
    codes = generate_codes(None)
    assert codes == {}
