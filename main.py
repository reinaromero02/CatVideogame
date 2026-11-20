from inventario import (
    agregar_objeto,
    soltar_objeto,
    usar_objeto,
    vaciar_inventario,
    objeto_mas_repetido,
    reemplazar_objeto,
    mostrar_inventario
)
from collections import deque
from historial import apilar_accion, deshacer_ultima_accion, mostrar_historial
from eventos import (
    cargar_eventos_iniciales,
    procesar_siguiente_evento,
    ver_siguiente_evento,
    simular_turnos,
)
from mazmorra import (
    NOMBRES_SALAS,
    ATAJOS,
    generar_mazmorra,
    contar_salas,
    calcular_profundidad,
    marcar_salas_profundas,
    indexar_salas,
    construir_grafo,
    agregar_atajos,
    ARBOL
)
from recorridos import ruta_mas_corta, dfs, zonas_aisladas

from estado_mundo import (
    crear_mundo,
    registrar_visita,
    objeto_en_sala,
    colocar_objeto,
    quitar_objeto,
    marcar_recogido,
)
def leer_opcion(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje).strip()
        try:
            numero = int(texto)     
        except ValueError:
            print(f"Opcion no valida. Elige un numero del {minimo} al {maximo}.")
            continue
        if numero < minimo or numero > maximo:
            print(f"Opcion no valida. Elige un numero del {minimo} al {maximo}.")
            continue
        return numero

def crear_estado(inventario_jugador):
    """Crea la mazmorra, el grafo del mapa, el diccionario del mundo, la cola de eventos y los turnos."""
    raiz = generar_mazmorra(list(NOMBRES_SALAS))
    marcar_salas_profundas(raiz, ["Bomba de Catnip", "Galleta de Atún", "Ovillo de Lana"], 2)
    grafo = construir_grafo(raiz)
    agregar_atajos(grafo, ATAJOS)
    mundo = crear_mundo(raiz, {ARBOL: "un árbol caído tapa el camino"})
    registrar_visita(mundo, raiz["nombre"])
    eventos = deque()
    cargar_eventos_iniciales(eventos)
    return {
        "raiz": raiz,
        "indice": indexar_salas(raiz),
        "grafo": grafo,
        "mundo": mundo,
        "sala": raiz,
        "historial": [],
        "eventos": eventos,
        "turnos": deque(["Gato", "Esbirro", "Fantasma"]),
        "inventario": inventario_jugador,
    }

def manejar_evento(estado, evento):
    """Aplica el efecto de un evento sobre el inventario y sobre el mundo."""
    if evento is None:
        return
    if evento["tipo"] == "enemigo":
        if "Bomba de Catnip" in estado["inventario"]:
            usar_objeto(estado["inventario"], "Bomba de Catnip")
        elif "Espada de Juguete" in estado["inventario"]:
            usar_objeto(estado["inventario"], "Espada de Juguete")
        else:
            print("No tienes juguetes: te defiendes con las garras.")
    elif evento["tipo"] == "cofre":
        sala = estado["sala"]["nombre"]
        if objeto_en_sala(estado["mundo"], sala) is None:
            colocar_objeto(estado["mundo"], sala, "Ratón de Juguete")
            print("Hay un 'Ratón de Juguete' en esta sala. ¡Puedes recogerlo!")

def mostrar_menu(estado):
    """Muestra la sala actual, el próximo evento y las opciones del menú."""
    print(f"\nEstás en: {estado['sala']['nombre']}")
    proximo = ver_siguiente_evento(estado["eventos"])
    if proximo:
        print(f"Próximo evento en la cola: {proximo['tipo']}")
    for numero, (texto, _) in enumerate(OPCIONES, start=1):
        print(f"{numero}. {texto}")
    print(f"{len(OPCIONES) + 1}. Salir")


