import pytest
import tempfile
import os
from src.huffman.encoder import encode
from src.huffman.io import write_compressed, read_compressed, serialize_tree, deserialize_tree
from src.huffman.node import Node


@pytest.mark.unit
def test_write_read_roundtrip():
    """Comprime, escreve .huff v2, lê de volta e verifica integridade."""
    data = b"mississippi river flows slowly"
    bitstring, tree = encode(data)

    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name

    try:
        write_compressed(path, tree, bitstring, "test.txt")
        restored_tree, restored_bits, original_name = read_compressed(path)
        assert restored_bits == bitstring
        assert original_name == "test.txt"
    finally:
        os.unlink(path)


@pytest.mark.unit
def test_tree_serialization():
    """Serializa e desserializa uma árvore complexa, verificando estrutura."""
    left_left = Node(byte_val=ord('a'), freq=3)
    left_right = Node(byte_val=ord('b'), freq=5)
    left = Node(byte_val=None, freq=8, left=left_left, right=left_right)
    right = Node(byte_val=ord('c'), freq=10)
    root = Node(byte_val=None, freq=18, left=left, right=right)

    data = serialize_tree(root)
    restored = deserialize_tree(data)

    assert restored is not None
    assert restored.left is not None
    assert restored.right is not None
    assert restored.left.left.byte_val == ord('a')
    assert restored.left.right.byte_val == ord('b')
    assert restored.right.byte_val == ord('c')


@pytest.mark.unit
def test_empty_input_io():
    """Escrever/ler com dados vazios (edge case)."""
    data = b""
    bitstring, tree = encode(data)

    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name

    try:
        write_compressed(path, tree, bitstring, "empty.txt")
        restored_tree, restored_bits, original_name = read_compressed(path)
        assert restored_bits == ""
        assert restored_tree is None
        assert original_name == "empty.txt"
    finally:
        os.unlink(path)


@pytest.mark.unit
def test_large_input_roundtrip():
    """Roundtrip com 5000+ bytes — testa robustez do formato binário v2."""
    import random
    random.seed(42)
    data = bytes(random.randint(0, 255) for _ in range(5000))
    bitstring, tree = encode(data)

    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name

    try:
        write_compressed(path, tree, bitstring, "large_file.bin")
        restored_tree, restored_bits, original_name = read_compressed(path)
        assert restored_bits == bitstring
        assert original_name == "large_file.bin"
    finally:
        os.unlink(path)

@pytest.mark.unit
def test_read_non_existent_file():
    """Testa leitura de arquivo inexistente (caminho de erro)."""
    with pytest.raises(FileNotFoundError):
        read_compressed("non_existent_file_that_should_not_exist.huff")

@pytest.mark.unit
def test_serialize_single_node_tree():
    """Testa serialização com árvore de um único nó."""
    root = Node(byte_val=65, freq=1)  # 'A' = 65
    data = serialize_tree(root)
    restored = deserialize_tree(data)
    assert restored is not None
    assert restored.byte_val == 65
    assert restored.left is None
    assert restored.right is None

@pytest.mark.unit
def test_original_filename_preserved():
    """Verifica que o nome original do arquivo é preservado no roundtrip."""
    data = b"hello world"
    bitstring, tree = encode(data)
    
    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name
    
    try:
        write_compressed(path, tree, bitstring, "meu_documento.pdf")
        _, _, original_name = read_compressed(path)
        assert original_name == "meu_documento.pdf"
    finally:
        os.unlink(path)

