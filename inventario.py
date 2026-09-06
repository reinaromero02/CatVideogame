"""Funcion para agregar los objetos a la mochila"""
def agregar_objeto(inventario, item):
    inventario.append(item)
    print("Obtuviste un'{item}'!")

"""Funcion para soltar los objetos de la mochila con .remove"""
def soltar_objeto(inventario, item):
    if item in inventario:
        inventario.remove(item)
        print("Soltaste '{item}'")
        return True
    else:
        print("No tienes '{item}' en tu mochila")
        return False

"""Funcion para usar un objeto y eliminarlo de la mochila"""
def usar_objeto(inventario, item):
    if item in inventario:
        inventario.remove(item)
        print("Usaste '{item}'")
        return True
    else:
        print("No puedes usar '{item}', no está en tu mochila")
        return False
    
"""Funcion para contar los objetos en la mochila"""
def contar_objetos(inventario, item):
    return inventario.count(item)

"""Funcion para vaciar inventario"""
def vaciar_inventario(inventario):
    while len(inventario) > 0:
        soltar_objeto(inventario, inventario[0])
    print("Tu inventario se ha vaciado completamente.")

