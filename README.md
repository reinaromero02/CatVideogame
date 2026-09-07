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
```
<img width="577" height="1107" alt="juegogato drawio" src="https://github.com/user-attachments/assets/786eab2d-8aea-4d71-9ec4-7c6fd5df404f" />

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
