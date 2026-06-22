import pytest
from src.huffman.counter import count_frequencies

@pytest.mark.unit
def test_empty_bytes():
    assert count_frequencies(b"") == {}

@pytest.mark.unit
def test_single_byte():
    assert count_frequencies(b"a") == {ord('a'): 1}

@pytest.mark.unit
def test_repeated_bytes():
    result = count_frequencies(b"aaabb")
    assert result[ord('a')] == 3
    assert result[ord('b')] == 2

@pytest.mark.unit
def test_mixed_bytes():
    data = b"a b 123 !a"
    freqs = count_frequencies(data)
    assert freqs[ord('a')] == 2
    assert freqs[ord(' ')] == 3
    assert freqs[ord('b')] == 1
    assert freqs[ord('1')] == 1
    assert freqs[ord('2')] == 1
    assert freqs[ord('3')] == 1
    assert freqs[ord('!')] == 1

@pytest.mark.unit
def test_binary_bytes():
    """Testa contagem com bytes binários completos (0x00–0xFF)."""
    data = bytes(range(256))
    freqs = count_frequencies(data)
    assert len(freqs) == 256
    for b in range(256):
        assert freqs[b] == 1

@pytest.mark.unit
def test_high_frequency_binary():
    """Testa contagem com bytes binários repetidos."""
    data = bytes([0x00] * 100 + [0xFF] * 50 + [0x42] * 25)
    freqs = count_frequencies(data)
    assert freqs[0x00] == 100
    assert freqs[0xFF] == 50
    assert freqs[0x42] == 25
