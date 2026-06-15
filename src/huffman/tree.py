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

def generate_codes(root: Node | None) -> dict[str, str]:
    """
    Percorre a árvore de Huffman (DFS) gerando os códigos binários para cada caractere.
    """
    codes = {}
    
    def dfs(node: Node | None, current_code: str):
        if not node:
            return
        if node.char is not None:
            # Se for folha, salva o código
            # Se a string inteira tinha apenas um caractere distinto (current_code vazio)
            codes[node.char] = current_code if current_code else "0"
            return
            
        dfs(node.left, current_code + "0")
        dfs(node.right, current_code + "1")
        
    dfs(root, "")
    return codes
