class Node:
    """
    Representa um nó na árvore de Huffman.
    byte_val armazena um inteiro 0–255 para folhas, None para nós internos.
    """
    def __init__(self, byte_val: int | None, freq: int, left: 'Node | None' = None, right: 'Node | None' = None):
        self.byte_val = byte_val
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: 'Node') -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.freq < other.freq

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return (self.byte_val == other.byte_val and 
                self.freq == other.freq and 
                self.left == other.left and 
                self.right == other.right)
