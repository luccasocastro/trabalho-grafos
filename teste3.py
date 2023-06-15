import matplotlib.pyplot as plt
import networkx as nx

def carregar_matrizes_adjacencia():
    matrizes = []
    with open('grafo.txt', 'r') as arquivo:
        matriz_atual = []
        for linha in arquivo:
            if linha.strip() == '':
                if matriz_atual:
                    matrizes.append(matriz_atual)
                    matriz_atual = []
            else:
                matriz_atual.append(list(map(int, linha.strip().split())))
        if matriz_atual:
            matrizes.append(matriz_atual)
    return matrizes

def plotar_grafo(matriz_adjacencia):
    G = nx.Graph()
    num_vertices = len(matriz_adjacencia)

    for i in range(num_vertices):
        G.add_node(i)

    for i in range(num_vertices):
        for j in range(num_vertices):
            if matriz_adjacencia[i][j] == 1:
                G.add_edge(i, j)

    nx.draw(G, with_labels=True, node_color='lightblue')
    plt.show()

def exibir_menu():
    print("Selecione uma opção:")
    print("1 - Verificar se o grafo é conexo")
    print("2 - Aplicar busca em largura")
    print("3 - Encontrar bipartição")
    print("0 - Sair")

def busca_largura(grafo, vertice_raiz):
    visitados = set()
    fila = [vertice_raiz]

    while fila:
        vertice = fila.pop(0)
        if vertice not in visitados:
            visitados.add(vertice)
            fila.extend(vizinho for vizinho, aresta in enumerate(grafo[vertice]) if aresta == 1 and vizinho not in visitados)

    return len(visitados) == len(grafo)


def encontrar_biparticao(grafo, vertice_raiz):
    visitados = set()
    fila = [(vertice_raiz, 0)]  # Tupla (vértice, cor)
    biparticao = {vertice_raiz: 0}  # Dicionário {vértice: cor}

    while fila:
        vertice, cor = fila.pop(0)
        if vertice not in visitados:
            visitados.add(vertice)
            for vizinho, aresta in enumerate(grafo[vertice]):
                if aresta == 1:
                    if vizinho not in biparticao:
                        biparticao[vizinho] = 1 - cor
                        fila.append((vizinho, 1 - cor))
                    elif biparticao[vizinho] == cor:
                        return None  # Grafo não é bipartido
    return biparticao


def encontrar_ciclo_impar(grafo, vertice_raiz):
    visitados = {}
    fila = [(vertice_raiz, 0)]
    ciclo_impar = []

    while fila:
        vertice, nivel = fila.pop(0)
        if vertice not in visitados:
            visitados[vertice] = nivel
            fila.extend((vizinho, nivel + 1) for vizinho, aresta in enumerate(grafo[vertice]) if aresta == 1 and vizinho not in visitados)
        elif visitados[vertice] % 2 != nivel % 2:
            ciclo_impar.extend([vertice, nivel])
            break

    return ciclo_impar

def main():
    matrizes = carregar_matrizes_adjacencia()
    num_matrizes = len(matrizes)
    print(f"Foram carregadas {num_matrizes} matrizes de adjacência.")

    indice_matriz = int(input(f"Digite o índice da matriz que você deseja manipular (0 a {num_matrizes - 1}): "))
    matriz_adjacencia = matrizes[indice_matriz]

    plotar_grafo(matriz_adjacencia)

    while True:
        exibir_menu()
        opcao = int(input("Digite o número da opção desejada: "))

        if opcao == 1:
            if busca_largura(matriz_adjacencia, 0):
                print("SIM, o grafo é conexo.")
            else:
                print("NÃO, o grafo é desconexo.")
            componentes_conexas = []
            vertices_visitados = set()
            for vertice in range(len(matriz_adjacencia)):
                if vertice not in vertices_visitados:
                    componente = set()
                    if busca_largura(matriz_adjacencia, vertice):
                        fila = [vertice]
                        while fila:
                            v = fila.pop(0)
                            if v not in componente:
                                componente.add(v)
                                fila.extend(vizinho for vizinho, aresta in enumerate(matriz_adjacencia[v]) if aresta == 1 and vizinho not in componente)
            componentes_conexas.append(componente)
            vertices_visitados.update(componente)
            print(f"Componentes Conexas:")
            for i, componente in enumerate(componentes_conexas):
                print(f"Componente Conexa {i+1}: {componente}")
        elif opcao == 2:
            vertice_raiz = int(input(f"Qual será o vértice raiz da busca? (0 a {len(matriz_adjacencia)-1}): "))
            componentes_conexas = busca_largura(matriz_adjacencia, vertice_raiz)
            plotar_grafo(matriz_adjacencia)
        elif opcao == 3:
            vertice_raiz = int(input("Qual será o vértice raiz da busca? "))
            biparticao = encontrar_biparticao(matriz_adjacencia, vertice_raiz)
            if biparticao is None:
                print("O grafo não é bipartido.")
                ciclo_impar = encontrar_ciclo_impar(matriz_adjacencia, vertice_raiz)
                print("Ciclo Ímpar:")
                print(ciclo_impar)
            else:
                print("Bipartição do grafo:")
                for vertice, cor in biparticao.items():
                    print(f"Vértice {vertice}: Cor {cor}")
        elif opcao == 0:
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()