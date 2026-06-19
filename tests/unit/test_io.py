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

@pytest.mark.unit
def test_read_non_existent_file():
    """Testa leitura de arquivo inexistente (caminho de erro)."""
    with pytest.raises(FileNotFoundError):
        read_compressed("non_existent_file_that_should_not_exist.huff")

@pytest.mark.unit
def test_deserialize_truncated_data():
    """Testa desserialização com dados truncados."""
    # Um único byte 0x00 significa 8 bits '0'.
    # Isso exige que a árvore continue criando nós internos iterativamente, 
    # mas ficará sem bits no meio do processo e deve retornar None
    # para nós que não conseguiu ler, ou algo que não falhe com exceção não tratada.
    # O código atual retorna None ao encontrar StopIteration.
    restored = deserialize_tree(b'\x00')
    assert restored is not None
    assert restored.left is not None # Conseguiu ler alguns
    
@pytest.mark.unit
def test_deserialize_invalid_utf8():
    """Testa desserialização com primeiro byte de UTF-8 inválido."""
    # Para forçar cair no `else: expected_bytes = 1` da linha 95, 
    # o primeiro byte precisa ser inválido em UTF-8, ex: 10xxxxxx (0x80 a 0xBF).
    # '1' indica folha, seguido por 8 bits do caractere.
    # Vamos apenas testar a desserialização com b'\xC0\x00'
    with pytest.raises(UnicodeDecodeError):
        deserialize_tree(b'\xC0\x00')

@pytest.mark.unit
def test_serialize_single_node_tree():
    """Testa serialização com árvore de um único nó."""
    root = Node(char="A", freq=1)
    data = serialize_tree(root)
    # 1 byte para o caractere "A", mais um bit "1" indicando folha.
    # O serialize_tree gera os bytes adequados
    restored = deserialize_tree(data)
    assert restored is not None
    assert restored.char == "A"
    assert restored.left is None
    assert restored.right is None

@pytest.mark.unit
def test_read_empty_compressed_file():
    """Testa leitura com arquivo vazio."""
    import struct
    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name
        
    try:
        with pytest.raises(struct.error):
            read_compressed(path)
    finally:
        os.unlink(path)
