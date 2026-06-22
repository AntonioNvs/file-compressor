"""
Testes unitários para o módulo de Run-Length Encoding (rle.py).
"""
import pytest
from src.huffman.rle import rle_encode, rle_decode


# --- Roundtrip básico ---

@pytest.mark.unit
def test_empty_data():
    """Dados vazios retorna vazio."""
    assert rle_encode(b"") == b""
    assert rle_decode(b"") == b""

@pytest.mark.unit
def test_no_runs():
    """Dados sem repetições: saída idêntica à entrada."""
    data = b"abcdef"
    encoded = rle_encode(data)
    assert encoded == data  # Sem runs ≥ 4, nada muda
    assert rle_decode(encoded) == data

@pytest.mark.unit
def test_short_runs():
    """Runs de 1–3 bytes: sem codificação especial."""
    data = b"aabbc"
    encoded = rle_encode(data)
    assert encoded == data
    assert rle_decode(encoded) == data

@pytest.mark.unit
def test_triple_no_encode():
    """Exatamente 3 bytes iguais: não dispara RLE."""
    data = b"aaab"
    encoded = rle_encode(data)
    assert encoded == data
    assert rle_decode(encoded) == data

@pytest.mark.unit
def test_exactly_four():
    """Exatamente 4 bytes iguais: codificado como 4 bytes + count 0."""
    data = b"aaaa"
    encoded = rle_encode(data)
    assert encoded == b"aaaa\x00"
    assert rle_decode(encoded) == data

@pytest.mark.unit
def test_five_bytes():
    """5 bytes iguais: 4 + count 1."""
    data = b"aaaaa"
    encoded = rle_encode(data)
    assert encoded == b"aaaa\x01"
    assert rle_decode(encoded) == data

@pytest.mark.unit
def test_ten_bytes():
    """10 bytes iguais: 4 + count 6."""
    data = b"a" * 10
    encoded = rle_encode(data)
    assert encoded == b"aaaa\x06"
    assert rle_decode(encoded) == data

@pytest.mark.unit
def test_max_single_run():
    """259 bytes iguais (4 + 255): um único chunk."""
    data = b"\x42" * 259
    encoded = rle_encode(data)
    assert encoded == b"\x42" * 4 + b"\xff"
    assert rle_decode(encoded) == data

# --- End of tests ---
