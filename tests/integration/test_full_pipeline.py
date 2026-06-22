import os
import tempfile
import pytest
from src.huffman.encoder import encode
from src.huffman.decoder import decode
from src.huffman.io import write_compressed, read_compressed
from src.huffman.decompressor import decompress_file
from src.huffman.rle import rle_encode, rle_decode


@pytest.mark.integration
def test_full_compress_decompress_pipeline():
    """
    Pipeline completo sem interface web:
    bytes → RLE → Huffman → write → read → Huffman → RLE → bytes originais.
    """
    original_data = (
        "A compressão de Huffman é um algoritmo de compressão de dados sem perda. "
        "Ela usa uma árvore binária para atribuir códigos mais curtos aos símbolos "
        "mais frequentes e códigos mais longos aos menos frequentes."
    ).encode("utf-8")

    rle_data = rle_encode(original_data)
    bitstring, tree = encode(rle_data)

    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name

    try:
        write_compressed(path, tree, bitstring, "texto.txt")

        restored_tree, restored_bits, original_name = read_compressed(path)
        decoded_rle = decode(restored_bits, restored_tree)
        decoded_data = rle_decode(decoded_rle)

        assert decoded_data == original_data
        assert original_name == "texto.txt"
    finally:
        os.unlink(path)


@pytest.mark.integration
def test_pipeline_with_unicode_text():
    """Pipeline completo com texto Unicode (acentos, emojis) como bytes."""
    original_data = "Olá, mundo! Hoje o céu está nublado. ☁️🌧️".encode("utf-8")

    rle_data = rle_encode(original_data)
    bitstring, tree = encode(rle_data)

    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name

    try:
        write_compressed(path, tree, bitstring, "unicode.txt")
        restored_tree, restored_bits, _ = read_compressed(path)
        decoded_data = rle_decode(decode(restored_bits, restored_tree))
        assert decoded_data == original_data
    finally:
        os.unlink(path)


@pytest.mark.integration
def test_pipeline_compression_is_effective():
    """Verifica que a compressão realmente reduz o tamanho para texto natural."""
    import random

    random.seed(0)
    original_data = (("aaaa bbbb cccc " * 200) + "".join(
        random.choices("abcde ", k=500)
    )).encode("utf-8")

    rle_data = rle_encode(original_data)
    bitstring, tree = encode(rle_data)
    original_size = len(original_data)
    compressed_size = (len(bitstring) + 7) // 8

    assert compressed_size < original_size, (
        f"Compressão não foi efetiva: {compressed_size} >= {original_size}"
    )

@pytest.mark.integration
def test_large_file_pipeline():
    """Testa o pipeline completo com um arquivo grande (>= 100KB) e verifica taxa de compressão (> 40%)."""
    import random
    import string
    
    random.seed(42)
    words = ["huffman", "compressao", "dados", "arvore", "binaria", "eficiente", "texto", "algoritmo", "python"]
    original_text = " ".join(random.choices(words, k=15000)) + " " + "".join(random.choices(string.ascii_letters, k=5000))
    original_data = original_text.encode("utf-8")
    
    rle_data = rle_encode(original_data)
    bitstring, tree = encode(rle_data)
    
    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name
        
    try:
        write_compressed(path, tree, bitstring, "large_text.txt")
        
        restored_tree, restored_bits, _ = read_compressed(path)
        decoded_data = rle_decode(decode(restored_bits, restored_tree))
        
        assert decoded_data == original_data
        
        original_size = len(original_data)
        compressed_size = os.path.getsize(path)
        compression_ratio = (original_size - compressed_size) / original_size
        
        assert original_size >= 100000, f"Tamanho original é apenas {original_size} bytes"
        assert compression_ratio > 0.40, f"Taxa de compressão menor que 40%: {compression_ratio:.2%}"
        
    finally:
        os.unlink(path)


# --- Binary file pipelines (use decompress_file which has RLE built-in) ---

