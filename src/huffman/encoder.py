from src.huffman.node import Node
from src.huffman.counter import count_frequencies
from src.huffman.tree import build_tree, generate_codes


def encode(text: str) -> tuple[str, Node | None]:
    """
    Codifica um texto usando o algoritmo de Huffman.
    Retorna a string de bits gerada e a raiz da árvore de Huffman.
    """
    if not text:
        return "", None

    freqs = count_frequencies(text)
    tree = build_tree(freqs)
    codes = generate_codes(tree)

    bitstring = "".join(codes[char] for char in text)

    return bitstring, tree


def get_stats(text: str) -> dict:
    """
    Calcula estatísticas de compressão para o texto fornecido.

    Retorna um dicionário com:
      - original_size: tamanho do texto original em bytes (UTF-8)
      - compressed_size: tamanho estimado da string de bits em bytes
      - ratio: percentual de redução de tamanho (0.0 se texto vazio)
      - tree_size: número de nós na árvore de Huffman
    """
    original_bytes = len(text.encode("utf-8"))

    if original_bytes == 0:
        return {
            "original_size": 0,
            "compressed_size": 0,
            "ratio": 0.0,
            "tree_size": 0,
        }

    bitstring, tree = encode(text)
    compressed_size = (len(bitstring) + 7) // 8  # ceil division

    def count_nodes(node: Node | None) -> int:
        if node is None:
            return 0
        return 1 + count_nodes(node.left) + count_nodes(node.right)

    tree_size = count_nodes(tree)
    ratio = (1 - compressed_size / original_bytes) * 100 if original_bytes > 0 else 0.0

    return {
        "original_size": original_bytes,
        "compressed_size": compressed_size,
        "ratio": ratio,
        "tree_size": tree_size,
    }
