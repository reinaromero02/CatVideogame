class Grafo:
    """Grafo no dirigido y genérico, guardado como lista de adyacencia (diccionario)."""

    def __init__(self):
        self.adyacencia = {}

    def agregar_nodo(self, nodo):
        """Agrega un nodo si todavía no existe."""
        if nodo not in self.adyacencia:
            self.adyacencia[nodo] = []

    def agregar_arista(self, a, b):
        """Conecta dos nodos en ambos sentidos, sin repetir aristas."""
        self.agregar_nodo(a)
        self.agregar_nodo(b)
        if b not in self.adyacencia[a]:
            self.adyacencia[a].append(b)
        if a not in self.adyacencia[b]:
            self.adyacencia[b].append(a)

    def existe(self, nodo):
        """Dice si el nodo está en el grafo."""
        return nodo in self.adyacencia

    def vecinos(self, nodo):
        """Devuelve la lista de vecinos; lista vacía si el nodo no existe."""
        return self.adyacencia.get(nodo, [])