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


def sumar_puntos(mundo, cantidad):
    """Suma puntos al marcador del mundo."""
    mundo[("puntos", "total")] = mundo.get(("puntos", "total"), 0) + cantidad


def salas_visitadas(mundo):
    """Filtra el diccionario: lista de salas que el jugador ya visitó."""
    return [clave[1] for clave, veces in mundo.items()
            if clave[0] == "visitas" and veces > 0]


def salas_bloqueadas(mundo):
    """Filtra el diccionario: conjunto de salas bloqueadas (se pasa a BFS y DFS)."""
    return {clave[1] for clave in mundo if clave[0] == "bloqueada"}


def objetos_pendientes(mundo):
    """Filtra el diccionario: {sala: objeto} de lo que aún no se ha recogido."""
    return {clave[1]: objeto for clave, objeto in mundo.items() if clave[0] == "objeto"}


def resumen_mundo(mundo):
    """Muestra un resumen del estado del mundo."""
    visitadas = salas_visitadas(mundo)
    bloqueadas = salas_bloqueadas(mundo)
    pendientes = objetos_pendientes(mundo)
    print(f"Salas visitadas ({len(visitadas)}): {', '.join(visitadas)}")
    if bloqueadas:
        detalle = ", ".join(f"{s} ({mundo[('bloqueada', s)]})" for s in bloqueadas)
        print(f"Salas bloqueadas: {detalle}")
    else:
        print("Salas bloqueadas: ninguna")
    if pendientes:
        detalle = ", ".join(f"{o} en {s}" for s, o in pendientes.items())
        print(f"Objetos por recoger: {detalle}")
    else:
        print("Objetos por recoger: ninguno")
    print(f"Puntos: {mundo.get(('puntos', 'total'), 0)}")

#def motivo_bloqueo: (no se si borrarlas o dejarlo así para despues.)

#def salas_bloqueadas: (lo mismo.)
     