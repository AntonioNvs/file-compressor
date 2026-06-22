"""
Run-Length Encoding (RLE) pré-processamento para melhorar a compressão Huffman.

Formato: quando 4+ bytes consecutivos idênticos são encontrados,
emite os 4 bytes seguidos de 1 byte de contagem (0–255) indicando
quantas cópias adicionais existem além das 4 iniciais.
Runs maiores que 259 (4+255) são divididos em múltiplos chunks.

Bytes sem repetição passam literalmente, sem overhead.
"""


def rle_encode(data: bytes) -> bytes:
    """
    Codifica dados usando Run-Length Encoding.
    Sequências de 4+ bytes idênticos → 4 bytes + count byte.
    """
    if not data:
        return b""

    result = bytearray()
    i = 0
    n = len(data)

    while i < n:
        byte = data[i]

        # Conta bytes consecutivos idênticos
        run_len = 1
        while i + run_len < n and data[i + run_len] == byte:
            run_len += 1

        if run_len >= 4:
            remaining = run_len
            while remaining >= 4:
                chunk = min(remaining, 259)  # 4 + max 255
                result.extend([byte] * 4)
                result.append(chunk - 4)
                remaining -= chunk
            # Sobra de 0–3 bytes emitida literalmente
            for _ in range(remaining):
                result.append(byte)
            i += run_len
        else:
            result.append(byte)
            i += 1

    return bytes(result)


def rle_decode(data: bytes) -> bytes:
    """
    Decodifica dados codificados com Run-Length Encoding.
    Detecta 4 bytes idênticos consecutivos e lê o byte seguinte como contagem.
    """
    if not data:
        return b""

    result = bytearray()
    i = 0
    n = len(data)
    run_count = 0
    last_byte = -1

    while i < n:
        byte = data[i]
        i += 1

        if byte == last_byte:
            run_count += 1
        else:
            run_count = 1
            last_byte = byte

        result.append(byte)

        if run_count == 4:
            # Próximo byte é a contagem de cópias adicionais
            if i < n:
                count = data[i]
                i += 1
                result.extend([byte] * count)
            # Reset para o próximo possível run
            run_count = 0
            last_byte = -1

    return bytes(result)
