import struct
from src.huffman.node import Node

def serialize_tree(root: Node | None) -> bytes:
    """
    Serializa a árvore de Huffman usando percurso em pré-ordem.
    Folhas: bit 1 seguido dos bytes UTF-8 do caractere.
    Nós internos: bit 0.
    """
    if not root:
        return b""
        
    bits = []
    
    def dfs(node: Node):
        if node.left is None and node.right is None:
            bits.append('1')
            if node.char is not None:
                for b in node.char.encode('utf-8'):
                    bits.append(f"{b:08b}")
        else:
            bits.append('0')
            dfs(node.left)
            dfs(node.right)
            
    dfs(root)
    full_bits = "".join(bits)
    
    padding_length = (8 - (len(full_bits) % 8)) % 8
    full_bits += '0' * padding_length
    
    body_bytes = bytearray()
    for i in range(0, len(full_bits), 8):
        byte_str = full_bits[i:i+8]
        body_bytes.append(int(byte_str, 2))
        
    return bytes(body_bytes)

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

def deserialize_tree(data: bytes) -> Node | None:
    """
    Reconstrói a árvore a partir dos bytes serializados.
    Lida adequadamente com caracteres UTF-8 multi-byte.
    """
    if not data:
        return None
        
    full_bits = "".join(f"{b:08b}" for b in data)
    iterator = iter(full_bits)
    
    def parse_node():
        try:
            bit = next(iterator)
        except StopIteration:
            return None
            
        if bit == '1':
            first_byte_str = "".join(next(iterator) for _ in range(8))
            first_byte = int(first_byte_str, 2)
            char_bytes = bytearray([first_byte])
            
            if (first_byte >> 7) == 0:
                expected_bytes = 1
            elif (first_byte >> 5) == 0b110:
                expected_bytes = 2
            elif (first_byte >> 4) == 0b1110:
                expected_bytes = 3
            elif (first_byte >> 3) == 0b11110:
                expected_bytes = 4
            else:
                expected_bytes = 1
                
            for _ in range(expected_bytes - 1):
                next_byte_str = "".join(next(iterator) for _ in range(8))
                char_bytes.append(int(next_byte_str, 2))
                
            char = char_bytes.decode('utf-8')
            return Node(char=char, freq=0)
        else:
            left = parse_node()
            right = parse_node()
            return Node(char=None, freq=0, left=left, right=right)
            
    return parse_node()

def read_compressed(path: str) -> tuple[Node | None, str]:
    """
    Lê a árvore e a string de bits de um arquivo binário .huff.
    """
    with open(path, 'rb') as f:
        tree_len = struct.unpack('>I', f.read(4))[0]
        tree_bytes = f.read(tree_len)
        tree = deserialize_tree(tree_bytes)
        
        padding_length = struct.unpack('>B', f.read(1))[0]
        body_bytes = f.read()
        
    bitstring = "".join(f"{b:08b}" for b in body_bytes)
    if padding_length > 0:
        bitstring = bitstring[:-padding_length]
        
    return tree, bitstring
