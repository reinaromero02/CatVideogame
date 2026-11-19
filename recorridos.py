from collections import deque


def bfs(grafo, inicio, bloqueados=()):
    """BFS con una fila: devuelve {nodo: padre} de todo lo alcanzable por la ruta con menos saltos."""
    if not grafo.existe(inicio) or inicio in bloqueados:
        return {}
    padres = {inicio: None}
    cola = deque([inicio])
    while len(cola) > 0:
        actual = cola.popleft()
        for vecino in grafo.vecinos(actual):
            if vecino not in padres and vecino not in bloqueados:
                padres[vecino] = actual
                cola.append(vecino)
    return padres


def ruta_mas_corta(grafo, inicio, destino, bloqueados=()):
    """Ruta con menos saltos entre dos nodos; None si no existe o no hay camino."""
    if not grafo.existe(destino) or destino in bloqueados:
        return None
    padres = bfs(grafo, inicio, bloqueados)
    if destino not in padres:
        return None
    ruta = []
    nodo = destino
    while nodo is not None:
        ruta.append(nodo)
        nodo = padres[nodo]
    ruta.reverse()
    return rutas

def dfs(grafo, inicio, bloqueados=(), visitados=None):
    """DFS recursivo: devuelve los nodos alcanzables desde 'inicio', en orden de visita."""
    if visitados is None:
        visitados = {}
    if not grafo.existe(inicio) or inicio in bloqueados:
        return list(visitados)
    visitados[inicio] = True
    for vecino in grafo.vecinos(inicio):
        if vecino not in visitados and vecino not in bloqueados:
            dfs(grafo, vecino, bloqueados, visitados)
    return list(visitados)


def zonas_aisladas(grafo, inicio, bloqueados=()):
    """Nodos a los que NO se puede llegar desde 'inicio' (usa DFS)."""
    alcanzables = dfs(grafo, inicio, bloqueados)
    return [nodo for nodo in grafo.adyacencia if nodo not in alcanzables]