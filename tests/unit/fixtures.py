"""
Fixtures e dados de teste reutilizáveis para testes de grande porte e Unicode.
"""
import random
import string


def generate_large_text(size: int = 10_000, seed: int = 99) -> str:
    """Gera um texto aleatório de `size` caracteres com seed fixo."""
    random.seed(seed)
    return "".join(random.choices(string.printable, k=size))


EMOJI_TEXT = "😀🎉👍🔥✨😎🙌💪🚀🌟"
MIXED_SCRIPTS_TEXT = "Hello Привет 你好 مرحبا"
