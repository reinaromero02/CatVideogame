# CatVideogame
PBL de estructura de datos

# Aventura en el Bosque Encantado

## 1. Concepto del Juego
* **Mundo:** Bosque encantado.
* **Protagonista:** Un gato.
* **Antagonista:** Fantasma.
* **Objeto Especial:** Múltiples juguetes para gato (con diferentes propósitos: bombas, varita, espada, etc.).
* **Problema a Resolver:** Vencer al fantasma y a sus esbirros para que la familia del gato y él puedan vivir en paz.

---
## 2. Ejecución del Juego
```bash
python main.py
```
## 3. Menu de la partida
1. Moverse	Elige una sala conectada. Se registra en el historial y dispara el siguiente evento de la cola
2. Ver inventario	Muestra los juguetes del gato (inventario del Checkpoint 1)
3. Deshacer	Revierte la última acción del historial (vuelve a la sala anterior)
4. Ver historial	Muestra las acciones, de la más reciente a la más antigua
5. Ver turnos	Ejecuta un turno completo del sistema de turnos
6. Recoger objeto	Recoge el objeto de la sala actual y lo guarda en el inventario
7. Combate final	Solo en las salas más profundas: enfrentar a los 4 enemigos, tomar la llave y escapar
8. Salir	Termina la partida


## 4. Estructura del Proyecto
```text
https://github.com/reinaromero02/CatVideogame.git
CatVideogame/
├── main.py        # Archivo central: menú, bucle del juego e integración de los módulos
├── inventario.py  # Lista de objetos del jugador
├── historial.py   # Historial de acciones
├── eventos.py     # Eventos y turnos
├── mazmorra.py    # Mazmorra 
└── README.md      # Documentación técnica
```
## 5. Estructura de datos implementados

### Historial de acciones: pila (`historial.py`)

**Mecánica que implementa:** cada acción importante del jugador (moverse, recoger un objeto) se apila en el historial. Deshacer desapila la última acción y revierte su efecto, por ejemplo volviendo a la sala anterior.

**Por qué una pila (LIFO):** lo último que hiciste es lo primero que quieres deshacer. Una pila entrega siempre el elemento más reciente, que es justo el comportamiento de un "deshacer" (backtracking). Se implementa con una lista de Python: `append` apila y `pop()` desapila, ambas por el final de la lista.

**Por qué cada acción es un diccionario y no un texto:** para deshacer un movimiento hay que saber de dónde venía el jugador. Con un texto como `"mover_norte"` no se puede volver a la sala anterior; con un diccionario se guarda el `origen` y el `destino`.

```python
def apilar_accion(historial, tipo, **datos):
    """Registra una acción nueva en el historial con append."""
    accion = {"tipo": tipo}
    accion.update(datos)
    historial.append(accion)
    print("Acción registrada: " + describir_accion(accion))
    return accion


def deshacer_ultima_accion(historial):
    """Quita y devuelve la acción más reciente del historial con pop."""
    if len(historial) == 0:
        print("No hay nada que deshacer: el historial está vacío.")
        return None
    accion = historial.pop()
    print("Deshaciendo: " + describir_accion(accion))
    return accion
```


| Función | Qué hace en el juego |
|---|---|
| `apilar_accion` | Registra un movimiento o la recogida de un objeto |
| `deshacer_ultima_accion` | Deshace la última acción (con validación de historial vacío) |
| `ver_ultima_accion` | Consulta la última acción sin quitarla |
| `mostrar_historial` | Muestra todo el historial, de la más reciente a la más antigua |
| `deshacer_multiples` | Deshace varias acciones seguidas |
| `contar_acciones_de_tipo` | Cuenta cuántos movimientos o recogidas se han hecho |
| `invertir_historial` | Invierte la pila usando una pila auxiliar |

### Eventos y turnos: cola (`eventos.py`)

