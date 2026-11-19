def registrar_salas(sala, mundo):
    """Recorre el árbol de salas y guarda en el diccionario sus visitas y objetos."""
    mundo[("visitas", sala["nombre"])] = 0
    if sala["objeto"] is not None:
        mundo[("objeto", sala["nombre"])] = sala["objeto"]
    for hijo in sala["hijos"]:
        registrar_salas(hijo, mundo)


def crear_mundo(raiz, bloqueos):
    """Crea el diccionario con el estado del mundo. Las claves son tuplas (tipo, nombre)."""
    mundo = {("puntos", "total"): 0}
    registrar_salas(raiz, mundo)
    for sala, motivo in bloqueos.items():
        mundo[("bloqueada", sala)] = motivo
    return mundo


def registrar_visita(mundo, sala):
    """Suma una visita a la sala (actualización con .get)."""
    mundo[("visitas", sala)] = mundo.get(("visitas", sala), 0) + 1


def objeto_en_sala(mundo, sala):
    """Devuelve el objeto que hay en la sala, o None si no hay (consulta con .get)."""
    return mundo.get(("objeto", sala))


def colocar_objeto(mundo, sala, objeto):
    """Inserta un objeto en la sala."""
    mundo[("objeto", sala)] = objeto


def quitar_objeto(mundo, sala):
    """Elimina y devuelve el objeto de la sala; None si no había."""
    return mundo.pop(("objeto", sala), None)


def motivo_bloqueo(mundo, sala):
    """Devuelve por qué está bloqueada la sala, o None si está libre."""
    return mundo.get(("bloqueada", sala))


def desbloquear(mundo, sala):
    """Elimina el bloqueo de una sala. Devuelve False si no estaba bloqueada."""
    if ("bloqueada", sala) in mundo:
        del mundo[("bloqueada", sala)]
        return True
    return False


def marcar_recogido(mundo, objeto):
    """Anota que el jugador ya recogió este objeto del mundo (progreso permanente)."""
    mundo[("recogido", objeto)] = True


def fue_recogido(mundo, objeto):
    """Dice si el jugador ya recogió ese objeto alguna vez."""
    return mundo.get(("recogido", objeto), False)

