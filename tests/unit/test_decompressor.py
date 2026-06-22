"""
Testes unitários para o módulo de descompactação (decompressor.py).
Dados são comprimidos com RLE+Huffman para corresponder ao pipeline real.
"""
import os
import tempfile
import pytest
from src.huffman.encoder import encode
from src.huffman.io import write_compressed
from src.huffman.decompressor import decompress_file
from src.huffman.rle import rle_encode


@pytest.mark.unit
def test_decompress_text_file():
    """Descompacta um arquivo de texto e verifica conteúdo restaurado."""
    original_data = b"hello world, this is a test for decompression!"
    rle_data = rle_encode(original_data)
    bitstring, tree = encode(rle_data)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        huff_path = os.path.join(tmpdir, "test.huff")
        write_compressed(huff_path, tree, bitstring, "original.txt")
        
        restored_path, stats = decompress_file(huff_path, tmpdir)
        
        assert os.path.exists(restored_path)
        assert stats["original_filename"] == "original.txt"
        assert stats["restored_size"] == len(original_data)
        
        with open(restored_path, 'rb') as f:
            assert f.read() == original_data


@pytest.mark.unit
def test_decompress_binary_file():
    """Descompacta dados binários e verifica integridade."""
    original_data = bytes(range(256)) * 10
    rle_data = rle_encode(original_data)
    bitstring, tree = encode(rle_data)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        huff_path = os.path.join(tmpdir, "binary.huff")
        write_compressed(huff_path, tree, bitstring, "data.bin")
        
        restored_path, stats = decompress_file(huff_path, tmpdir)
        
        with open(restored_path, 'rb') as f:
            restored = f.read()
        assert restored == original_data
        assert stats["original_filename"] == "data.bin"


@pytest.mark.unit
def test_decompress_preserves_filename():
    """Verifica que o nome original é restaurado corretamente."""
    original_data = b"some pdf content"
    rle_data = rle_encode(original_data)
    bitstring, tree = encode(rle_data)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        huff_path = os.path.join(tmpdir, "compressed.huff")
        write_compressed(huff_path, tree, bitstring, "relatorio.pdf")
        
        restored_path, stats = decompress_file(huff_path, tmpdir)
        
        assert os.path.basename(restored_path) == "relatorio.pdf"
        assert stats["original_filename"] == "relatorio.pdf"


@pytest.mark.unit
def test_decompress_stats_correct():
    """Verifica que as estatísticas de descompactação são corretas."""
    original_data = b"aaaa bbbb cccc dddd" * 100
    rle_data = rle_encode(original_data)
    bitstring, tree = encode(rle_data)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        huff_path = os.path.join(tmpdir, "stats_test.huff")
        write_compressed(huff_path, tree, bitstring, "data.txt")
        
        _, stats = decompress_file(huff_path, tmpdir)
        
        assert stats["restored_size"] == len(original_data)
        assert stats["compressed_size"] == os.path.getsize(huff_path)
        assert stats["compressed_size"] < stats["restored_size"]
