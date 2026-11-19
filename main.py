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
    generar_mazmorra,
    contar_salas,
    calcular_profundidad,
    marcar_salas_profundas,
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
    """Crea la mazmorra, la cola de eventos y los turnos de la partida."""
    raiz = generar_mazmorra(list(NOMBRES_SALAS))
    marcar_salas_profundas(raiz, ["Bomba de Catnip", "Ovillo de Lana"], 2)
    eventos = deque()
    cargar_eventos_iniciales(eventos)
    return {
        "raiz": raiz,
        "sala": raiz,
        "historial": [],
        "eventos": eventos,
        "turnos": deque(["Gato", "Esbirro", "Fantasma"]),
        "inventario": inventario_jugador,
    }


def manejar_evento(estado, evento):
    """Aplica el efecto de un evento sobre el inventario del jugador."""
    if evento is None:
        return
    if evento["tipo"] == "enemigo":
        if "Bomba de Catnip" in estado["inventario"]:
            usar_objeto(estado["inventario"], "Bomba de Catnip")
        elif "Espada de Juguete" in estado["inventario"]:
            usar_objeto(estado["inventario"], "Espada de Juguete")
        else:
            print("No tienes juguetes: te defiendes con las garras.")


def mostrar_menu(estado):
    """Muestra la sala actual, el próximo evento y las opciones del menú."""
    print(f"\nEstás en: {estado['sala']['nombre']}")
    proximo = ver_siguiente_evento(estado["eventos"])
    if proximo:
        print(f"Próximo evento en la cola: {proximo['tipo']}")
    print("1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial")
    print("5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir")


def mover(estado):
    """Mueve al jugador, lo registra en el historial y dispara el siguiente evento."""
    sala = estado["sala"]
    if not sala["hijos"]:
        print("No hay salas conectadas desde aquí.")
        return
    opciones = "  ".join(f"{i}) {h['nombre']}" for i, h in enumerate(sala["hijos"], start=1))
    print("Salas conectadas: " + opciones)
    eleccion = leer_opcion("Elige una sala: ", 1, len(sala["hijos"]))
    destino = sala["hijos"][eleccion - 1]

    apilar_accion(estado["historial"], "mover", origen=sala, destino=destino)
    estado["sala"] = destino
    print(f"Te mueves a: {destino['nombre']}")

    evento = procesar_siguiente_evento(estado["eventos"])
    manejar_evento(estado, evento)


def recoger(estado):
    """Recoge el objeto de la sala actual y lo guarda en el inventario."""
    sala = estado["sala"]
    if sala["objeto"] is None:
        print("No hay nada que recoger aquí.")
        return
    objeto = sala["objeto"]
    agregar_objeto(estado["inventario"], objeto)
    sala["objeto"] = None
    apilar_accion(estado["historial"], "recoger", objeto=objeto, sala=sala)


def deshacer(estado):
    """Revierte la última acción del historial."""
    accion = deshacer_ultima_accion(estado["historial"])
    if accion is None:
        return
    if accion["tipo"] == "mover":
        estado["sala"] = accion["origen"]
        print(f"Vuelves a: {accion['origen']['nombre']}")
    elif accion["tipo"] == "recoger":
        soltar_objeto(estado["inventario"], accion["objeto"])
        accion["sala"]["objeto"] = accion["objeto"]


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
        opcion = leer_opcion("Opción: ", 1, 8)
        if opcion == 1:
            mover(estado)
        elif opcion == 2:
            mostrar_inventario(estado["inventario"])
        elif opcion == 3:
            deshacer(estado)
        elif opcion == 4:
            mostrar_historial(estado["historial"])
        elif opcion == 5:
            simular_turnos(estado["turnos"], len(estado["turnos"]))
        elif opcion == 6:
            recoger(estado)
        elif opcion == 7:
            if estado["sala"]["profundidad"] < profundidad:
                print("El fantasma solo aparece en las salas más profundas del bosque.")
            else:
                combate_final(estado["inventario"])
                break
        else:
            print("¡Gracias por jugar!")
            break

if __name__ == "__main__":
    simular_juego()