# VIDEOJUEGO - PLANTAS VS ZOMBIES
Este repositorio contiene todos los archivos necesarios para ejecutar el videojuego, desde estructuras de código hasta soundtrack e imágenes.
Link al video de youtube demostrarivo del juego: 
# https://youtu.be/T4LyruFEoHY
## Archivo principal
- `main_final`: Contiene el código de ejecución principal del videojuego.
## Archivo de funciones 
- `Funciones_dibujos_final`: Contiene todas las funciones a utilizar en el código principal.
## Archivos de clases
- `clases_zombies_final`: Contiene todas las clases relacionadas a la creación y manejo de los zombies.
- `clases_plantas_final`: Contiene todas las clases relacionadas a la creacion y manejo de las plantas.
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
# *funciones_dibujos_final* 
Contiene funciones y variables relacionadas con la interfaz gráfica de un juego. Su uso principal es para manejar la visualización de elementos como: la grilla del jardín (dibuja el fondo con pasto y líneas de división, la barra lateral izquierda (contiene botones para seleccionar plantas/herramientas y muestra el contador de soles (moneda del juego), botones interactivos para plantas específicas y herramientas. Además, proporciona funciones auxiliares para crear y posicionar estos botones en la barra lateral.
# *clase_zombies_final*
Crea los zombies y hereda la clase NPC. Contiene los comportamientos de los zombies como velocidad, daño de ataque, vida. Las funciones de esta clase se encargan de ir actualizando los valores de estas variables. Tiene clases hijas donde varía su salud e imagen según el tipo de zombie.
# *clases_plantas_final*
Contiene los elementos del juego con los que interactúa el usuario. Entre estos los soles que se recolectan (generados por girasol o que caen del cielo), las podadoras defensivas, distintos tipos de plantas como los girasoles que generan soles, nueces que sirven como defensoras, lanzaguisantes normal, lanzaguisantes de hielo (ralentiza a los zombies) y los proyectiles que dañan a los zombies. Además contiene los botones interactivos para seleccionar las plantas y la herramienta como la pala para eliminarlas. 
