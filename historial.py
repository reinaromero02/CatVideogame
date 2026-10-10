"""ayuda a apilar la accion en el historial"""
def registrar_accion (historial, tipo, **datos):
    accion = {"tipo": tipo}
    accion.update(datos)
    historial.append(accion)
    return accion

"""vuelve a la ultima accion sin apilar cuando el historial esta vacio, devuelve none"""
def deshacer_ultima(historial):
    if not historial:
        print("no hay acciones que deshacerr")
        return None
    return historial.pop()

"""devulve la accion"""
def consultar_ultima(historial):
    if not historial:
        return None
    return historial[-1]
