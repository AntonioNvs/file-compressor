import os
import tempfile
import pytest
from src.huffman.encoder import encode
from src.huffman.decoder import decode
from src.huffman.io import write_compressed, read_compressed


@pytest.mark.integration
def test_full_compress_decompress_pipeline():
    """
    Pipeline completo sem interface web:
    texto → encode → write_compressed → read_compressed → decode → texto original.
    """
    original_text = (
        "A compressão de Huffman é um algoritmo de compressão de dados sem perda. "
        "Ela usa uma árvore binária para atribuir códigos mais curtos aos símbolos "
        "mais frequentes e códigos mais longos aos menos frequentes."
    )

    bitstring, tree = encode(original_text)

    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name

    try:
        write_compressed(path, tree, bitstring)

        restored_tree, restored_bits = read_compressed(path)
        decoded_text = decode(restored_bits, restored_tree)

        assert decoded_text == original_text
    finally:
        os.unlink(path)


@pytest.mark.integration
def test_pipeline_with_unicode_text():
    """Pipeline completo com texto Unicode (acentos, emojis)."""
    original_text = "Olá, mundo! Hoje o céu está nublado. ☁️🌧️"

    bitstring, tree = encode(original_text)

    with tempfile.NamedTemporaryFile(suffix=".huff", delete=False) as tmp:
        path = tmp.name

    try:
        write_compressed(path, tree, bitstring)
        restored_tree, restored_bits = read_compressed(path)
        decoded_text = decode(restored_bits, restored_tree)
        assert decoded_text == original_text
    finally:
        os.unlink(path)


@pytest.mark.integration
def test_pipeline_compression_is_effective():
    """Verifica que a compressão realmente reduz o tamanho para texto natural."""
    import random
    import string

    random.seed(0)
    # Texto com distribuição não-uniforme (compressão deve ser efetiva)
    original_text = ("aaaa bbbb cccc " * 200) + "".join(
        random.choices("abcde ", k=500)
    )

    bitstring, tree = encode(original_text)
    original_size = len(original_text.encode("utf-8"))
    compressed_size = (len(bitstring) + 7) // 8

    assert compressed_size < original_size, (
        f"Compressão não foi efetiva: {compressed_size} >= {original_size}"
    )
