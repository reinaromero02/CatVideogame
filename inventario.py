"""Funcion para agregar los objetos a la mochila"""
def agregar_objeto(inventario, item):
    inventario.append(item)
    print(f"Obtuviste un'{item}'!")

"""Funcion para soltar los objetos de la mochila con .remove"""
def soltar_objeto(inventario, item):
    if item in inventario:
        inventario.remove(item)
        print(f"Soltaste '{item}'")
        return True
    else:
        print("No tienes '{item}' en tu mochila")
        return False

"""Funcion para usar un objeto y eliminarlo de la mochila"""
def usar_objeto(inventario, item):
    if item in inventario:
        inventario.remove(item)
        print(f"Usaste '{item}'")
        return True
    else:
        print(f"No puedes usar '{item}', no está en tu mochila")
        return False
    
"""Funcion para contar los objetos en la mochila"""
def contar_objetos(inventario, item):
    return inventario.count(item)

"""Funcion para vaciar inventario"""
def vaciar_inventario(inventario):
    while len(inventario) > 0:
        soltar_objeto(inventario, inventario[0])
    print("Tu inventario se ha vaciado completamente.")

"""Mostrar el objeto mas repetido en la mochila"""
def objeto_mas_repetido(inventario):
    if not inventario:
        return None
    mas_repetido = None
    max_count = 0
    for item in inventario:
        conteo = contar_objetos(inventario, item)
        if conteo > max_count:
            max_count = conteo
            mas_repetido = item
    return mas_repetido

"""Reemplazar un objeto en la mochila"""
def reemplazar_objeto(inventario, item_viejo, item_nuevo):
    if item_viejo not in inventario:
        print(f"No tienes '{item_viejo}' en tu mochila para reemplazarlo.")
        return False
    soltar_objeto(inventario, item_viejo)
    agregar_objeto(inventario, item_nuevo)
    print(f"Has reemplazado '{item_viejo}' por '{item_nuevo}'.")
    return True
"""Funcion para mostrar el inventario"""
def mostrar_inventario(inventario):
    print("Tus juguetes")
    if not inventario:
        print("Tu mochila está vacía.")
    else:
        for item in inventario:
            print(f"- {item}")