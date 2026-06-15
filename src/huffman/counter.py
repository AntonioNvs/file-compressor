from collections import Counter

def count_frequencies(text: str) -> dict[str, int]:
    """
    Recebe uma string e retorna um dicionário com a frequência de cada caractere.
    """
    return dict(Counter(text))
