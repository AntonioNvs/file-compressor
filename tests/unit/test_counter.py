import pytest
from src.huffman.counter import count_frequencies

@pytest.mark.unit
def test_empty_string():
    assert count_frequencies("") == {}

@pytest.mark.unit
def test_single_char():
    assert count_frequencies("a") == {"a": 1}

@pytest.mark.unit
def test_repeated_chars():
    assert count_frequencies("aaabb") == {"a": 3, "b": 2}

@pytest.mark.unit
def test_mixed_chars():
    text = "a b 123 !a"
    freqs = count_frequencies(text)
    assert freqs["a"] == 2
    assert freqs[" "] == 3
    assert freqs["b"] == 1
    assert freqs["1"] == 1
    assert freqs["2"] == 1
    assert freqs["3"] == 1
    assert freqs["!"] == 1
