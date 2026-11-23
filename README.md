# CatVideogame
PBL de estructura de datos

# Aventura en el Bosque Encantado

* **Mundo:** Bosque encantado.
* **Protagonista:** Un gato.
* **Antagonista:** Fantasma.
* **Objeto Especial:** Múltiples juguetes para gato (con diferentes propósitos: bombas, varita, espada, etc.).
* **Problema a Resolver:** Vencer al fantasma y a sus esbirros para que la familia del gato y él puedan vivir en paz.

---
**Repositorio:** [https://github.com/reinaromero02/CatVideogame.git](https://github.com/reinaromero02/CatVideogame.git)
```text
CatVideogame/
├── main.py                # Juego
├── inventario.py          # Lista de objetos del jugador
├── juegogato.drawio.png   # Diagrama de flujo
└── README.md              # Documentación en formato Markdown

```text
Algoritmo CombateYEscapeAutomatico
	Definir enemigosDerrotados, vidaJugador, vidaEnemigo Como Entero
	Definir jugadorAtaca, hizoDano, enemigoAtaca Como Logico
	Definir juegoTerminado, enemigoDerrotadoActual Como Logico
	
	enemigosDerrotados <- 0
	vidaJugador <- 100
	juegoTerminado <- Falso
	
	Mientras NO juegoTerminado Hacer
		vidaEnemigo <- 50
		Escribir "=== Aparece el enemigo ", (enemigosDerrotados + 1), " ==="
		enemigoDerrotadoActual <- Falso
		
		Mientras NO enemigoDerrotadoActual Y NO juegoTerminado Hacer
			jugadorAtaca <- (Aleatorio(1, 100) > 30)
			
			Si jugadorAtaca Entonces
				hizoDano <- (Aleatorio(1, 100) > 20)
				Si hizoDano Entonces
					vidaEnemigo <- vidaEnemigo - 25
					Escribir "Atacas con éxito. Vida enemigo: ", vidaEnemigo
					
					Si vidaEnemigo <= 0 Entonces
						enemigosDerrotados <- enemigosDerrotados + 1
						enemigoDerrotadoActual <- Verdadero
						
						Si enemigosDerrotados = 4 Entonces
							Escribir "El enemigo 4 suelta la llave (Jugador la obtiene)."
							Escribir "Usas la llave para abrir la salida y escapar."
							Escribir "¡ESCAPASTE!"
							Escribir "FIN: Victoria"
							juegoTerminado <- Verdadero
						FinSi
					FinSi
				SiNo
					Escribir "Atacaste pero no hiciste daño."
				FinSi
			SiNo
				enemigoAtaca <- (Aleatorio(1, 100) > 40)
				Si enemigoAtaca Entonces
					vidaJugador <- vidaJugador - 20
					Escribir "El enemigo te ataca. Vida jugador: ", vidaJugador
					
					Si vidaJugador <= 0 Entonces
						Escribir "PERDISTE"
						Escribir "FIN: Derrota"
						juegoTerminado <- Verdadero
					FinSi
				SiNo
					Escribir "El enemigo intentó atacar pero falló."
				FinSi
			FinSi
		FinMientras
	FinMientras
FinAlgoritmo
```
# Explicación breve: 
```text
Para esta primera entrega desarrollamos la mecánica de combate y escape del videojuego "CatVideogame". Tomamos la decisión de implementar un sistema secuencial en el cual el jugador debe enfrentarse a cuatro enemigos consecutivos utilizando estructuras de control condicionales, la lógica de los ataques y el cálculo de daño se basaron en probabilidades aleatorias para brindarle dinamismo al juego. Asimismo, definimos que la derrota del cuarto enemigo active de manera automática la entrega de la llave de salida, cumpliendo así la condición de victoria y escape del gatito.
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
7. Ver misiones	Muestra el árbol de misiones, lo disponible por etapa y los puntos por rama
8. Combate final	Solo en la Guarida y si el árbol de misiones lo permite: enfrentar a los 4 enemigos, tomar la llave y escapar
9. Salir	Termina la partida


## 4. Estructura del Proyecto
```text
https://github.com/reinaromero02/CatVideogame.git
CatVideogame/
├── main.py        # Archivo central: menú, bucle del juego e integración de los módulos
├── inventario.py  # Lista de objetos del jugador
├── historial.py   # Historial de acciones
├── eventos.py     # Eventos y turnos
├── mazmorra.py    # Mazmorra 
├── grafo.py         # Clase Grafo genérica (lista de adyacencia)
├── recorridos.py    # BFS, DFS, ruta más corta y zonas aisladas
├── estado_mundo.py  # Diccionario con el estado del mundo
├── misiones.py    # Árbol de misiones: condiciones, efectos y recorridos
├── arboles.py     # Nodos y funciones base del árbol
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

### Árboles: el árbol de misiones (`misiones.py`, `arboles.py`)
**Qué parte del juego resuelve:** las misiones y sus dependencias. Hay 9 misiones y altura 4. Cada misión depende de una sola misión anterior, por eso es un árbol y no un grafo. Una misión solo está disponible si no está completada y su padre sí lo está.

```text
Despertar en el Claro Encantado
├── Cruzar el Sendero de Hongos
│   ├── Recoger la Bomba de Catnip
│   └── Derrotar al Murciélago Fantasma
└── Explorar el Árbol Hueco
    ├── Conseguir el Ovillo de Lana
    └── Llegar a la Guarida del Fantasma
        └── Derrotar a los 4 esbirros
            └── Tomar la llave y escapar
```

**Completar una misión tiene efecto en la partida:** suma puntos al diccionario del mundo (135 en total si se completan todas) y, en el caso de *Recoger la Bomba de Catnip*, desbloquea el Árbol Hueco (elimina el bloqueo del diccionario del mundo, lo que cambia las rutas de BFS y DFS). Las misiones se completan solas cuando se cumple su condición y su dependencia (`revisar_misiones`), y el combate final solo se permite cuando *Derrotar a los 4 esbirros* está disponible.

**Cómo se conectan las tres estructuras:** el diccionario del mundo (visitas, objetos recogidos, bloqueos) guarda lo que hace el jugador. El árbol de misiones lee ese diccionario para saber qué misiones se cumplieron. Al completarse la misión de la Bomba, el árbol modifica el diccionario (quita el bloqueo) y eso cambia las rutas que calcula el grafo.

**Recorridos y para qué se usan:**

| Recorrido | Uso en el juego |
|---|---|
| Preorden | Mostrar el árbol con sangría (menú "Ver misiones") |
| Por niveles | Listar lo disponible por etapa |
| Postorden | Sumar los puntos de una rama (primero los hijos, al final el nodo) |

**Por qué esta estructura:** las dependencias entre misiones forman una jerarquía, y un árbol permite saber qué se desbloquea al completar un nodo.

**Complejidad:** cada recorrido es O(n), con n el número de misiones. `completar_mision` es O(n) porque primero busca la misión. `revisar_misiones` hace como máximo n pasadas de O(n), o sea O(n²), que con 9 misiones es despreciable.

**Decisión al deshacer:** las misiones completadas son progreso permanente. Si el jugador deshace un movimiento o un objeto recogido, la misión ya completada no se revierte.

**Aporte de Andrea:** `misiones.py` (recompensas, condiciones, efectos, revisión automática y vista del árbol) y la sección de árboles de este README.

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
| `puntos_de_rama`, `misiones_por_nivel`, `mostrar_misiones` | O(n) | Recorren cada misión una sola vez (n = número de misiones) |
| `completar_mision` | O(n) | Primero busca la misión recorriendo el árbol |
| `revisar_misiones` | O(n²) | Como máximo n pasadas de O(n); con 9 misiones es despreciable |

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
| (Camila Julian) | (`historial.py`, pila) |
| (Reina Romero) | (`eventos.py`, cola, turnos) |
| (Andrea Lopez y Camila Peñate) | (`mazmorra.py`, recursividad ; `misiones.py`, árbol de misiones) |
| (Camila Peñate) | (`main.py`, integración, README y pruebas de casos límite) |

---

## 12. Diagrama de fujo

<img width="577" height="1107" alt="juegogato drawio" src="https://github.com/user-attachments/assets/786eab2d-8aea-4d71-9ec4-7c6fd5df404f" />


## Grafos: el mapa del bosque (`grafo.py`, `recorridos.py`)

**Qué parte del juego resuelve:** el mapa. La mazmorra del Checkpoint 2 es un árbol, y le agregamos 2 atajos (Cueva del Murciélago con Colina de la Luna, y Arroyo de Luciérnagas con Guarida del Fantasma) para que el mapa tenga ciclos y caminos alternativos. El jugador se mueve por los vecinos del grafo. BFS calcula la ruta con menos saltos entre dos salas (menú "Ruta más corta") y DFS dice qué salas se pueden alcanzar y cuáles quedan aisladas (menú "Zonas alcanzables"). Los dos evitan las salas bloqueadas del diccionario del mundo.

**Por qué esta estructura:**
* La clase `Grafo` es genérica (guarda cualquier tipo de nodo) y no depende de un solo mapa. Usa una lista de adyacencia (un diccionario `{nodo: [vecinos]}`) porque el mapa tiene pocas conexiones comparadas con todas las posibles, y la lista ocupa O(V + E) frente a O(V²) de una matriz.
* BFS usa una fila (`deque`) y visita por capas, así que garantiza llegar por el camino con menos saltos.
* DFS es recursivo y baja por un camino hasta el fondo antes de retroceder. No garantiza el camino más corto, pero basta para saber qué se puede alcanzar.

**Complejidad:**

| Operación | Complejidad |
|---|---|
| BFS y DFS | O(V + E) |
| `ruta_mas_corta` | O(V + E) |
| `vecinos` | O(1) |
| `agregar_arista` | O(d), con d = grado del nodo (muy pequeño en este mapa) |

## Diccionarios: el estado del mundo (`estado_mundo.py`)

**Qué parte del juego resuelve:** lo que cambia mientras se juega y el juego necesita consultar rápido: qué salas están bloqueadas y por qué, qué objeto hay en cada sala, cuántas veces se visitó cada sala, qué objetos ya se recogieron y los puntos. Los objetos de las salas viven en este diccionario (ya no dentro de la sala).

**Cómo está hecho:** las claves son tuplas `(tipo, nombre)`, por ejemplo `("objeto", "Arroyo de Luciérnagas")`, `("bloqueada", "Árbol Hueco")` o `("visitas", "Claro Encantado")`. Son únicas e inmutables, y nunca usamos una lista como clave. El valor es lo que va cambiando.

| Operación | Función |
|---|---|
| Consulta con `.get()` | `objeto_en_sala`, `motivo_bloqueo`, `fue_recogido` |
| Actualización | `registrar_visita`, `sumar_puntos` |
| Inserción | `colocar_objeto` (por ejemplo, el evento de cofre) |
| Eliminación | `quitar_objeto` (al recoger), `desbloquear` |
| Filtran o resumen | `salas_visitadas`, `salas_bloqueadas`, `objetos_pendientes`, `resumen_mundo` |

**Por qué esta estructura:** buscar por clave en un diccionario es O(1) en promedio, mientras que buscar en una lista es O(n). Además `.get()`, `in` y `pop` con valor por defecto evitan el `KeyError` cuando se consulta algo que no existe.

**Trabaja con las otras estructuras:** `salas_bloqueadas` se le pasa a BFS y DFS para que eviten esas salas, y completar una misión del árbol puede eliminar un bloqueo.

**Complejidad:** `get`, insertar y eliminar son O(1) en promedio. Las funciones que filtran recorren las k claves del diccionario: O(k).

## Checkpoint 3: grafo, árbol de misiones y diccionario de estados

### Cómo ejecutar

Requiere Python 3 y no necesita instalar nada.

```bash
python main.py       # el juego
python pruebas.py    # pruebas automáticas de casos límite
```

### Menú del juego

| Opción | Qué hace |
|---|---|
| 1. Moverse | Se mueve por las conexiones del grafo, lo registra en el historial y dispara el siguiente evento |
| 2. Ver inventario | Muestra los juguetes del gato |
| 3. Deshacer | Revierte la última acción (posición e inventario) |
| 4. Ver historial | Acciones de la más reciente a la más antigua |
| 5. Ver turnos | Un turno completo: Gato, Esbirro y Fantasma |
| 6. Recoger objeto | Recoge el objeto de la sala (lo toma del diccionario del mundo) |
| 7. Ruta más corta | BFS: ruta con menos saltos hasta una sala, evitando las bloqueadas |
| 8. Zonas alcanzables | DFS: salas alcanzables y salas aisladas o bloqueadas |
| 9. Estado del mundo | Resumen del diccionario: visitas, bloqueos, objetos y puntos |
| 10. Ver misiones | Árbol de misiones, lo disponible por etapa y puntos por rama |
| 11. Combate final | Solo en la Guarida y si el árbol de misiones lo permite |
| 12. Salir | Termina la partida |

### Funcionalidades del juego hasta ahora

* Inventario con listas y combate contra 4 enemigos con llave de salida (Checkpoint 1).
* Historial con pila para deshacer, eventos y turnos con colas, y mazmorra generada con recursividad (Checkpoint 2).
* Mapa como grafo con caminos alternativos, rutas con BFS y zonas con DFS.
* Estado del mundo en un diccionario: salas bloqueadas, objetos, visitas y puntos.
* Árbol de misiones con dependencias, efectos y recompensas.
* Casos límite manejados con mensajes claros, sin cerrar el programa.

### Cómo trabajan juntas las tres estructuras

Las estructuras dependen unas de otras:

1. El Árbol Hueco empieza **bloqueado** en el diccionario del mundo (un árbol caído tapa el camino).
2. El **grafo** lo sabe: moverse no deja entrar, y BFS y DFS evitan esa sala. Por eso la ruta a la Guarida usa el atajo (3 saltos) en vez del camino directo (2 saltos).
3. Al recoger la Bomba de Catnip se completa la misión del **árbol** *Recoger la Bomba de Catnip*, que **elimina el bloqueo** del diccionario. Desde ese momento la ruta más corta cambia.
4. Si el jugador llega a la Guarida por el atajo antes de explorar el Árbol Hueco, la misión *Llegar a la Guarida* **espera** (su padre aún no está completado) y se completa en cascada al explorarlo.
5. El combate final solo se permite si el árbol de misiones lo habilita (*Derrotar a los 4 esbirros* disponible).
6. El historial (pila) y los eventos (cola) del Checkpoint 2 siguen funcionando: moverse registra la acción y dispara el siguiente evento, y el evento de cofre inserta un objeto en el diccionario.

### Decisión: ¿qué pasa con el estado del mundo al deshacer?

* Deshacer un **movimiento** devuelve al jugador a la sala anterior. Las visitas ya registradas se conservan.
* Deshacer un **recoger** quita el objeto del inventario y lo **vuelve a poner en la sala** en el diccionario.
* El **progreso del mundo es permanente**: las misiones completadas, los puntos y los desbloqueos **no se deshacen**. Igual que en el Checkpoint 2, el tiempo del bosque sigue corriendo aunque el gato retroceda: lo que ya ocurrió no se borra, solo cambian la posición y el inventario.

### Dibujos(Grafo del mapa)

<img width="802" height="377" alt="Mapitagrafo drawio" src="https://github.com/user-attachments/assets/24005eae-60a7-414d-9ef2-02377e8567e6" />

```text
Claro Encantado: Sendero de Hongos, Árbol Hueco
Sendero de Hongos: Claro Encantado, Arroyo de Luciérnagas, Cueva del Murciélago
Arroyo de Luciérnagas: Sendero de Hongos, Guarida del Fantasma
Cueva del Murciélago: Sendero de Hongos, Colina de la Luna
Árbol Hueco: Claro Encantado, Colina de la Luna, Guarida del Fantasma
Colina de la Luna: Árbol Hueco, Cueva del Murciélago
Guarida del Fantasma: Árbol Hueco, Arroyo de Luciérnagas
```
### Evidencia de ejecución 

```text
AVENTURA EN EL BOSQUE ENCANTADO
¡Misión completada: Despertar en el Claro Encantado!
Mazmorra generada: 7 salas, profundidad 2
Opción: 7
¿A qué sala quieres ir? 7
Ruta (3 saltos): Claro Encantado -> Sendero de Hongos -> Arroyo de Luciernagas -> Guarida del Fantasma
Opción: 8
Alcanzables desde Claro Encantado: Claro Encantado, Sendero de Hongos, Arroyo de Luciernagas, Guarida del Fantasma, Cueva del Murcielago, Colina de la Luna
Aisladas o bloqueadas: Arbol Hueco
Opción: 1
Salas conectadas: 1) Sendero de Hongos  2) Arbol Hueco [bloqueada: un árbol caído tapa el camino]
Elige una sala: 2
No puedes pasar: un árbol caído tapa el camino.
Opción: 1
Salas conectadas: 1) Sendero de Hongos  2) Arbol Hueco [bloqueada: un árbol caído tapa el camino]
Elige una sala: 1
Te mueves a: Sendero de Hongos
¡Misión completada: Cruzar el Sendero de Hongos!
Opción: 1
Elige una sala: 2
Te mueves a: Arroyo de Luciernagas
Opción: 6
Obtuviste 'Bomba de Catnip'!
¡Misión completada: Recoger la Bomba de Catnip!
¡Se desbloquea: Arbol Hueco!
Opción: 10
=== ÁRBOL DE MISIONES ===
[x] Despertar en el Claro Encantado
    [x] Cruzar el Sendero de Hongos
        [x] Recoger la Bomba de Catnip
        [ ] Derrotar al Murciélago Fantasma
    [ ] Explorar el Árbol Hueco
        [ ] Conseguir el Ovillo de Lana
        [ ] Llegar a la Guarida del Fantasma
            [ ] Derrotar a los 4 esbirros
                [ ] Tomar la llave y escapar