**Mecánica que implementa:** al iniciar la partida se encolan los eventos del bosque (enemigos, mensajes, cofres y trampas). Cada vez que el jugador se mueve, se procesa el siguiente evento de la cola. Además hay un sistema de turnos que rota entre 3 participantes: **Gato, Esbirro y Fantasma**.

**Por qué una cola (FIFO):** los eventos deben ocurrir en el orden en que fueron programados: el que llegó primero se atiende primero. Se usa `collections.deque` porque `popleft()` saca del frente en **O(1)**, mientras que `lista.pop(0)` es **O(n)** porque tiene que desplazar todos los elementos restantes.

```python
def procesar_siguiente_evento(cola_eventos):
    """Quita y devuelve el evento más antiguo de la cola con popleft."""
    if len(cola_eventos) == 0:
        print("No hay eventos pendientes.")
        return None
    evento = cola_eventos.popleft()
    print(f"Evento: {evento['descripcion']} (quedan {len(cola_eventos)} eventos)")
    return evento
```

**Sistema de turnos:** el participante sale por el frente con `popleft` y vuelve a entrar por el final con `append`, así la rotación se hace sola:

```python
def simular_turnos(turnos, cantidad):
    """Rota los turnos 'cantidad' veces: popleft saca al participante y append lo manda al final."""
    for _ in range(cantidad):
        participante = turnos.popleft()
        print(f"Turno de: {participante}")
        turnos.append(participante)
```


| Función | Qué hace en el juego |
|---|---|
| `encolar_evento` | Agrega un evento al final de la cola |
| `procesar_siguiente_evento` | Procesa el evento que lleva más tiempo esperando |
| `ver_siguiente_evento` | Muestra en el menú cuál es el próximo evento sin sacarlo |
| `procesar_multiples_eventos` | Procesa varios eventos seguidos |
| `contar_eventos_de_tipo` | Cuenta los eventos pendientes de un tipo (por ejemplo, enemigos) |
| `simular_turnos` | Ejecuta turnos completos del Gato, el Esbirro y el Fantasma |

### Mazmorra: recursividad (`mazmorra.py`)

**Mecánica que implementa:** el bosque se genera como un árbol de salas con nombres propios. Cada sala es un diccionario con su `nombre`, su `profundidad`, sus `hijos` (las salas conectadas) y un `objeto` opcional.

**Por qué recursividad:** el bosque es una estructura que se repite: cada sala conectada es a su vez "un bosque más pequeño". Por eso es natural generarlo con una función que se llama a sí misma, en vez de escribir bucles anidados para cada nivel.

* **Caso base:** se llegó a la profundidad máxima, o ya no quedan nombres de salas. La función devuelve la sala sin hijos.
* **Caso recursivo:** para cada rama, la función se llama a sí misma con `profundidad_actual + 1` y agrega el resultado como hijo.

```python
def generar_mazmorra(nombres, profundidad_actual=0, profundidad_maxima=2, ramas=2):
    """Genera recursivamente el bosque como un árbol de salas."""
    sala = {
        "nombre": nombres.pop(0),
        "profundidad": profundidad_actual,
        "hijos": [],
        "objeto": None,
    }

    if profundidad_actual == profundidad_maxima or not nombres:   # caso base
        return sala

    for _ in range(ramas):                                         # caso recursivo
        if nombres:
            hijo = generar_mazmorra(nombres, profundidad_actual + 1, profundidad_maxima, ramas)
            sala["hijos"].append(hijo)
    return sala
```

Con profundidad máxima 2 y 2 ramas por sala se generan 1 + 2 + 4 = **7 salas**.

**Árbol de la mazmorra** (entre corchetes, los objetos que esperan en las salas más profundas):

```text
- Claro Encantado
    - Sendero de Hongos
        - Arroyo de Luciernagas  [Bomba de Catnip]
        - Cueva del Murcielago  [Ovillo de Lana]
    - Arbol Hueco
        - Colina de la Luna
        - Guarida del Fantasma
```


