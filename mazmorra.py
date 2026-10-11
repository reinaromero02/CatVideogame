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