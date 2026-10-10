from collections import deque

def encolar_evento(cola, tipo, descripcion):
    """Agrega un evento al final de la cola."""
    cola.append({"tipo": tipo, "descripcion": descripcion})

def cargar_eventos_iniciales(cola):
    """Encola los eventos del mapa al iniciar la partida (cambien los textos por los de su historia)."""
    encolar_evento(cola, "enemigo", "un esbirro fantasma te bloquea el paso")
    encolar_evento(cola, "mensaje", "oyes un maullido lejano")
    encolar_evento(cola, "cofre", "encuentras un cofre con un ovillo de lana")
    encolar_evento(cola, "trampa", "pisas una telarania pegajosa")
    encolar_evento(cola, "enemigo", "un murcielago fantasma te ataca")

def procesar_siguiente_evento(cola):
    """Saca el evento que lleva más tiempo esperando (popleft) y lo muestra."""
    if not cola:
        print("No hay eventos pendientes.")
        return None
    evento = cola.popleft()       
    print(f"Evento: {evento['descripcion']} (quedan {len(cola)} eventos)")
    return evento
