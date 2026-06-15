import pytest
from src.huffman.encoder import encode
from src.huffman.decoder import decode

@pytest.mark.unit
def test_simple_phrase():
    bitstring, tree = encode("hello")
    assert bitstring != ""
    assert tree is not None
    assert tree.char is None

@pytest.mark.unit
def test_single_char():
    bitstring, tree = encode("aaaa")
    assert bitstring == "0000"
    assert tree is not None
    assert tree.char == "a"

@pytest.mark.unit
def test_unicode():
    bitstring, tree = encode("coração 🌟")
    assert bitstring != ""
    assert tree is not None

@pytest.mark.unit
def test_empty_string():
    bitstring, tree = encode("")
    assert bitstring == ""
    assert tree is None

# --- Edge cases (task #31) ---

@pytest.mark.unit
def test_only_spaces():
    """Texto composto apenas de espaços e whitespace."""
    text = "     \t  \t   "
    bitstring, tree = encode(text)
    decoded = decode(bitstring, tree)
    assert decoded == text

@pytest.mark.unit
def test_only_newlines():
    """Texto com \\n e \\r\\n."""
    text = "\n\n\r\n\n\r\n"
    bitstring, tree = encode(text)
    decoded = decode(bitstring, tree)
    assert decoded == text

@pytest.mark.unit
def test_binary_like_text():
    """Texto contendo caracteres '0' e '1' — não deve confundir com bitstring."""
    text = "01010101 00110011 11001100"
    bitstring, tree = encode(text)
    decoded = decode(bitstring, tree)
    assert decoded == text

@pytest.mark.unit
def test_single_char_repeated():
    """1000× o mesmo caractere — decodificação deve ser exata."""
    text = "z" * 1000
    bitstring, tree = encode(text)
    decoded = decode(bitstring, tree)
    assert decoded == text

# --- Large input and unicode boundary (task #32) ---

@pytest.mark.unit
def test_large_text_10k():
    """Roundtrip com 10.000 caracteres de texto variado."""
    import random
    import string
    random.seed(99)
    text = "".join(random.choices(string.printable, k=10_000))
    bitstring, tree = encode(text)
    decoded = decode(bitstring, tree)
    assert decoded == text

@pytest.mark.unit
def test_emoji():
    """Roundtrip com emojis — multi-byte characters preservados."""
    text = "😀🎉👍🔥✨😎🙌💪🚀🌟"
    bitstring, tree = encode(text)
    decoded = decode(bitstring, tree)
    assert decoded == text

@pytest.mark.unit
def test_mixed_scripts():
    """Texto com latim, cirílico, chinês e árabe misturados."""
    text = "Hello Привет 你好 مرحبا"
    bitstring, tree = encode(text)
    decoded = decode(bitstring, tree)
    assert decoded == text

# --- Compression ratio stats (task #37) ---

@pytest.mark.unit
def test_stats_on_normal_text():
    """Texto típico: original_size > compressed_size e ratio > 0."""
    from src.huffman.encoder import get_stats
    stats = get_stats("the quick brown fox jumps over the lazy dog")
    assert stats["original_size"] > stats["compressed_size"]
    assert stats["ratio"] > 0

@pytest.mark.unit
def test_stats_on_single_char():
    """100 bytes de um único caractere: ratio ≈ 87%."""
    from src.huffman.encoder import get_stats
    stats = get_stats("a" * 100)
    # 100 bits -> ceil(100/8) = 13 bytes
    assert stats["compressed_size"] == 13
    assert stats["original_size"] == 100
    assert stats["ratio"] > 80

@pytest.mark.unit
def test_stats_on_empty():
    """Texto vazio retorna original_size = 0 e não divide por zero."""
    from src.huffman.encoder import get_stats
    stats = get_stats("")
    assert stats["original_size"] == 0
    assert stats["compressed_size"] == 0
    assert stats["ratio"] == 0.0

@pytest.mark.unit
def test_stats_tree_size_positive():
    """get_stats retorna tree_size > 0 para texto com múltiplos caracteres."""
    from src.huffman.encoder import get_stats
    stats = get_stats("abcdefghij")
    assert stats["tree_size"] > 0