| Mazmorra |
|---|---|
| `persona_actual` | Nombre propio de la sala (tomado de `NOMBRES_SALAS`) |
| `generacion` | `profundidad_actual` |
| `max_generaciones` | `profundidad_maxima` |
| Caso base: `generacion >= max_generaciones` | `profundidad_actual == profundidad_maxima or not nombres` |
| Caso recursivo: `for i in range(2)` | `for _ in range(ramas)` |
| Listas `personas` y `conexiones` | El propio árbol: cada sala guarda sus `hijos` |

| Función | Qué hace |
|---|---|
| `contar_salas` | Cuenta todas las salas del árbol |
| `contar_salas_por_nivel` | Devuelve cuántas salas hay en cada nivel, por ejemplo `{0: 1, 1: 2, 2: 4}` |
| `calcular_profundidad` | Calcula la profundidad real alcanzada |
| `marcar_salas_profundas` | Coloca objetos en las salas del nivel más profundo |
| `mostrar_arbol` | Imprime el árbol con sangría |

---

## 6. Complejidad de las operaciones principales

| Operación | Complejidad | Por qué |
|---|---|---|
| `apilar_accion` (`append`) | O(1) | Agrega al final de la lista |
| `deshacer_ultima_accion` (`pop()`) | O(1) | Quita del final de la lista, no hay que desplazar nada |
| `ver_ultima_accion` (`lista[-1]`) | O(1) | Acceso directo, se valida antes que la lista no esté vacía |
| `encolar_evento` (`append` en deque) | O(1) | Agrega al final |
| `procesar_siguiente_evento` (`deque.popleft()`) | O(1) | El deque está hecho para sacar por el frente |
| `list.pop(0)` (lo que **evitamos** para la cola) | O(n) | Desplaza todos los elementos una posición |
| `contar_acciones_de_tipo`, `contar_eventos_de_tipo` | O(n) | Recorren todos los elementos una vez |
| `contar_salas`, `calcular_profundidad`, `contar_salas_por_nivel` | O(n) | Visitan cada sala del árbol una sola vez (n = número de salas) |
| `generar_mazmorra` | O(n²) con lista, O(n) con deque | Hace n llamadas recursivas y cada `nombres.pop(0)` es O(n); con solo 7 salas el costo es despreciable |

---

## 7. Integración en una partida jugable (`main.py`)

Las tres estructuras trabajan juntas dentro del bucle del menú:

1. **Al iniciar:** la mazmorra se genera con su función recursiva, se marcan los objetos en las salas profundas, se cargan los eventos en la cola y se crean los turnos.
2. **Moverse:** el jugador elige una sala conectada. El movimiento se **apila** en el historial y se **desencola** el siguiente evento de la cola. Si el evento es un enemigo, el gato gasta un juguete del inventario (primero la Bomba de Catnip, luego la Espada de Juguete).
3. **Deshacer:** se **desapila** la última acción; si era un movimiento, el jugador vuelve de verdad a la sala anterior (backtracking).
4. **Recoger:** en las salas marcadas el jugador recoge un objeto, que entra al inventario del Checkpoint 1. Esa acción también queda en el historial y se puede deshacer (el objeto vuelve a la sala).
5. **Combate final:** solo está disponible en las salas más profundas. Es el combate del Checkpoint 1: se derrota a 4 enemigos, el enemigo 4 suelta la llave y el gato escapa.

```python
def mover(estado):
    """Mueve al jugador, lo registra en el historial y dispara el siguiente evento."""
    ...
    apilar_accion(estado["historial"], "mover", origen=sala, destino=destino)   # PILA
    estado["sala"] = destino
    print(f"Te mueves a: {destino['nombre']}")

    evento = procesar_siguiente_evento(estado["eventos"])                        # COLA
    manejar_evento(estado, evento)                                               # INVENTARIO
```