@pytest.mark.integration
def test_binary_file_pipeline():
    """Pipeline completo com dados binários puros (simulando imagem)."""
    import random
    random.seed(123)
    
    original_data = b"\x89PNG\r\n\x1a\n" + bytes(random.randint(0, 255) for _ in range(2000))
    
    with tempfile.TemporaryDirectory() as tmpdir:
        huff_path = os.path.join(tmpdir, "image.huff")
        
        rle_data = rle_encode(original_data)
        bitstring, tree = encode(rle_data)
        write_compressed(huff_path, tree, bitstring, "photo.png")
        
        restored_path, stats = decompress_file(huff_path, tmpdir)
        
        with open(restored_path, 'rb') as f:
            restored_data = f.read()
        
        assert restored_data == original_data
        assert os.path.basename(restored_path) == "photo.png"


@pytest.mark.integration
def test_pdf_pipeline():
    """Pipeline completo com dados simulando um PDF."""
    original_data = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\n" + b"\x00\xFF" * 500
    
    with tempfile.TemporaryDirectory() as tmpdir:
        huff_path = os.path.join(tmpdir, "doc.huff")
        
        rle_data = rle_encode(original_data)
        bitstring, tree = encode(rle_data)
        write_compressed(huff_path, tree, bitstring, "relatorio.pdf")
        
        restored_path, stats = decompress_file(huff_path, tmpdir)
        
        with open(restored_path, 'rb') as f:
            restored_data = f.read()
        
        assert restored_data == original_data
        assert stats["original_filename"] == "relatorio.pdf"


@pytest.mark.integration
def test_audio_pipeline():
    """Pipeline completo com dados simulando um arquivo WAV."""
    import struct
    wav_header = b"RIFF" + struct.pack('<I', 1000) + b"WAVEfmt " + struct.pack('<I', 16)
    original_data = wav_header + bytes(range(256)) * 4
    
    with tempfile.TemporaryDirectory() as tmpdir:
        huff_path = os.path.join(tmpdir, "audio.huff")
        
        rle_data = rle_encode(original_data)
        bitstring, tree = encode(rle_data)
        write_compressed(huff_path, tree, bitstring, "musica.wav")
        
        restored_path, stats = decompress_file(huff_path, tmpdir)
        
        with open(restored_path, 'rb') as f:
            restored_data = f.read()
        
        assert restored_data == original_data
        assert stats["original_filename"] == "musica.wav"


# --- RLE-specific integration tests ---

@pytest.mark.integration
def test_rle_improves_repetitive_data():
    """Dados com muitas repetições: RLE+Huffman deve comprimir melhor que Huffman sozinho."""
    original_data = b"\x00" * 1000 + b"\xFF" * 500 + b"\x42" * 300

    # Sem RLE
    bitstring_no_rle, _ = encode(original_data)
    size_no_rle = (len(bitstring_no_rle) + 7) // 8

    # Com RLE
    rle_data = rle_encode(original_data)
    bitstring_rle, _ = encode(rle_data)
    size_rle = (len(bitstring_rle) + 7) // 8

    assert size_rle < size_no_rle, (
        f"RLE+Huffman ({size_rle}) não melhorou sobre Huffman sozinho ({size_no_rle})"
    )


@pytest.mark.integration
def test_rle_roundtrip_with_bmp_like_data():
    """Dados tipo BMP (muitos zeros): RLE deve ajudar significativamente."""
    # Simula pixels BMP com muitas áreas sólidas
    original_data = (
        b"\x00\x00\x00" * 200 +  # 200 pixels pretos
        b"\xFF\xFF\xFF" * 100 +  # 100 pixels brancos
        b"\x00\x00\xFF" * 50     # 50 pixels azuis
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        huff_path = os.path.join(tmpdir, "image.huff")
        
        rle_data = rle_encode(original_data)
        bitstring, tree = encode(rle_data)
        write_compressed(huff_path, tree, bitstring, "image.bmp")
        
        restored_path, stats = decompress_file(huff_path, tmpdir)
        
        with open(restored_path, 'rb') as f:
            restored_data = f.read()
        
        assert restored_data == original_data
