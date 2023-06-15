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
    componentes_conexas = []

    while fila:
        vertice = fila.pop(0)
        if vertice not in visitados:
            visitados.add(vertice)
            componente_atual = set()
            componente_atual.add(vertice)
            fila.extend(vizinho for vizinho, aresta in enumerate(grafo[vertice]) if aresta == 1 and vizinho not in visitados)
            while fila:
                proximo_vertice = fila.pop(0)
                if proximo_vertice not in visitados:
                    visitados.add(proximo_vertice)
                    componente_atual.add(proximo_vertice)
                    fila.extend(vizinho for vizinho, aresta in enumerate(grafo[proximo_vertice]) if aresta == 1 and vizinho not in visitados)
            componentes_conexas.append(componente_atual)
    return componentes_conexas

def encontrar_biparticao(grafo, vertice_raiz):
    visitados = {}
    fila = [(vertice_raiz, 0)]
    biparticao = {}

    while fila:
        vertice, nivel = fila.pop(0)
        if vertice not in visitados:
            visitados[vertice] = nivel
            fila.extend((vizinho, nivel + 1) for vizinho, aresta in enumerate(grafo[vertice]) if aresta == 1 and vizinho not in visitados)
    
    for vertice in visitados:
        if visitados[vertice] % 2 == 0:
            biparticao[vertice] = "A"
        else:
            biparticao[vertice] = "B"
    
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
            componentes_conexas = busca_largura(matriz_adjacencia, 0)
            if len(componentes_conexas) == 1:
                print("SIM, o grafo é conexo.")
            else:
                print("NÃO, o grafo é desconexo.")
                for i, componente in enumerate(componentes_conexas):
                    print(f"Componente Conexa {i+1}: {componente}")
        elif opcao == 2:
            vertice_raiz = int(input(f"Qual será o vértice raiz da busca? (0 a {len(matriz_adjacencia)-1}): "))
            componentes_conexas = busca_largura(matriz_adjacencia, vertice_raiz)
            plotar_grafo(matriz_adjacencia)
        elif opcao == 3:
            vertice_raiz = int(input(f"Qual será o vértice raiz para encontrar a bipartição? (0 a {len(matriz_adjacencia)-1}): "))
            biparticao = encontrar_biparticao(matriz_adjacencia, vertice_raiz)
            if not biparticao:
                ciclo_impar = encontrar_ciclo_impar(matriz_adjacencia, vertice_raiz)
                print("O grafo não é bipartido, segue o ciclo ímpar:")
                print(ciclo_impar)
            else:
                print("O grafo é bipartido! Veja:")
                for vertice, grupo in biparticao.items():
                    print(f"Vértice {vertice}: Grupo {grupo}")
        elif opcao == 0:
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()