import pytest
from src.huffman.encoder import encode
from src.huffman.decoder import decode

@pytest.mark.unit
def test_simple_phrase():
    bitstring, tree = encode(b"hello")
    assert bitstring != ""
    assert tree is not None
    assert tree.byte_val is None

@pytest.mark.unit
def test_single_byte():
    bitstring, tree = encode(b"aaaa")
    assert bitstring == "0000"
    assert tree is not None
    assert tree.byte_val == ord('a')

@pytest.mark.unit
def test_unicode_bytes():
    """Roundtrip com texto UTF-8 codificado como bytes."""
    text = "coração 🌟"
    data = text.encode("utf-8")
    bitstring, tree = encode(data)
    assert bitstring != ""
    assert tree is not None
    decoded = decode(bitstring, tree)
    assert decoded == data

@pytest.mark.unit
def test_empty_bytes():
    bitstring, tree = encode(b"")
    assert bitstring == ""
    assert tree is None

# --- Edge cases (task #31) ---

@pytest.mark.unit
def test_only_spaces():
    """Dados compostos apenas de espaços e whitespace."""
    data = b"     \t  \t   "
    bitstring, tree = encode(data)
    decoded = decode(bitstring, tree)
    assert decoded == data

@pytest.mark.unit
def test_only_newlines():
    """Dados com \\n e \\r\\n."""
    data = b"\n\n\r\n\n\r\n"
    bitstring, tree = encode(data)
    decoded = decode(bitstring, tree)
    assert decoded == data

@pytest.mark.unit
def test_binary_like_text():
    """Dados contendo caracteres '0' e '1' — não deve confundir com bitstring."""
    data = b"01010101 00110011 11001100"
    bitstring, tree = encode(data)
    decoded = decode(bitstring, tree)
    assert decoded == data

@pytest.mark.unit
def test_single_byte_repeated():
    """1000× o mesmo byte — decodificação deve ser exata."""
    data = b"z" * 1000
    bitstring, tree = encode(data)
    decoded = decode(bitstring, tree)
    assert decoded == data

# --- Large input and binary data (task #32) ---

@pytest.mark.unit
def test_large_data_10k():
    """Roundtrip com 10.000 bytes de dados variados."""
    import random
    random.seed(99)
    data = bytes(random.randint(0, 255) for _ in range(10_000))
    bitstring, tree = encode(data)
    decoded = decode(bitstring, tree)
    assert decoded == data

@pytest.mark.unit
def test_emoji_bytes():
    """Roundtrip com emojis — multi-byte UTF-8 preservado como bytes."""
    text = "😀🎉👍🔥✨😎🙌💪🚀🌟"
    data = text.encode("utf-8")
    bitstring, tree = encode(data)
    decoded = decode(bitstring, tree)
    assert decoded == data

@pytest.mark.unit
def test_mixed_scripts_bytes():
    """Texto com latim, cirílico, chinês e árabe como bytes."""
    text = "Hello Привет 你好 مرحبا"
    data = text.encode("utf-8")
    bitstring, tree = encode(data)
    decoded = decode(bitstring, tree)
    assert decoded == data

# --- Binary data specific tests ---

@pytest.mark.unit
def test_all_byte_values():
    """Roundtrip com todos os 256 valores de byte possíveis."""
    data = bytes(range(256))
    bitstring, tree = encode(data)
    decoded = decode(bitstring, tree)
    assert decoded == data

@pytest.mark.unit
def test_binary_pdf_header():
    """Roundtrip com bytes simulando um header de PDF."""
    data = b"%PDF-1.4\n" + bytes(range(256)) * 10
    bitstring, tree = encode(data)
    decoded = decode(bitstring, tree)
    assert decoded == data

@pytest.mark.unit
def test_binary_png_header():
    """Roundtrip com bytes simulando um header de PNG."""
    data = b"\x89PNG\r\n\x1a\n" + bytes([0x00, 0xFF] * 500)
    bitstring, tree = encode(data)
    decoded = decode(bitstring, tree)
    assert decoded == data

# --- Compression ratio stats (task #37) ---

@pytest.mark.unit
def test_stats_on_normal_text():
    """Texto típico: original_size > compressed_size e ratio > 0."""
    from src.huffman.encoder import get_stats
    stats = get_stats(b"the quick brown fox jumps over the lazy dog")
    assert stats["original_size"] > stats["compressed_size"]
    assert stats["ratio"] > 0

@pytest.mark.unit
def test_stats_on_single_byte():
    """100 bytes de um único byte: ratio ≈ 87%."""
    from src.huffman.encoder import get_stats
    stats = get_stats(b"a" * 100)
    assert stats["compressed_size"] == 13
    assert stats["original_size"] == 100
    assert stats["ratio"] > 80

@pytest.mark.unit
def test_stats_on_empty():
    """Dados vazios retorna original_size = 0 e não divide por zero."""
    from src.huffman.encoder import get_stats
    stats = get_stats(b"")
    assert stats["original_size"] == 0
    assert stats["compressed_size"] == 0
    assert stats["ratio"] == 0.0

@pytest.mark.unit
def test_stats_tree_size_positive():
    """get_stats retorna tree_size > 0 para dados com múltiplos bytes."""
    from src.huffman.encoder import get_stats
    stats = get_stats(b"abcdefghij")
    assert stats["tree_size"] > 0
