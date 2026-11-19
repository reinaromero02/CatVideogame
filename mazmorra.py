from grafo import Grafo


NOMBRES_SALAS = [
    "Claro Encantado",
    "Sendero de Hongos",
    "Arroyo de Luciernagas",
    "Cueva del Murcielago",
    "Arbol Hueco",
    "Colina de la Luna",
    "Guarida del Fantasma",
]

def generar_mazmorra(nombres, profundidad_actual=0, profundidad_maxima=2, ramas=2):
    """Genera recursivamente el bosque como un árbol de salas."""
    sala = {
        "nombre": nombres.pop(0),
        "profundidad": profundidad_actual,
        "hijos": [],
        "objeto": None,
    }

    if profundidad_actual == profundidad_maxima or not nombres:
        return sala

    for _ in range(ramas):
        if nombres:
            hijo = generar_mazmorra(nombres, profundidad_actual + 1, profundidad_maxima, ramas)
            sala["hijos"].append(hijo)
    return sala
def calcular_profundidad(sala):
    if not sala["hijos"]:
        return 0
    return 1 + max(calcular_profundidad(hijo) for hijo in sala["hijos"])
def contar_salas(sala):
    total = 1
    for hijo in sala["hijos"]:
        total += contar_salas(hijo)
    return total
def contar_salas_nivel(sala, resultado=None):
    if resultado is None:
        resultado = {}
    nivel = sala["profundidad"]
    resultado[nivel] = resultado.get(nivel, 0) + 1
    for hijo in sala["hijos"]:
        contar_salas_nivel(hijo, resultado)
    return resultado

def marcar_salas_profundas(sala, objetos, profundidad_objetivo):
    if sala["profundidad"] == profundidad_objetivo and objetos:
        sala["objeto"] = objetos.pop(0)
    for hijo in sala["hijos"]:
        marcar_salas_profundas(hijo, objetos, profundidad_objetivo)

def mostrar_arbol(sala, nivel=0):
    marca = f"  [{sala['objeto']}]" if sala["objeto"] else ""
    print("    " * nivel + "- " + sala["nombre"] + marca)
    for hijo in sala["hijos"]:
        mostrar_arbol(hijo, nivel + 1)

CLARO, SENDERO, ARROYO, CUEVA, ARBOL, COLINA, GUARIDA = NOMBRES_SALAS

ATAJOS = [(CUEVA, COLINA), (ARROYO, GUARIDA)]


def indexar_salas(sala, indice=None):
    """Crea un diccionario {nombre: sala} recorriendo el árbol de forma recursiva."""
    if indice is None:
        indice = {}
    indice[sala["nombre"]] = sala
    for hijo in sala["hijos"]:
        indexar_salas(hijo, indice)
    return indice


def construir_grafo(raiz, grafo=None):
    """Convierte el árbol de salas en un Grafo (cada sala conectada con sus hijos)."""
    if grafo is None:
        grafo = Grafo()
    grafo.agregar_nodo(raiz["nombre"])
    for hijo in raiz["hijos"]:
        grafo.agregar_arista(raiz["nombre"], hijo["nombre"])
        construir_grafo(hijo, grafo)
    return grafo


def agregar_atajos(grafo, atajos):
    """Agrega aristas extra al grafo: así el mapa tiene caminos alternativos (ciclos)."""
    for a, b in atajos:
        grafo.agregar_arista(a, b)