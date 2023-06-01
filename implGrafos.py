from queue import Queue


def read_graph(filename):
    graphs = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        current_graph = []
        for line in lines:
            if line.strip() == "":
                if current_graph:
                    graphs.append(current_graph)
                    current_graph = []
            else:
                row = [int(x) for x in line.split()]
                current_graph.append(row)
        if current_graph:
            graphs.append(current_graph)
    return graphs


def print_graph(graph):
    for row in graph:
        print(" ".join(str(x) for x in row))


def bfs(graph, start):
    n = len(graph)
    visited = [False] * n
    queue = Queue()
    queue.put(start)
    visited[start] = True

    while not queue.empty():
        vertex = queue.get()
        print(vertex, end=" ")
        for v in range(n):
            if graph[vertex][v] == 1 and not visited[v]:
                queue.put(v)
                visited[v] = True


def is_bipartite(graph):
    n = len(graph)
    colors = [0] * n

    def is_bipartite_util(vertex):
        colors[vertex] = 1
        queue = Queue()
        queue.put(vertex)

        while not queue.empty():
            u = queue.get()
            if graph[u][u] == 1:  # Check if self-loop exists
                return False

            for v in range(n):
                if graph[u][v] == 1 and colors[v] == colors[u]:
                    return False
                if graph[u][v] == 1 and colors[v] == 0:
                    colors[v] = -colors[u]
                    queue.put(v)

        return True

    for i in range(n):
        if colors[i] == 0:
            if not is_bipartite_util(i):
                return False

    return True


def find_odd_cycle(graph):
    n = len(graph)
    colors = [-1] * n
    parents = [-1] * n

    def bfs_cycle(start):
        queue = Queue()
        queue.put(start)
        colors[start] = 0

        while not queue.empty():
            vertex = queue.get()

            for v in range(n):
                if graph[vertex][v] == 1:
                    if colors[v] == -1:
                        colors[v] = 1 - colors[vertex]
                        parents[v] = vertex
                        queue.put(v)
                    elif colors[v] == colors[vertex]:
                        return v

        return -1

    for i in range(n):
        if colors[i] == -1:
            result = bfs_cycle(i)
            if result != -1:
                cycle = [result]
                parent = parents[result]
                while parent != result:
                    cycle.append(parent)
                    parent = parents[parent]
                cycle.append(result)
                return cycle

    return None


def main():
    filename = "grafo.txt"
    graphs = read_graph(filename)
    num_graphs = len(graphs)

    print(f"Foram carregadas {num_graphs} matrizes de adjacência.")

    graph_idx = int(input("Qual grafo você deseja manipular? (Digite o índice correspondente): "))
    graph = graphs[graph_idx]
    print("Matriz de adjacência:")
    print_graph(graph)

    while True:
        print("\nMenu de seleção:")
        print("1 - Verificar se o grafo é conexo")
        print("2 - Aplicar busca em largura")
        print("3 - Encontrar bipartição")
        print("0 - Sair")

        option = int(input("Escolha uma opção: "))

        if option == 0:
            break
        elif option == 1:
            visited = [False] * len(graph)
            components = []

            def dfs(v, component):
                visited[v] = True
                component.append(v)

                for u in range(len(graph)):
                    if graph[v][u] == 1 and not visited[u]:
                        dfs(u, component)

            for i in range(len(graph)):
                if not visited[i]:
                    component = []
                    dfs(i, component)
                    components.append(component)

            if len(components) == 1:
                print("O grafo é conexo.")
            else:
                print("O grafo é desconexo.")
                for i, component in enumerate(components):
                    print(f"Componente {i + 1}: {component}")
        elif option == 2:
            start_vertex = int(input("Qual será o vértice raiz da busca? (Digite o número correspondente): "))
            print("Vértices candidatos:")
            for i in range(len(graph)):
                print(i, end=" ")
            print("\nÁrvore de busca em largura:")
            bfs(graph, start_vertex)
        elif option == 3:
            if is_bipartite(graph):
                print("O grafo é bipartido.")
            else:
                print("O grafo não é bipartido.")
                odd_cycle = find_odd_cycle(graph)
                if odd_cycle:
                    print("Ciclo ímpar encontrado:", odd_cycle)
                else:
                    print("Não foi possível encontrar um ciclo ímpar no grafo.")

        print("\n")

if __name__ == '__main__':
    main()
