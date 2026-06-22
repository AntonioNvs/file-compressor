from src.huffman.node import Node
from src.huffman.counter import count_frequencies
from src.huffman.tree import build_tree, generate_codes


def encode(data: bytes) -> tuple[str, Node | None]:
    """
    Codifica dados binários usando o algoritmo de Huffman.
    Recebe bytes brutos e retorna a string de bits gerada e a raiz da árvore.
    """
    if not data:
        return "", None

    freqs = count_frequencies(data)
    tree = build_tree(freqs)
    codes = generate_codes(tree)

    bitstring = "".join(codes[byte] for byte in data)

    return bitstring, tree


def get_stats(data: bytes) -> dict:
    """
    Calcula estatísticas de compressão para os dados fornecidos.

    Retorna um dicionário com:
      - original_size: tamanho dos dados originais em bytes
      - compressed_size: tamanho estimado da string de bits em bytes
      - ratio: percentual de redução de tamanho (0.0 se vazio)
      - tree_size: número de nós na árvore de Huffman
    """
    original_size = len(data)

    if original_size == 0:
        return {
            "original_size": 0,
            "compressed_size": 0,
            "ratio": 0.0,
            "tree_size": 0,
        }

    bitstring, tree = encode(data)
    compressed_size = (len(bitstring) + 7) // 8  # ceil division

    def count_nodes(node: Node | None) -> int:
        if node is None:
            return 0
        return 1 + count_nodes(node.left) + count_nodes(node.right)

    tree_size = count_nodes(tree)
    ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0.0

    return {
        "original_size": original_size,
        "compressed_size": compressed_size,
        "ratio": ratio,
        "tree_size": tree_size,
    }
