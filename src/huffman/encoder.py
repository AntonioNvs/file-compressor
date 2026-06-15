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