Todo el estado de la partida (sala actual, historial, cola de eventos, turnos e inventario) vive en un diccionario `estado` que se pasa a cada función.

---

## 8. Decisión: ¿qué pasa con un evento cuando se deshace un movimiento?

**Decisión: el evento se pierde.** Cuando el jugador deshace un movimiento vuelve a la sala anterior, pero el evento que se disparó con ese movimiento **no vuelve a la cola**.

**Por qué:**
* El evento ya ocurrió y tuvo efecto sobre el juego (por ejemplo, un enemigo ya consumió un juguete del inventario). Devolverlo a la cola obligaría a revertir también sus efectos.
* Mantiene sencilla la relación entre las dos estructuras: la pila deshace la **posición** del jugador y la cola solo avanza hacia adelante.
* Tiene sentido narrativo: el tiempo en el bosque sigue corriendo aunque el gato retroceda.

---

## 9. Casos límite

El programa nunca se cierra con un error: muestra un mensaje claro y sigue.

| Caso | Cómo se maneja |
|---|---|
| Deshacer con el historial vacío | `deshacer_ultima_accion` valida `len(historial) == 0` y muestra "No hay nada que deshacer" |
| Procesar un evento con la cola vacía | `procesar_siguiente_evento` avisa "No hay eventos pendientes" y devuelve `None` |
| Opción inválida en cualquier menú: texto, `0`, negativos, fuera de rango | `leer_opcion` captura `ValueError`, valida el rango y vuelve a pedir la opción |
| Moverse a una sala que no existe o no está conectada | Solo se ofrecen las salas hijas de la sala actual y la elección se valida con `leer_opcion` |
| Moverse desde una sala sin conexiones | `mover` muestra "No hay salas conectadas desde aquí" |
| Recoger donde no hay objeto | `recoger` muestra "No hay nada que recoger aquí" |
| Combate final en una sala que no es profunda | Se avisa que el fantasma solo aparece en las salas más profundas |
| `lista[-1]` en una lista vacía | `ver_ultima_accion` verifica que haya elementos antes de usar el índice |

---

## 10. Evidencia de ejecución

