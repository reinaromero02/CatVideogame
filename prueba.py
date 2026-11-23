import builtins
import io
from contextlib import redirect_stdout

import main
from grafo import Grafo
from recorridos import bfs, ruta_mas_corta, dfs, zonas_aisladas
from estado_mundo import (
    crear_mundo,
    objeto_en_sala,
    quitar_objeto,
    desbloquear,
    motivo_bloqueo,
    fue_recogido,
    salas_bloqueadas,
)
from mazmorra import SENDERO, ARROYO, ARBOL, GUARIDA
from misiones import completar_mision, misiones_disponibles, construir_arbol_misiones

def con_entradas(respuestas, funcion, *args):
    pendientes = iter(respuestas)
    original = builtins.input
    builtins.input = lambda _="": next(pendientes)
    try:
        with redirect_stdout(io.StringIO()):
            return funcion(*args)
    finally:
        builtins.input = original

def silencioso(funcion, *args):
    with redirect_stdout(io.StringIO()):
        return funcion(*args)

def nuevo_estado():
    return silencioso(main.crear_estado, ["Espada de Juguete", "Bomba de Catnip", "Varita Mágica de Plumas"])

def ir_a(estado, destino):
    vecinos = estado["grafo"].vecinos(estado["sala"]["nombre"])
    con_entradas([str(vecinos.index(destino) + 1)], main.mover, estado)

def prueba_grafo_generico():
    g = Grafo()
    for a, b in [("Gato", "Perro"), ("Perro", "Loro"), ("Hada", "Duende")]:
        g.agregar_arista(a, b)
    assert ruta_mas_corta(g, "Gato", "Loro") == ["Gato", "Perro", "Loro"]
    assert ruta_mas_corta(g, "Gato", "Hada") is None
    assert ruta_mas_corta(g, "Gato", "Dragón") is None
    assert dfs(g, "Dragón") == []
    assert bfs(g, "Gato", {"Gato"}) == {}
    assert zonas_aisladas(g, "Gato") == ["Hada", "Duende"]
    assert g.vecinos("Dragón") == []
    g.agregar_arista("Gato", "Perro")
    assert g.vecinos("Gato") == ["Perro"]

def prueba_mapa_con_bloqueos():
    estado = nuevo_estado()
    bloqueadas = salas_bloqueadas(estado["mundo"])
    assert bloqueadas == {ARBOL}
    ruta = ruta_mas_corta(estado["grafo"], "Claro Encantado", GUARIDA, bloqueadas)
    assert ruta is not None and ARBOL not in ruta
    assert len(ruta) - 1 == 3
    libre = ruta_mas_corta(estado["grafo"], "Claro Encantado", GUARIDA)
    assert len(libre) - 1 == 2

def prueba_diccionario_sin_keyerror():
    mundo = crear_mundo({"nombre": "Sala", "profundidad": 0, "hijos": [], "objeto": None}, {})
    assert objeto_en_sala(mundo, "Sala Fantasma") is None
    assert quitar_objeto(mundo, "Sala Fantasma") is None
    assert desbloquear(mundo, "Sala Fantasma") is False
    assert motivo_bloqueo(mundo, "Sala Fantasma") is None
    assert fue_recogido(mundo, "Nada") is False

def prueba_misiones():
    raiz = construir_arbol_misiones()
    assert silencioso(completar_mision, raiz, "Misión inventada") is False
    assert silencioso(completar_mision, raiz, "Tomar la llave y escapar") is False
    assert silencioso(completar_mision, raiz, "Despertar en el Claro Encantado") is True
    assert silencioso(completar_mision, raiz, "Despertar en el Claro Encantado") is False
    disponibles = misiones_disponibles(raiz)
    assert "Cruzar el Sendero de Hongos" in disponibles
    assert "Tomar la llave y escapar" not in disponibles

def prueba_menu_opciones_invalidas():
    numero = con_entradas(["abc", "", "0", "-3", "99", "2"], main.leer_opcion, "Opción: ", 1, 5)
    assert numero == 2

def prueba_deshacer_historial_vacio():
    estado = nuevo_estado()
    silencioso(main.deshacer, estado)
    assert estado["sala"]["nombre"] == "Claro Encantado"

def prueba_sala_bloqueada_no_deja_pasar():
    estado = nuevo_estado()
    con_entradas(["2"], main.mover, estado)
    assert estado["sala"]["nombre"] == "Claro Encantado"
    assert len(estado["historial"]) == 0

def prueba_recoger_sin_objeto():
    estado = nuevo_estado()
    silencioso(main.recoger, estado)
    assert len(estado["historial"]) == 0

def prueba_bomba_desbloquea_y_deshacer_no_revierte_progreso():
    estado = nuevo_estado()
    ir_a(estado, SENDERO)
    ir_a(estado, ARROYO)
    silencioso(main.recoger, estado)
    assert motivo_bloqueo(estado["mundo"], ARBOL) is None
    silencioso(main.deshacer, estado)
    assert objeto_en_sala(estado["mundo"], ARROYO) == "Bomba de Catnip"
    assert motivo_bloqueo(estado["mundo"], ARBOL) is None

def prueba_combate_exige_misiones():
    estado = nuevo_estado()
    assert silencioso(main.opcion_combate, estado) is False
    ir_a(estado, SENDERO)
    ir_a(estado, ARROYO)
    silencioso(main.recoger, estado)
    ir_a(estado, GUARIDA)
    assert silencioso(main.opcion_combate, estado) is False
    ir_a(estado, ARBOL)
    ir_a(estado, GUARIDA)
    assert silencioso(main.opcion_combate, estado) is True

PRUEBAS = [
    prueba_grafo_generico,
    prueba_mapa_con_bloqueos,
    prueba_diccionario_sin_keyerror,
    prueba_misiones,
    prueba_menu_opciones_invalidas,
    prueba_deshacer_historial_vacio,
    prueba_sala_bloqueada_no_deja_pasar,
    prueba_recoger_sin_objeto,
    prueba_bomba_desbloquea_y_deshacer_no_revierte_progreso,
    prueba_combate_exige_misiones,
]

if __name__ == "__main__":
    fallidas = 0
    for prueba in PRUEBAS:
        try:
            prueba()
            print(f"OK    {prueba.__name__}")
        except AssertionError:
            fallidas += 1
            print(f"FALLA {prueba.__name__}")
    print(f"\n{len(PRUEBAS) - fallidas} de {len(PRUEBAS)} pruebas pasaron.")
