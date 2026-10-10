from collections import deque


"""hace que se agreguee un evento al final de la cola"""
def encolar_evento(cola_eventos, tipo, descripcion):
    evento = {"tipo": tipo, "descripcion": descripcion}
    cola_eventos.append(evento)

"""quita y devuelve el evento mas antiguo"""
def procesar_siguiente_evento(cola_eventos):
    if len(cola_eventos) == 0:
        print("No hay eventos pendientes.")
        return None
    evento = cola_eventos.popleft()
    print(f"Evento: {evento['descripcion']} (quedan {len(cola_eventos)} eventos)")
    return evento

"""consulta el evento mas antiguio"""
def ver_siguiente_evento(cola_eventos):
    if len(cola_eventos) == 0:
        return None
    return cola_eventos[0]



"""procesa hasta la cantidad de eventos seguidos"""
def procesar_multiples_eventos(cola_eventos, cantidad):
    procesados = []
    for _ in range(cantidad):
        evento = procesar_siguiente_evento(cola_eventos)
        if evento is None:
            break
        procesados.append(evento)
    return procesados
"""cuenta los eventos de tipo y cuantos son pendientes"""
def contar_eventos_de_tipo(cola_eventos, tipo):
    contador = 0
    for evento in cola_eventos:
        if evento["tipo"] == tipo:
            contador += 1
    return contador


""""""
def simular_turnos(turnos, cantidad):
    for _ in range(cantidad):
        participante = turnos.popleft()
        print(f"Turno de: {participante}")
        turnos.append(participante)