```text

AVENTURA EN EL BOSQUE ENCANTADO

Tus juguetes
- Espada de Juguete
- Bomba de Catnip
- Varita Mágica de Plumas

Objeto más repetido: Espada de Juguete

Mazmorra generada: 7 salas, profundidad 2

Estás en: Claro Encantado
Próximo evento en la cola: enemigo
1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial
5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir
Opción: 1
Salas conectadas: 1) Sendero de Hongos  2) Arbol Hueco
Elige una sala: 1
Acción registrada: Te moviste de Claro Encantado a Sendero de Hongos
Te mueves a: Sendero de Hongos
Evento: un esbirro fantasma te bloquea el paso (quedan 4 eventos)
Usaste 'Bomba de Catnip'

Estás en: Sendero de Hongos
Próximo evento en la cola: mensaje
1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial
5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir
Opción: 1
Salas conectadas: 1) Arroyo de Luciernagas  2) Cueva del Murcielago
Elige una sala: 2
Acción registrada: Te moviste de Sendero de Hongos a Cueva del Murcielago
Te mueves a: Cueva del Murcielago
Evento: oyes un maullido lejano (quedan 3 eventos)

Estás en: Cueva del Murcielago
Próximo evento en la cola: cofre
1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial
5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir
Opción: 4
1. Te moviste de Sendero de Hongos a Cueva del Murcielago
2. Te moviste de Claro Encantado a Sendero de Hongos

Estás en: Cueva del Murcielago
Próximo evento en la cola: cofre
1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial
5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir
Opción: 3
Deshaciendo: Te moviste de Sendero de Hongos a Cueva del Murcielago
Vuelves a: Sendero de Hongos

Estás en: Sendero de Hongos
Próximo evento en la cola: cofre
1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial
5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir
Opción: 5
Turno de: Gato
Turno de: Esbirro
Turno de: Fantasma

Estás en: Sendero de Hongos
Próximo evento en la cola: cofre
1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial
5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir
Opción: 3
Deshaciendo: Te moviste de Claro Encantado a Sendero de Hongos
Vuelves a: Claro Encantado

Estás en: Claro Encantado
Próximo evento en la cola: cofre
1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial
5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir
Opción: 7
El fantasma solo aparece en las salas más profundas del bosque.

Estás en: Claro Encantado
Próximo evento en la cola: cofre
1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial
5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir
Opción: 1
Salas conectadas: 1) Sendero de Hongos  2) Arbol Hueco
Elige una sala: 1
Acción registrada: Te moviste de Claro Encantado a Sendero de Hongos
Te mueves a: Sendero de Hongos
Evento: encuentras un cofre con un ovillo de lana (quedan 2 eventos)

Estás en: Sendero de Hongos
Próximo evento en la cola: trampa
1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial
5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir
Opción: 1
Salas conectadas: 1) Arroyo de Luciernagas  2) Cueva del Murcielago
Elige una sala: 1
Acción registrada: Te moviste de Sendero de Hongos a Arroyo de Luciernagas
Te mueves a: Arroyo de Luciernagas
Evento: pisas una telaraña pegajosa (quedan 1 eventos)

Estás en: Arroyo de Luciernagas
Próximo evento en la cola: enemigo
1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial
5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir
Opción: 1
No hay salas conectadas desde aquí.

Estás en: Arroyo de Luciernagas
Próximo evento en la cola: enemigo
1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial
5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir
Opción: 6
Obtuviste un'Bomba de Catnip'!
Acción registrada: Recogiste 'Bomba de Catnip' en Arroyo de Luciernagas

Estás en: Arroyo de Luciernagas
Próximo evento en la cola: enemigo
1. Moverse  2. Ver inventario  3. Deshacer  4. Ver historial
5. Ver turnos  6. Recoger objeto  7. Combate final  8. Salir
Opción: 7

INICIO DE COMBATE EN EL BOSQUE

¡Combate contra enemigo 1!
Usaste 'Bomba de Catnip'
Enemigo 1 derrotado. Total derrotados: 1

¡Combate contra enemigo 2!
Usaste 'Espada de Juguete'
Enemigo 2 derrotado. Total derrotados: 2

¡Combate contra enemigo 3!
Obtuviste un'Varita Mágica de Plumas'!
Usaste 'Varita Mágica de Plumas'
Enemigo 3 derrotado. Total derrotados: 3

¡Combate contra enemigo 4!
Obtuviste un'Varita Mágica de Plumas'!
Usaste 'Varita Mágica de Plumas'
Enemigo 4 derrotado. Total derrotados: 4
El enemigo 4 suelta la llave, ¡es tu oportunidad!
Obtuviste un'Llave de salida'!
Tus juguetes
- Varita Mágica de Plumas
- Llave de salida

Encuentras la salida del bosque encantado. ¡Usa la llave para escapar!
Usaste 'Llave de salida'
¡Venciste al fantasma!
```

---

## 11. Aporte de cada integrante

| Integrante | Aporte |
|---|---|
| (Nombre 1) | (por ejemplo: `historial.py`, pila y Guía 5) |
| (Nombre 2) | (por ejemplo: `eventos.py`, cola, turnos y Guía 6) |
| (Nombre 3) | (por ejemplo: `mazmorra.py`, recursividad y Guía 7) |
| (Nombre 4) | (por ejemplo: `main.py`, integración, README y pruebas de casos límite) |

---

## 12. Diagrama de fujo

<img width="577" height="1107" alt="juegogato drawio" src="https://github.com/user-attachments/assets/786eab2d-8aea-4d71-9ec4-7c6fd5df404f" />

