"""
Testes suplementares para garantir cobertura de branches e casos não cobertos.
Varredura final para ultrapassar 30 testes unitários no total.
"""
import pytest
from src.huffman.node import Node
from src.huffman.tree import build_tree, generate_codes
from src.huffman.io import deserialize_tree, serialize_tree
from src.huffman.decoder import decode
from src.huffman.encoder import encode


# --- Node edge cases ---

@pytest.mark.unit
def test_node_lt_equal_frequencies():
    """__lt__ com frequências iguais retorna False (não menor que)."""
    a = Node(byte_val=ord('a'), freq=5)
    b = Node(byte_val=ord('b'), freq=5)
    assert not (a < b)
    assert not (b < a)


@pytest.mark.unit
def test_node_lt_with_non_node_returns_not_implemented():
    """__lt__ com objeto não-Node deve retornar NotImplemented."""
    node = Node(byte_val=ord('x'), freq=3)
    result = node.__lt__("not a node")
    assert result is NotImplemented


@pytest.mark.unit
def test_node_eq_with_non_node_returns_not_implemented():
    """__eq__ com objeto não-Node deve retornar NotImplemented."""
    node = Node(byte_val=ord('x'), freq=3)
    result = node.__eq__(42)
    assert result is NotImplemented


# --- Tree edge cases ---

@pytest.mark.unit
def test_build_tree_empty_dict():
    """build_tree com dicionário vazio retorna None."""
    result = build_tree({})
    assert result is None


@pytest.mark.unit
def test_generate_codes_single_node_tree():
    """generate_codes com árvore de nó único atribui código '0'."""
    root = Node(byte_val=ord('a'), freq=5)
    codes = generate_codes(root)
    assert codes == {ord('a'): "0"}


@pytest.mark.unit
def test_generate_codes_none_root():
    """generate_codes com root=None retorna dicionário vazio."""
    codes = generate_codes(None)
    assert codes == {}


# --- IO / Serialization edge cases ---

@pytest.mark.unit
def test_deserialize_tree_empty_bytes():
    """deserialize_tree com bytes vazios retorna None."""
    result = deserialize_tree(b"")
    assert result is None


@pytest.mark.unit
def test_serialize_none_tree():
    """serialize_tree com None retorna bytes vazios."""
    result = serialize_tree(None)
    assert result == b""


@pytest.mark.unit
def test_serialize_deserialize_single_leaf():
    """Árvore com único nó folha sobrevive ao ciclo serialize/deserialize."""
    root = Node(byte_val=ord('z'), freq=7)
    data = serialize_tree(root)
    restored = deserialize_tree(data)
    assert restored is not None
    assert restored.byte_val == ord('z')


# --- Decoder edge cases ---

@pytest.mark.unit
def test_decode_with_none_root():
    """decode com root=None e bitstring não-vazia retorna bytes vazios."""
    result = decode("010101", None)
    assert result == b""


@pytest.mark.unit
def test_decode_with_empty_bitstring_valid_tree():
    """decode com bitstring vazia mas árvore válida retorna bytes vazios."""
    node = Node(byte_val=ord('a'), freq=1)
    result = decode("", node)
    assert result == b""
