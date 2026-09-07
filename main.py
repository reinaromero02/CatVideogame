from inventario import (
    agregar_objeto,
    soltar_objeto,
    usar_objeto,
    vaciar_inventario,
    objeto_mas_repetido,
    reemplazar_objeto,
    mostrar_inventario
)

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
    
    # solo para probar si sirven las funciones de inventario
    print(f"\nObjeto más repetido: {objeto_mas_repetido(inventario_jugador)}")
    
    
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
    usar_objeto(inventario_jugador, "Llave de la salida")
    print("¡Venciste al fantasma!")

if __name__ == "__main__":
    simular_juego()