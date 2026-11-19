class Nodo:
    """Misión del árbol de misiones."""
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []
        self.completada = False


def agregar_hijo(padre, hijo):
    """Agrega una misión como hija de otra."""
    padre.hijos.append(hijo)


def preorden(nodo, nivel=0):
    """Imprime el árbol con sangría: primero el nodo, luego sus hijos."""
    marca = "[x]" if nodo.completada else "[ ]"
    print("    " * nivel + f"{marca} {nodo.nombre}")
    for hijo in nodo.hijos:
        preorden(hijo, nivel + 1)


def postorden(nodo, nivel=0):
    """Imprime primero los hijos y al final el nodo."""
    for hijo in nodo.hijos:
        postorden(hijo, nivel + 1)
    print("    " * nivel + nodo.nombre)


def altura(nodo):
    """Altura del árbol: una hoja tiene altura 0."""
    if not nodo.hijos:
        return 0
    return 1 + max(altura(hijo) for hijo in nodo.hijos)


def contar_hojas(nodo):
    """Cuenta las misiones sin hijos."""
    if not nodo.hijos:
        return 1
    total = 0
    for hijo in nodo.hijos:
        total += contar_hojas(hijo)
    return total


def contar_nodos(nodo):
    """Cuenta todos los nodos del árbol."""
    total = 1
    for hijo in nodo.hijos:
        total += contar_nodos(hijo)
    return total


def misiones_disponibles(nodo, padre_completado=True):
    """Misiones no completadas cuyo padre sí está completado."""
    disponibles = []
    if padre_completado and not nodo.completada:
        disponibles.append(nodo.nombre)
    for hijo in nodo.hijos:
        disponibles += misiones_disponibles(hijo, nodo.completada)
    return disponibles


def buscar_mision(nodo, nombre, padre=None):
    """Busca una misión y devuelve (misión, padre); (None, None) si no existe."""
    if nodo.nombre == nombre:
        return nodo, padre
    for hijo in nodo.hijos:
        encontrado, su_padre = buscar_mision(hijo, nombre, nodo)
        if encontrado is not None:
            return encontrado, su_padre
    return None, None


def completar_mision(raiz, nombre):
    """Completa una misión; no deja si su padre no está completado."""
    mision, padre = buscar_mision(raiz, nombre)
    if mision is None:
        print(f"Error: la misión '{nombre}' no existe.")
        return False
    if mision.completada:
        print(f"La misión '{nombre}' ya estaba completada.")
        return False
    if padre is not None and not padre.completada:
        print(f"Misión bloqueada: primero completa '{padre.nombre}'.")
        return False
    mision.completada = True
    print(f"¡Misión completada: {nombre}!")
    return True


def construir_arbol_misiones():
    """Construye el árbol de misiones del Bosque Encantado."""
    raiz = Nodo("Despertar en el Claro Encantado")
    sendero = Nodo("Cruzar el Sendero de Hongos")
    arbol_hueco = Nodo("Explorar el Árbol Hueco")
    bomba = Nodo("Recoger la Bomba de Catnip")
    murcielago = Nodo("Derrotar al Murciélago Fantasma")
    ovillo = Nodo("Conseguir el Ovillo de Lana")
    guarida = Nodo("Llegar a la Guarida del Fantasma")
    esbirros = Nodo("Derrotar a los 4 esbirros")
    escapar = Nodo("Tomar la llave y escapar")

    agregar_hijo(raiz, sendero)
    agregar_hijo(raiz, arbol_hueco)
    agregar_hijo(sendero, bomba)
    agregar_hijo(sendero, murcielago)
    agregar_hijo(arbol_hueco, ovillo)
    agregar_hijo(arbol_hueco, guarida)
    agregar_hijo(guarida, esbirros)
    agregar_hijo(esbirros, escapar)
    return raiz


class NodoDecision:
    """Nodo del árbol de decisión: pregunta (interno) o decisión (hoja)."""
    def __init__(self, pregunta=None, condicion=None, decision=None):
        self.pregunta = pregunta
        self.condicion = condicion
        self.decision = decision
        self.si = None
        self.no = None