Puntos ganados: 30
Opción: 9
Puntos: 30
Opción: 3
Deshaciendo: Recogiste 'Bomba de Catnip' en Arroyo de Luciernagas
Soltaste 'Bomba de Catnip'
Opción: 9
Puntos: 30
Opción: abc
Opcion no valida. Elige un numero del 1 al 12.
Opción: 0
Opcion no valida. Elige un numero del 1 al 12.
Opción: -3
Opcion no valida. Elige un numero del 1 al 12.
Opción: 99
Opcion no valida. Elige un numero del 1 al 12.
Opción: 3
Deshaciendo: Te moviste de Sendero de Hongos a Arroyo de Luciernagas
Vuelves a: Sendero de Hongos
Opción: 3
Deshaciendo: Te moviste de Claro Encantado a Sendero de Hongos
Vuelves a: Claro Encantado
Opción: 3
No hay nada que deshacer: el historial está vacío.
Opción: 11
El fantasma solo aparece en las salas más profundas del bosque.
Opción: 1
Elige una sala: 1
Te mueves a: Sendero de Hongos
Opción: 1
Elige una sala: 2
Te mueves a: Arroyo de Luciernagas
Opción: 1
Elige una sala: 2
Te mueves a: Guarida del Fantasma
Opción: 11
Todavía no puedes enfrentar al fantasma: te faltan misiones por completar (explora el Árbol Hueco).
Opción: 1
Elige una sala: 1
Te mueves a: Arbol Hueco
¡Misión completada: Explorar el Árbol Hueco!
¡Misión completada: Llegar a la Guarida del Fantasma!
Opción: 1
Elige una sala: 3
Te mueves a: Guarida del Fantasma
Opción: 11
INICIO DE COMBATE EN EL BOSQUE
¡Combate contra enemigo 1!
Usaste 'Varita Mágica de Plumas'
Enemigo 1 derrotado. Total derrotados: 1
[...]
¡Combate contra enemigo 4!
Usaste 'Varita Mágica de Plumas'
Enemigo 4 derrotado. Total derrotados: 4
El enemigo 4 suelta la llave, ¡es tu oportunidad!
Obtuviste 'Llave de salida'!
Tus juguetes
- Varita Mágica de Plumas
- Llave de salida
Encuentras la salida del bosque encantado. ¡Usa la llave para escapar!
Usaste 'Llave de salida'
¡Venciste al fantasma!
¡Misión completada: Derrotar a los 4 esbirros!
¡Misión completada: Tomar la llave y escapar!
```