"""
Fixtures e dados de teste reutilizáveis para testes de grande porte e binários.
"""
import random


def generate_large_data(size: int = 10_000, seed: int = 99) -> bytes:
    """Gera dados binários aleatórios de `size` bytes com seed fixo."""
    random.seed(seed)
    return bytes(random.randint(0, 255) for _ in range(size))


def generate_large_text(size: int = 10_000, seed: int = 99) -> bytes:
    """Gera texto aleatório de `size` bytes com seed fixo (ASCII printable)."""
    import string
    random.seed(seed)
    return "".join(random.choices(string.printable, k=size)).encode("utf-8")


EMOJI_TEXT = "😀🎉👍🔥✨😎🙌💪🚀🌟".encode("utf-8")
MIXED_SCRIPTS_TEXT = "Hello Привет 你好 مرحبا".encode("utf-8")