def decidir(nodo, situacion):
    """Baja desde la raíz hasta una hoja y devuelve la decisión."""
    if nodo.decision is not None:
        return nodo.decision
    if nodo.condicion(situacion):
        return decidir(nodo.si, situacion)
    return decidir(nodo.no, situacion)


def construir_arbol_fantasma():
    """Árbol de decisión del Fantasma: 3 preguntas y 4 decisiones."""
    raiz = NodoDecision("¿El gato está cerca?",
                        lambda s: s.get("jugador_cerca", False))
    poca_vida = NodoDecision("¿Al fantasma le queda poca vida?",
                             lambda s: s.get("vida", 100) < 30)
    hay_esbirros = NodoDecision("¿Quedan esbirros vivos?",
                                lambda s: s.get("esbirros", 0) > 0)

    raiz.si = poca_vida
    raiz.no = hay_esbirros
    poca_vida.si = NodoDecision(decision="Huir a la Guarida")
    poca_vida.no = NodoDecision(decision="Atacar al gato")
    hay_esbirros.si = NodoDecision(decision="Pedir ayuda a los esbirros")
    hay_esbirros.no = NodoDecision(decision="Patrullar el bosque")
    return raiz


def inorden(nodo, nivel=0):
    """Árbol binario: izquierda (sí), nodo, derecha (no)."""
    if nodo is None:
        return
    inorden(nodo.si, nivel + 1)
    texto = nodo.pregunta if nodo.decision is None else "-> " + nodo.decision
    print("    " * nivel + texto)
    inorden(nodo.no, nivel + 1)


def construir_torneo():
    """Torneo de eliminación directa de 8 equipos: la raíz es la final."""
    final = Nodo("Final")
    semis = [Nodo("Semifinal 1"), Nodo("Semifinal 2")]
    cuartos = [Nodo(f"Cuartos {i}") for i in range(1, 5)]
    equipos = [Nodo(f"Equipo {letra}") for letra in "ABCDEFGH"]
    for semi in semis:
        agregar_hijo(final, semi)
    for i, cuarto in enumerate(cuartos):
        agregar_hijo(semis[i // 2], cuarto)
        agregar_hijo(cuarto, equipos[2 * i])
        agregar_hijo(cuarto, equipos[2 * i + 1])
    return final


def main():
    raiz = construir_arbol_misiones()
    print("=== ÁRBOL DE MISIONES ===")
    preorden(raiz)
    print(f"\nAltura: {altura(raiz)}")
    print(f"Hojas: {contar_hojas(raiz)}")
    print(f"Nodos visitados por el recorrido: {contar_nodos(raiz)}")
    print("Disponibles:", misiones_disponibles(raiz))

    print("\n=== COMPLETAR MISIONES ===")
    completar_mision(raiz, "Despertar en el Claro Encantado")
    print("Disponibles:", misiones_disponibles(raiz))
    completar_mision(raiz, "Cruzar el Sendero de Hongos")
    print("Disponibles:", misiones_disponibles(raiz))

    print("\n=== MISIÓN BLOQUEADA ===")
    completar_mision(raiz, "Tomar la llave y escapar")
    completar_mision(raiz, "Misión inventada")

    print("\n=== POSTORDEN ===")
    postorden(raiz)

    print("\n=== ÁRBOL DE DECISIÓN DEL FANTASMA ===")
    fantasma = construir_arbol_fantasma()
    inorden(fantasma)
    situaciones = [
        {"jugador_cerca": True, "vida": 20},
        {"jugador_cerca": True, "vida": 80},
        {"jugador_cerca": False, "esbirros": 3},
        {"jugador_cerca": False, "esbirros": 0},
        {},
    ]
    for s in situaciones:
        print(f"{s} -> {decidir(fantasma, s)}")

    print("\n=== CASO REAL: TORNEO DE ELIMINACIÓN DIRECTA ===")
    torneo = construir_torneo()
    preorden(torneo)
    equipos = contar_hojas(torneo)
    print(f"Rondas (altura): {altura(torneo)}")
    print(f"Equipos (hojas): {equipos}")
    print(f"Partidos: {contar_nodos(torneo) - equipos}")


if __name__ == "__main__":
    main()