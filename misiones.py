#Cada misión se completa sola cuando se cumple su
#condición (consultando el diccionario del mundo) y su misión padre ya está
#completada. Completar una misión suma puntos y puede desbloquear una sala.

from collections import deque

from arboles import (preorden, misiones_disponibles, completar_mision,
                     construir_arbol_misiones)
from estado_mundo import desbloquear, fue_recogido, sumar_puntos
from mazmorra import SENDERO, CUEVA, ARBOL, GUARIDA

# Puntos que da cada misión al completarla (suman 135 en total).
RECOMPENSAS = {
    "Despertar en el Claro Encantado": 5,
    "Cruzar el Sendero de Hongos": 10,
    "Explorar el Árbol Hueco": 10,
    "Recoger la Bomba de Catnip": 15,
    "Derrotar al Murciélago Fantasma": 20,
    "Conseguir el Ovillo de Lana": 15,
    "Llegar a la Guarida del Fantasma": 15,
    "Derrotar a los 4 esbirros": 20,
    "Tomar la llave y escapar": 25,
}


def puntos_de_rama(nodo):
    #Recorrido en postorden: suma los puntos de una misión y de todas sus descendientes.
    total = 0
    for hijo in nodo.hijos:
        total += puntos_de_rama(hijo)
    return total + RECOMPENSAS.get(nodo.nombre, 0)



def _visitada(mundo, sala):
    #Dice si el jugador ya visitó la sala (consulta con .get en el diccionario del mundo).
    return mundo.get(("visitas", sala), 0) > 0


# Condición para completar cada misión: función que recibe el diccionario del mundo.
CONDICIONES = {
    "Despertar en el Claro Encantado": lambda mundo: True,
    "Cruzar el Sendero de Hongos": lambda mundo: _visitada(mundo, SENDERO),
    "Derrotar al Murciélago Fantasma": lambda mundo: _visitada(mundo, CUEVA),
    "Explorar el Árbol Hueco": lambda mundo: _visitada(mundo, ARBOL),
    "Llegar a la Guarida del Fantasma": lambda mundo: _visitada(mundo, GUARIDA),
    "Recoger la Bomba de Catnip": lambda mundo: fue_recogido(mundo, "Bomba de Catnip"),
    "Conseguir el Ovillo de Lana": lambda mundo: fue_recogido(mundo, "Ovillo de Lana"),
    "Derrotar a los 4 esbirros": lambda mundo: mundo.get(("esbirros", "derrotados"), 0) >= 4,
    "Tomar la llave y escapar": lambda mundo: mundo.get(("bosque", "escapaste"), False),
}


def misiones_por_nivel(raiz):
    #Recorrido por niveles (con una cola): devuelve {etapa: [nombres de misiones]}.
    etapas = {}
    cola = deque([(raiz, 0)])
    while len(cola) > 0:
        nodo, nivel = cola.popleft()
        etapas.setdefault(nivel, []).append(nodo.nombre)
        for hijo in nodo.hijos:
            cola.append((hijo, nivel + 1))
    return etapas



# Sala que se desbloquea en el mundo al completar una misión.
DESBLOQUEOS = {
    "Recoger la Bomba de Catnip": ARBOL,
}


def aplicar_efecto(estado, nombre):
    """Aplica el efecto de una misión completada: suma puntos y desbloquea salas."""
    mundo = estado["mundo"]
    sumar_puntos(mundo, RECOMPENSAS.get(nombre, 0))
    sala = DESBLOQUEOS.get(nombre)
    if sala is not None and desbloquear(mundo, sala):
        print(f"¡Se desbloquea: {sala}!")


def revisar_misiones(estado):
    """Completa todas las misiones disponibles cuya condición ya se cumple.

    Repite hasta que no cambie nada, porque completar una misión puede
    dejar disponible a sus hijas. Devuelve cuántas completó.
    """
    raiz = estado["misiones"]
    mundo = estado["mundo"]
    completadas = 0
    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for nombre in misiones_disponibles(raiz):
            condicion = CONDICIONES.get(nombre)
            if condicion is not None and condicion(mundo):
                if completar_mision(raiz, nombre):
                    aplicar_efecto(estado, nombre)
                    completadas += 1
                    hubo_cambio = True
    return completadas


def mostrar_misiones(estado):
    """Muestra el árbol (preorden), lo disponible por etapa y los puntos por rama."""
    raiz = estado["misiones"]
    print("\n=== ÁRBOL DE MISIONES ===")
    preorden(raiz)
    print("\nDisponibles por etapa:")
    disponibles = misiones_disponibles(raiz)
    hay_disponibles = False
    for nivel, nombres in misiones_por_nivel(raiz).items():
        libres = [n for n in nombres if n in disponibles]
        if libres:
            print(f"  Etapa {nivel}: " + ", ".join(libres))
            hay_disponibles = True
    if not hay_disponibles:
        print("  Ninguna: ya completaste todas las misiones.")
    print("\nPuntos por rama:")
    for hijo in raiz.hijos:
        print(f"  {hijo.nombre}: {puntos_de_rama(hijo)} pts")
    print(f"\nPuntos ganados: {estado['mundo'].get(('puntos', 'total'), 0)}")