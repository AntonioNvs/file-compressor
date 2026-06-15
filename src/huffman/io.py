import struct
from src.huffman.node import Node

def serialize_tree(root: Node | None) -> bytes:
    return b""

def write_compressed(path: str, tree: Node | None, bitstring: str):
    """
    Serializa a árvore e a string de bits em um arquivo binário .huff.
    Formato:
    - 4 bytes: Tamanho da árvore serializada (N)
    - N bytes: Árvore serializada (Header)
    - 1 byte: Número de bits de padding adicionados
    - M bytes: Corpo contendo a bitstring empacotada
    """
    tree_bytes = serialize_tree(tree)
    
    padding_length = (8 - (len(bitstring) % 8)) % 8
    padded_bitstring = bitstring + ('0' * padding_length)
    
    body_bytes = bytearray()
    for i in range(0, len(padded_bitstring), 8):
        byte_str = padded_bitstring[i:i+8]
        body_bytes.append(int(byte_str, 2))
        
    with open(path, 'wb') as f:
        f.write(struct.pack('>I', len(tree_bytes)))
        f.write(tree_bytes)
        f.write(struct.pack('>B', padding_length))
        f.write(body_bytes)
