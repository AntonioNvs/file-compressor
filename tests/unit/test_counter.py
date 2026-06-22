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
