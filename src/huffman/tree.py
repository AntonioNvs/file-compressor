import heapq
from src.huffman.node import Node

def build_tree(freqs: dict[int, int]) -> Node | None:
    """
    Constrói a árvore de Huffman usando uma min-heap e retorna o nó raiz.
    Recebe frequências de bytes (int 0–255).
    Retorna None se o dicionário de frequências estiver vazio.
    """
    if not freqs:
        return None

    heap = [Node(byte_val=b, freq=f) for b, f in freqs.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = Node(byte_val=None, freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(root: Node | None) -> dict[int, str]:
    """
    Percorre a árvore de Huffman (DFS) gerando os códigos binários para cada byte.
    Retorna dict[int, str] mapeando byte_val → código binário.
    """
    codes = {}
    
    def dfs(node: Node | None, current_code: str):
        if not node:
            return
        if node.byte_val is not None:
            codes[node.byte_val] = current_code if current_code else "0"
            return
            
        dfs(node.left, current_code + "0")
        dfs(node.right, current_code + "1")
        
    dfs(root, "")
    return codes
