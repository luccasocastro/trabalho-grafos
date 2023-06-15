import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import networkx as nx

# Função para ler a matriz de adjacência de um arquivo
def ler_matriz_adjacencia(arquivo):
    with open(arquivo, 'r') as file:
        matrizes = file.read().strip().split('\n\n')
    return [np.array([list(map(int, row.split())) for row in matriz.split('\n')]) for matriz in matrizes]

# Função para plotar o grafo utilizando NetworkX
def plotar_grafo(matriz_adjacencia, nome_arquivo):
    G = nx.from_numpy_array(matriz_adjacencia)
    nx.draw(G, with_labels=True)
    plt.savefig(nome_arquivo)
    plt.show()

# Função para verificar se o grafo é conexo
def verificar_conexo(matriz_adjacencia):
    n = len(matriz_adjacencia)
    visitado = [False] * n
    componentes_conexas = []

    def dfs(v):
        visitado[v] = True
        componente_atual.append(v)
        for u in range(n):
            if matriz_adjacencia[v][u] and not visitado[u]:
                dfs(u)

    for v in range(n):
        if not visitado[v]:
            componente_atual = []
            dfs(v)
            componentes_conexas.append(componente_atual)

    return componentes_conexas

# Função para realizar a busca em largura
def busca_em_largura(matriz_adjacencia, vertice_raiz):
    n = len(matriz_adjacencia)
    visitado = [False] * n
    nivel = [None] * n
    fila = deque()

    visitado[vertice_raiz] = True
    nivel[vertice_raiz] = 0
    fila.append(vertice_raiz)

    arvore_busca = np.zeros_like(matriz_adjacencia)

    while fila:
        v = fila.popleft()
        for u in range(n):
            if matriz_adjacencia[v][u] and not visitado[u]:
                visitado[u] = True
                nivel[u] = nivel[v] + 1
                fila.append(u)
                arvore_busca[v][u] = 1

    return arvore_busca, nivel

# Função para encontrar a bipartição do grafo
def encontrar_biparticao(matriz_adjacencia):
    n = len(matriz_adjacencia)
    cores = [None] * n
    bipartido = True
    ciclo_impar = []

    def dfs(v, cor):
        cores[v] = cor
        for u in range(n):
            if matriz_adjacencia[v][u]:
                if cores[u] is None:
                    dfs(u, not cor)
                elif cores[u] == cor:
                    nonlocal bipartido
                    bipartido = False
                    ciclo_impar.extend(encontrar_ciclo_impar(v, u))

    def encontrar_ciclo_impar(v, u):
        ciclo = []
        while v != u:
            ciclo.append(v)
            for w in range(n):
                if matriz_adjacencia[v][w] and cores[w] == cores[v]:
                    ciclo.append(w)
                    return ciclo
            v = ciclo[-1]
        ciclo.append(v)
        return ciclo

    for v in range(n):
        if cores[v] is None:
            dfs(v, True)

    if not bipartido:
        return None, ciclo_impar

    conjunto_a = [v for v, cor in enumerate(cores) if cor]
    conjunto_b = [v for v, cor in enumerate(cores) if not cor]
    return conjunto_a, conjunto_b


# Função principal
def main():
    matrizes_adjacencia = ler_matriz_adjacencia('grafo.txt')
    num_matrizes = len(matrizes_adjacencia)

    print(f"Foram carregadas {num_matrizes} matrizes de adjacência.")

    indice_matriz = int(input(f"Digite o índice da matriz que você deseja manipular (0 a {num_matrizes - 1}): "))
    matriz_adjacencia = matrizes_adjacencia[indice_matriz]

    plotar_grafo(matriz_adjacencia, "grafo.png")

    while True:
        print("Menu de seleção:")
        print("1 - Verificar se o grafo é conexo")
        print("2 - Aplicar busca em largura")
        print("3 - Encontrar bipartição")
        print("0 - Sair")

        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            componentes_conexas = verificar_conexo(matriz_adjacencia)
            if len(componentes_conexas) == 1:
                print("O grafo é conexo.")
            else:
                print("O grafo é desconexo.")
                for i, componente in enumerate(componentes_conexas):
                    print(f"Componente conexa {i+1}: {componente}")

        elif opcao == "2":
            vertice_raiz = int(input(f"Qual será o vértice raiz da busca? (0 a {len(matriz_adjacencia)-1}): "))
            arvore_busca, nivel = busca_em_largura(matriz_adjacencia, vertice_raiz)
            print("Árvore de Busca em Largura:")
            print(arvore_busca)

        elif opcao == "3":
            conjunto_a, conjunto_b = encontrar_biparticao(matriz_adjacencia)
            if conjunto_a is None:
                print("O grafo não é bipartido.")
                print(f"Ciclo ímpar: {conjunto_b}")
            else:
                print("O grafo é bipartido.")
                print(f"Conjunto A: {conjunto_a}")
                print(f"Conjunto B: {conjunto_b}")

        elif opcao == "0":
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
