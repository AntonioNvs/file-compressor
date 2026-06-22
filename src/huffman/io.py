import struct
from src.huffman.node import Node

# Magic number para identificar arquivos .huff v2
MAGIC_NUMBER = b'\x48\x46'  # "HF"
FORMAT_VERSION = 2


def serialize_tree(root: Node | None) -> bytes:
    """
    Serializa a árvore de Huffman usando percurso em pré-ordem.
    Folhas: bit 1 seguido de 8 bits representando o byte_val (0–255).
    Nós internos: bit 0.
    """
    if not root:
        return b""
        
    bits = []
    
    def dfs(node: Node):
        if node.left is None and node.right is None:
            bits.append('1')
            if node.byte_val is not None:
                bits.append(f"{node.byte_val:08b}")
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


def write_compressed(path: str, tree: Node | None, bitstring: str, original_filename: str = "output.bin"):
    """
    Serializa a árvore e a string de bits em um arquivo binário .huff v2.
    Formato:
    - 2 bytes: Magic number (0x48 0x46 = "HF")
    - 1 byte:  Versão do formato (0x02)
    - 2 bytes: Tamanho do nome original (L)
    - L bytes: Nome original do arquivo (UTF-8)
    - 4 bytes: Tamanho da árvore serializada (N)
    - N bytes: Árvore serializada (Header)
    - 1 byte:  Número de bits de padding adicionados
    - M bytes: Corpo contendo a bitstring empacotada
    """
    tree_bytes = serialize_tree(tree)
    filename_bytes = original_filename.encode('utf-8')
    
    padding_length = (8 - (len(bitstring) % 8)) % 8
    padded_bitstring = bitstring + ('0' * padding_length)
    
    body_bytes = bytearray()
    for i in range(0, len(padded_bitstring), 8):
        byte_str = padded_bitstring[i:i+8]
        body_bytes.append(int(byte_str, 2))
        
    with open(path, 'wb') as f:
        # Header v2
        f.write(MAGIC_NUMBER)
        f.write(struct.pack('>B', FORMAT_VERSION))
        f.write(struct.pack('>H', len(filename_bytes)))
        f.write(filename_bytes)
        # Árvore
        f.write(struct.pack('>I', len(tree_bytes)))
        f.write(tree_bytes)
        # Corpo
        f.write(struct.pack('>B', padding_length))
        f.write(body_bytes)


def deserialize_tree(data: bytes) -> Node | None:
    """
    Reconstrói a árvore a partir dos bytes serializados.
    Cada folha contém 1 byte fixo (byte_val 0–255).
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
            # Folha: lê 8 bits = 1 byte
            byte_str = "".join(next(iterator) for _ in range(8))
            byte_val = int(byte_str, 2)
            return Node(byte_val=byte_val, freq=0)
        else:
            left = parse_node()
            right = parse_node()
            return Node(byte_val=None, freq=0, left=left, right=right)
            
    return parse_node()


def read_compressed(path: str) -> tuple[Node | None, str, str]:
    """
    Lê a árvore, a string de bits e o nome original de um arquivo binário .huff v2.
    Retorna (árvore, bitstring, nome_original).
    """
    with open(path, 'rb') as f:
        # Ler e validar magic number
        magic = f.read(2)
        if magic != MAGIC_NUMBER:
            raise ValueError(f"Formato de arquivo inválido: magic number esperado {MAGIC_NUMBER!r}, encontrado {magic!r}")
        
        # Ler versão
        version = struct.unpack('>B', f.read(1))[0]
        if version != FORMAT_VERSION:
            raise ValueError(f"Versão do formato não suportada: {version}")
        
        # Ler nome original
        filename_len = struct.unpack('>H', f.read(2))[0]
        original_filename = f.read(filename_len).decode('utf-8')
        
        # Ler árvore
        tree_len = struct.unpack('>I', f.read(4))[0]
        tree_bytes = f.read(tree_len)
        tree = deserialize_tree(tree_bytes)
        
        # Ler corpo
        padding_length = struct.unpack('>B', f.read(1))[0]
        body_bytes = f.read()
        
    bitstring = "".join(f"{b:08b}" for b in body_bytes)
    if padding_length > 0:
        bitstring = bitstring[:-padding_length]
        
    return tree, bitstring, original_filename
