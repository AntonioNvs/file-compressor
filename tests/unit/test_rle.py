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

@pytest.mark.unit
def test_run_split():
    """260 bytes: dividido em chunk de 259 + 1 literal."""
    data = b"\x00" * 260
    encoded = rle_encode(data)
    # Chunk 1: 4 zeros + count 255
    # Sobra: 1 zero literal
    assert encoded == b"\x00\x00\x00\x00\xff\x00"
    assert rle_decode(encoded) == data

@pytest.mark.unit
def test_large_run_split():
    """520 bytes: dividido em 2 chunks de 259 + 2 literais."""
    data = b"\xAA" * 520
    encoded = rle_encode(data)
    # Chunk 1: 4 + 255 = 259
    # Chunk 2: 4 + 255 = 259
    # Sobra: 520 - 518 = 2 literais
    expected = b"\xAA" * 4 + b"\xff" + b"\xAA" * 4 + b"\xff" + b"\xAA" * 2
    assert encoded == expected
    assert rle_decode(encoded) == data


# --- Dados mistos ---

@pytest.mark.unit
def test_mixed_runs_and_literals():
    """Mistura de runs e literais."""
    data = b"abc" + b"\x00" * 10 + b"xyz" + b"\xff" * 5
    decoded = rle_decode(rle_encode(data))
    assert decoded == data

@pytest.mark.unit
def test_consecutive_different_runs():
    """Dois runs consecutivos de bytes diferentes."""
    data = b"A" * 8 + b"B" * 6
    decoded = rle_decode(rle_encode(data))
    assert decoded == data

@pytest.mark.unit
def test_alternating_bytes():
    """Bytes alternados: sem runs, passagem literal."""
    data = bytes([0, 1] * 100)
    encoded = rle_encode(data)
    assert encoded == data  # Nenhum run ≥ 4
    assert rle_decode(encoded) == data


# --- Dados binários reais ---

@pytest.mark.unit
def test_all_byte_values():
    """Roundtrip com todos os 256 valores."""
    data = bytes(range(256))
    assert rle_decode(rle_encode(data)) == data

@pytest.mark.unit
def test_binary_with_runs():
    """Dados binários com runs naturais (simula BMP)."""
    data = b"\x00" * 100 + b"\xff" * 50 + bytes(range(256))
    assert rle_decode(rle_encode(data)) == data

@pytest.mark.unit
def test_random_binary_roundtrip():
    """Roundtrip com 10000 bytes aleatórios."""
    import random
    random.seed(42)
    data = bytes(random.randint(0, 255) for _ in range(10_000))
    assert rle_decode(rle_encode(data)) == data

@pytest.mark.unit
def test_null_bytes():
    """Roundtrip com sequência de bytes nulos."""
    data = b"\x00" * 500
    assert rle_decode(rle_encode(data)) == data

@pytest.mark.unit
def test_rle_reduces_size_for_repetitive_data():
    """RLE deve reduzir tamanho para dados com muitas repetições."""
    data = b"\x42" * 1000
    encoded = rle_encode(data)
    assert len(encoded) < len(data)
    assert rle_decode(encoded) == data

@pytest.mark.unit
def test_rle_no_overhead_for_random_data():
    """RLE não deve aumentar dados aleatórios sem runs ≥ 4."""
    # Dados sem nenhuma repetição de 4+
    data = bytes(range(256))  # Cada byte aparece exatamente 1 vez
    encoded = rle_encode(data)
    assert len(encoded) == len(data)
