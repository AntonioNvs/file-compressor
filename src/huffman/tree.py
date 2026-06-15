import heapq
from src.huffman.node import Node

def build_tree(freqs: dict[str, int]) -> Node | None:
    """
    Constrói a árvore de Huffman usando uma min-heap e retorna o nó raiz.
    Retorna None se o dicionário de frequências estiver vazio.
    """
    if not freqs:
        return None

    heap = [Node(char=c, freq=f) for c, f in freqs.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = Node(char=None, freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]