def mover(estado):
    """Mueve al jugador por las conexiones del grafo, registra el movimiento y dispara el siguiente evento."""
    sala = estado["sala"]
    vecinos = estado["grafo"].vecinos(sala["nombre"])
    if len(vecinos) == 0:
        print("No hay salas conectadas desde aquí.")
        return
    textos = []
    for i, nombre in enumerate(vecinos, start=1):
        motivo = motivo_bloqueo(estado["mundo"], nombre)
        extra = f" [bloqueada: {motivo}]" if motivo else ""
        textos.append(f"{i}) {nombre}{extra}")
    print("Salas conectadas: " + "  ".join(textos))
    eleccion = leer_opcion("Elige una sala: ", 1, len(vecinos))
    nombre_destino = vecinos[eleccion - 1]
    motivo = motivo_bloqueo(estado["mundo"], nombre_destino)
    if motivo:
        print(f"No puedes pasar: {motivo}.")
        return
    destino = estado["indice"].get(nombre_destino)
    if destino is None:
        print("Esa sala no existe en el mapa.")
        return

    apilar_accion(estado["historial"], "mover", origen=sala, destino=destino)
    estado["sala"] = destino
    registrar_visita(estado["mundo"], nombre_destino)
    print(f"Te mueves a: {nombre_destino}")

    evento = procesar_siguiente_evento(estado["eventos"])
    manejar_evento(estado, evento)

def recoger(estado):
    """Recoge el objeto de la sala actual (lo lee del diccionario del mundo) y lo guarda en el inventario."""
    sala = estado["sala"]
    objeto = objeto_en_sala(estado["mundo"], sala["nombre"])
    if objeto is None:
        print("No hay nada que recoger aquí.")
        return
    agregar_objeto(estado["inventario"], objeto)
    quitar_objeto(estado["mundo"], sala["nombre"])
    marcar_recogido(estado["mundo"], objeto)
    apilar_accion(estado["historial"], "recoger", objeto=objeto, sala=sala)


def deshacer(estado):
    """Revierte la última acción. Si era un 'recoger', el objeto vuelve a la sala en el diccionario."""
    accion = deshacer_ultima_accion(estado["historial"])
    if accion is None:
        return
    if accion["tipo"] == "mover":
        estado["sala"] = accion["origen"]
        print(f"Vuelves a: {accion['origen']['nombre']}")
    elif accion["tipo"] == "recoger":
        soltar_objeto(estado["inventario"], accion["objeto"])
        colocar_objeto(estado["mundo"], accion["sala"]["nombre"], accion["objeto"])
def combate_final(inventario_jugador):
    """Combate del Checkpoint 1: derrotar a los 4 enemigos, tomar la llave y escapar."""
    print("\nINICIO DE COMBATE EN EL BOSQUE")
    enemigos_derrotados = 0
    
    # Aqui empezamos a atacar al enemigo con los jueguetes y derrotarlos
    while enemigos_derrotados < 4:
        enemigos_derrotados += 1
        print(f"\n¡Combate contra enemigo {enemigos_derrotados}!")
        
        if "Bomba de Catnip" in inventario_jugador:
            usar_objeto(inventario_jugador, "Bomba de Catnip")
        elif "Espada de Juguete" in inventario_jugador:
            usar_objeto(inventario_jugador, "Espada de Juguete")
        else:
            agregar_objeto(inventario_jugador, "Varita Mágica de Plumas")
            usar_objeto(inventario_jugador, "Varita Mágica de Plumas")
            
        print(f"Enemigo {enemigos_derrotados} derrotado. Total derrotados: {enemigos_derrotados}")

    # Si enemigos_derrotados == 4
    print("El enemigo 4 suelta la llave, ¡es tu oportunidad!")
    agregar_objeto(inventario_jugador, "Llave de salida")
    mostrar_inventario(inventario_jugador)
    
    # Usar la llave para abrir la salida y escapar
    print("\nEncuentras la salida del bosque encantado. ¡Usa la llave para escapar!")
    usar_objeto(inventario_jugador, "Llave de salida")
    print("¡Venciste al fantasma!")

