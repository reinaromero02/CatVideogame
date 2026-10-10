"""describe en texto la accion que se realiza"""
def describir_accion(accion):
    if accion["tipo"] == "mover":
        return f"Te moviste de {accion['origen']['nombre']} a {accion['destino']['nombre']}"
    if accion["tipo"] == "recoger":
        return f"Recogiste '{accion['objeto']}' en {accion['sala']['nombre']}"
    return f"Acción: {accion['tipo']}"

"""registra otra accio con append"""
def apilar_accion(historial, tipo, **datos):
   
    accion = {"tipo": tipo}
    accion.update(datos)
    historial.append(accion)
    print("Acción registrada: " + describir_accion(accion))   # describir_accion, no "+ accion"
    return accion

"""quita la accion y devuelve la ultimaa"""
def deshacer_ultima_accion(historial):
    if len(historial) == 0:
        print("No hay nada que deshacer: el historial está vacío.")
        return None
    accion = historial.pop()
    print("Deshaciendo: " + describir_accion(accion))
    return accion

"""consulta la ultima accion sin quitarla del historial"""
def ver_ultima_accion(historial):
    if len(historial) == 0:
        return None
    return historial[-1]

"""deshace las acciones hasta la ultima"""
def deshacer_multiples(historial, cantidad):
    
    deshechas = []
    for _ in range(cantidad):
        accion = deshacer_ultima_accion(historial)
        if accion is None:          
            break
        deshechas.append(accion)
    return deshechas

"""Cuenta cuantas acciones de un tipo hay en el historial."""
def contar_acciones_de_tipo(historial, tipo):
    contador = 0
    for accion in historial:
        if accion["tipo"] == tipo:
            contador += 1
    return contador

"""invierte la pila para usar una pilaa auxiliar"""
def invertir_historial(historial):  
    auxiliar = []
    while len(historial) > 0:
        auxiliar.append(historial.pop())
    return auxiliar