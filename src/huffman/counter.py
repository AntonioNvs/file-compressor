from collections import Counter

def count_frequencies(data: bytes) -> dict[int, int]:
    """
    Recebe bytes e retorna um dicionário com a frequência de cada byte (0–255).
    """
    return dict(Counter(data))