def mostrar_ruta(estado):
    """Usa BFS para mostrar la ruta con menos saltos hasta una sala, evitando las bloqueadas."""
    nombres = list(estado["grafo"].adyacencia)
    for i, nombre in enumerate(nombres, start=1):
        print(f"{i}) {nombre}")
    eleccion = leer_opcion("¿A qué sala quieres ir? ", 1, len(nombres))
    destino = nombres[eleccion - 1]
    origen = estado["sala"]["nombre"]
    if destino == origen:
        print("Ya estás en esa sala.")
        return
    ruta = ruta_mas_corta(estado["grafo"], origen, destino, salas_bloqueadas(estado["mundo"]))
    if ruta is None:
        print("No hay ruta posible: el camino está bloqueado.")
    else:
        saltos = len(ruta) - 1
        print(f"Ruta ({saltos} salto{'s' if saltos != 1 else ''}): " + " -> ".join(ruta))


def mostrar_zonas(estado):
    """Usa DFS para mostrar qué salas se pueden alcanzar y cuáles quedan aisladas o bloqueadas."""
    bloqueadas = salas_bloqueadas(estado["mundo"])
    origen = estado["sala"]["nombre"]
    alcanzables = dfs(estado["grafo"], origen, bloqueadas)
    aisladas = zonas_aisladas(estado["grafo"], origen, bloqueadas)
    print(f"Alcanzables desde {origen}: {', '.join(alcanzables)}")
    if aisladas:
        print(f"Aisladas o bloqueadas: {', '.join(aisladas)}")
    else:
        print("No hay salas aisladas.")

def opcion_inventario(estado):
    """Muestra el inventario del jugador."""
    mostrar_inventario(estado["inventario"])


def opcion_historial(estado):
    """Muestra el historial de acciones."""
    mostrar_historial(estado["historial"])


def opcion_turnos(estado):
    """Ejecuta un turno completo del sistema de turnos."""
    simular_turnos(estado["turnos"], len(estado["turnos"]))


def opcion_combate(estado):
    """Combate final: solo en las salas más profundas. Devuelve True si el juego termina."""
    if estado["sala"]["profundidad"] < calcular_profundidad(estado["raiz"]):
        print("El fantasma solo aparece en las salas más profundas del bosque.")
        return False
    combate_final(estado["inventario"])
    return True


OPCIONES = [
    ("Moverse", mover),
    ("Ver inventario", opcion_inventario),
    ("Deshacer", deshacer),
    ("Ver historial", opcion_historial),
    ("Ver turnos", opcion_turnos),
    ("Recoger objeto", recoger),
    ("Ruta más corta", mostrar_ruta),
    ("Zonas alcanzables", mostrar_zonas),
    ("Combate final", opcion_combate),
]


def simular_juego():
    print("")
    print("AVENTURA EN EL BOSQUE ENCANTADO")
    print("")
    
    # Inventario inicial del gato (protagonista)
    inventario_jugador = [
        "Espada de Juguete", 
        "Bomba de Catnip", 
        "Varita Mágica de Plumas"
    ]
    
    mostrar_inventario(inventario_jugador)
    
    
    print(f"\nObjeto más repetido: {objeto_mas_repetido(inventario_jugador)}")

    estado = crear_estado(inventario_jugador)
    total = contar_salas(estado["raiz"])
    profundidad = calcular_profundidad(estado["raiz"])
    print(f"\nMazmorra generada: {total} salas, profundidad {profundidad}")

    while True:
        mostrar_menu(estado)
        salir = len(OPCIONES) + 1
        opcion = leer_opcion("Opción: ", 1, salir)
        if opcion == salir:
            print("¡Gracias por jugar!")
            break
        terminar = OPCIONES[opcion - 1][1](estado)
        if terminar:
            break

if __name__ == "__main__":
    simular_juego()