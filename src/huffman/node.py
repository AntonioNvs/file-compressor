class Node:
    """
    Representa um nó na árvore de Huffman.
    """
    def __init__(self, char: str | None, freq: int, left: 'Node | None' = None, right: 'Node | None' = None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: 'Node') -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.freq < other.freq
