from src.huffman.node import Node

def decode(bitstring: str, root: Node | None) -> str:
    """
    Decodifica uma string de bits usando a árvore de Huffman fornecida.
    """
    if not bitstring or not root:
        return ""
        
    # Caso especial: árvore com apenas um nó folha (apenas um caractere distinto no texto)
    if root.left is None and root.right is None:
        return root.char * len(bitstring)
        
    decoded = []
    current = root
    
    for bit in bitstring:
        if bit == '0':
            current = current.left
        else:
            current = current.right
            
        if current.char is not None:
            decoded.append(current.char)
            current = root
            
    return "".join(decoded)
