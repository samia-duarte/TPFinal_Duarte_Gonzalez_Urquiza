# TPFinal_Duarte_Gonzalez_Urquiza
# https://youtu.be/T4LyruFEoHY

# VIDEOJUEGO - PLANTAS VS ZOMBIES
Este repositorio contiene todos los archivos necesarios para ejecutar el videojuego, desde estructuras de código hasta soundtrack e imágenes.

## Archivo principal
- `main_final`: Contiene el código de ejecución principal del videojuego.
## Archivo de funciones 
- `Funciones_dibujos_final`: Contiene todas las funciones a utilizar en el código principal.
## Archivos de clases
- `clases_zombies_final`: Contiene todas las clases relacionadas a la creación y manejo de los zombies.
- `clases_plantas_final`: Contiene todas las clases relacionadas a la creacion y manejo de las plantas.
  (Nota: en el programa se utiliza `clases_plantas` porque aunque sea el mismo archivo que `clases_plantas_final` por alguna razón no lo toma. Son identicos.)
## Carpeta - Assets
Contiene dos subcarpetas con todos los activos a utilizar:
- ### imagenes:
  Contiene todas las imágenes a utilizar en la visualización del videojuego:
  - `game_over🧠`: Imagen que sale al perder la partida.
  - `girasol🌻`: Imagen de girasol.
  - `gisante🟢`: Imagen de guisante común.
  - `gisante_hielo🔵`: Imagen de guisanted e hielo.
  - `lanzaguisantes🫛`: Imagen de lanzaguisantes común, (planta del juego).
  - `lanzaguisantes_hielo🧊`: Imagen de lanzaguizantes de hielo, (planta del juego).
  - `pala🌱`: Imagen de pala.
  - `papa🥔`: Imagen de una papa, (planta del juego)
  - `pasto🌿`: Imagen de cesped, grilla para objetos.
  - `patio_definitivo🖼️`: Imagen del fondo general.
  - `podadora✂️`: Imagen de podadora.
  - `sol☀️`: Imagen de sol.
  - `zombie_balde🧟‍♂️`: Imagen de zombie con balde en la cabeza, (zombie del juego).
  - `zombie_cono🧟‍♂️`: Imagen de zombie con cono en la cabeza, (zombie del juego).
  - `zombie_n🧟‍♂️`: Imagen de zombie común, (zombie del juego).
- ### soundtrack:
  Contiene todos los sonidos implementados en el videojuego:
  - `plants-vs-zombies-soundtrack-day-stage`: sonido de fondo.
  - `sonido_game_over`: sonido de partida perdida.
## Funcionalidades
Ejecuta videojuego principalmente a travéz de una programación orientada a objetos utiliazando biblioteca de pygame.
# *main* 
Ejecuta toda la lógica general del juego, además aplica manejo de errores y excepciones a archivos dentro de la carpeta assests. Lo que mas se destaca en este código es la implementación del bucle ya que utiliza manejo de eventos pygame que detecta los inputs que recibe del teclado y el click del mouse (salir del juego, plantar, sacar plantas, recolectar soles). Además realiza llamado de funciones y clases de archivos externos, generando actualización de assets y gestiona oleadas de zombies; el bucle rompe al salir de la ventana pygame o cuando llega un segundo zombie a la casa desde la misma fila de la grilla. 
Por último, se encuentra *wave_data*, clase que se encarga de la generación de oleadas de zombies.
# *Funciones_dibujos_final* 
Contiene funciones y variables relacionadas con la interfaz gráfica de un juego. Su uso principal es para manejar la visualización de elementos como: la grilla del jardín (dibuja el fondo con pasto y líneas de división, la barra lateral izquierda (contiene botones para seleccionar plantas/herramientas y muestra el contador de soles (moneda del juego), botones interactivos para plantas específicas y herramientas. Además, proporciona funciones auxiliares para crear y posicionar estos botones en la barra lateral.




