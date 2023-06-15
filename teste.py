def is_bipartite(graph):
    """
    Verifica se um grafo é bipartido. Se o grafo não for bipartido, retorna o ciclo ímpar presente no grafo.
    
    Args:
        graph (dict): O grafo representado como um dicionário, onde as chaves são os vértices
                      e os valores são listas de vértices adjacentes.
                      
    Returns:
        bool | list: True se o grafo for bipartido, lista contendo o ciclo ímpar caso contrário.
    """
    def dfs(v, color):
        """
        Função auxiliar para percorrer o grafo usando busca em profundidade (DFS).
        
        Args:
            v (int): Vértice atual.
            color (list): Lista de cores para cada vértice.
            
        Returns:
            bool | list: True se o grafo for bipartido, lista contendo o ciclo ímpar caso contrário.
        """
        color[v] = 1  # Marca o vértice atual como visitado
        
        for neighbor in graph[v]:
            if color[neighbor] == 0:
                color[neighbor] = -color[v]  # Atribui uma cor oposta ao vizinho
                # Chama a DFS recursivamente para o vizinho não visitado
                result = dfs(neighbor, color)
                if isinstance(result, list):
                    if v in result:
                        return result[result.index(v):]  # Retorna o ciclo a partir do vértice atual
                    return [v] + result  # Concatena o vértice atual com o ciclo ímpar encontrado
            elif color[neighbor] == color[v]:
                # Encontrou um ciclo ímpar
                return [v, neighbor, v]
        
        color[v] = 2  # Marca o vértice atual como finalizado
        return True
    
    # Inicializa as cores dos vértices como 0 (não visitado)
    color = {v: 0 for v in graph}
    
    # Executa a DFS para cada vértice não visitado
    for v in graph:
        if color[v] == 0:
            result = dfs(v, color)
            if isinstance(result, list):
                return result[::-1]  # Inverte a ordem do ciclo ímpar encontrado
    
    return True


# Exemplo de uso
graph = {
    1: [3,4,8],
    2: [7],
    3: [1,4],
    4: [1,3,6],
    5: [6,7,9],
    6: [4,5],
    7: [2,5,8],
    8: [1,7,10],
    9: [5,10],
    10: [8,9]
}

graph1 = {
    1: [2, 3],
    2: [1, 4],
    3: [1, 4],
    4: [2, 3, 5],
    5: [4]
}

result = is_bipartite(graph1)
if isinstance(result, bool):
    print("O grafo é bipartido.")
else:
    print("O grafo não é bipartido. Ciclo ímpar encontrado:", result)
