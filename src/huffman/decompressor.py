import os
from src.huffman.decoder import decode
from src.huffman.io import read_compressed


def decompress_file(huff_path: str, output_dir: str) -> tuple[str, dict]:
    """
    Lê um arquivo .huff v2, decodifica e salva o arquivo original restaurado.
    
    Retorna:
        (caminho_do_arquivo_restaurado, estatísticas)
    """
    tree, bitstring, original_filename = read_compressed(huff_path)
    original_data = decode(bitstring, tree)
    
    output_path = os.path.join(output_dir, original_filename)
    with open(output_path, 'wb') as f:
        f.write(original_data)
    
    compressed_size = os.path.getsize(huff_path)
    restored_size = len(original_data)
    
    return output_path, {
        "compressed_size": compressed_size,
        "restored_size": restored_size,
        "original_filename": original_filename,
    }
