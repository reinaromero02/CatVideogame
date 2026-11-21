#Cada misión se completa sola cuando se cumple su
#condición (consultando el diccionario del mundo) y su misión padre ya está
#completada. Completar una misión suma puntos y puede desbloquear una sala.


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
    """Recorrido en postorden: suma los puntos de una misión y de todas sus descendientes."""
    total = 0
    for hijo in nodo.hijos:
        total += puntos_de_rama(hijo)
    return total + RECOMPENSAS.get(nodo.nombre, 0)