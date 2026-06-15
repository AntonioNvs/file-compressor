import pytest
import tempfile
import os
from src.huffman.encoder import encode
from src.huffman.io import write_compressed, read_compressed, serialize_tree, deserialize_tree
from src.huffman.node import Node


@pytest.mark.unit
def test_write_read_roundtrip():
    """Comprime, escreve .huff, lê de volta e verifica integridade."""
    text = "mississippi river flows slowly"
    bitstring, tree = encode(text)

    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name

    try:
        write_compressed(path, tree, bitstring)
        restored_tree, restored_bits = read_compressed(path)
        assert restored_bits == bitstring
    finally:
        os.unlink(path)


@pytest.mark.unit
def test_tree_serialization():
    """Serializa e desserializa uma árvore complexa, verificando estrutura."""
    left_left = Node(char="a", freq=3)
    left_right = Node(char="b", freq=5)
    left = Node(char=None, freq=8, left=left_left, right=left_right)
    right = Node(char="c", freq=10)
    root = Node(char=None, freq=18, left=left, right=right)

    data = serialize_tree(root)
    restored = deserialize_tree(data)

    assert restored is not None
    assert restored.left is not None
    assert restored.right is not None
    assert restored.left.left.char == "a"
    assert restored.left.right.char == "b"
    assert restored.right.char == "c"


@pytest.mark.unit
def test_empty_input_io():
    """Escrever/ler com texto vazio (edge case)."""
    text = ""
    bitstring, tree = encode(text)

    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name

    try:
        write_compressed(path, tree, bitstring)
        restored_tree, restored_bits = read_compressed(path)
        assert restored_bits == ""
        assert restored_tree is None
    finally:
        os.unlink(path)


@pytest.mark.unit
def test_large_input_roundtrip():
    """Roundtrip com 5000+ caracteres — testa robustez do formato binário."""
    import random
    import string
    random.seed(42)
    text = "".join(random.choices(string.ascii_letters + " \n", k=5000))
    bitstring, tree = encode(text)

    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name

    try:
        write_compressed(path, tree, bitstring)
        restored_tree, restored_bits = read_compressed(path)
        assert restored_bits == bitstring
    finally:
        os.unlink(path)
