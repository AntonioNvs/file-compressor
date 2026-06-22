from src.huffman.node import Node

def decode(bitstring: str, root: Node | None) -> bytes:
    """
    Decodifica uma string de bits usando a árvore de Huffman fornecida.
    Retorna os bytes originais reconstruídos.
    """
    if not bitstring or not root:
        return b""
        
    # Caso especial: árvore com apenas um nó folha (apenas um byte distinto nos dados)
    if root.left is None and root.right is None:
        return bytes([root.byte_val] * len(bitstring))
        
    decoded = []
    current = root
    
    for bit in bitstring:
        if bit == '0':
            current = current.left
        else:
            current = current.right
            
        if current.byte_val is not None:
            decoded.append(current.byte_val)
            current = root
            
    return bytes(decoded)
