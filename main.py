import time
import random
import pygame as pg
import os

# Importaciones de clases
from clases_plantas import Sol, NPC, Planta, Girasol, Nuez, BotonPlanta, Guisante, LanzaGuisantes, LanzaGuisantesFrio
from funciones_dibujos import dibujar_fondo_grilla, dibujar_soles_hud, dibujar_barra_lateral, botones_plantas_armado
from clase_zombies import ZombieNormal, ZombieConCono, ZombieConBalde

# Inicializar pygame
pg.init()
pg.mixer.init()

# Manejo de errores try-except
try:
    #=======Implementación de imágenes=======
    #----PLANTAS----
    ima_papa_plant = pg.image.load(os.path.join('assets', 'imagenes', 'papa.png'))
    ima_girasol_plant = pg.image.load(os.path.join('assets', 'imagenes', 'girasol.png')) 
    ima_pee_plant = pg.image.load(os.path.join('assets', 'imagenes', 'lanzaguizantes.png'))
    ima_pee_plant = pg.image.load(os.path.join('assets', 'imagenes', 'lanzaguizantes.png'))
    ima_pee_frio_plant = pg.image.load(os.path.join('assets', 'imagenes', 'lanzaguizantes_hielo.png'))
    ima_guisante = pg.image.load(os.path.join('assets', 'imagenes', 'guisante.png'))
    ima_guisante_frio = pg.image.load(os.path.join('assets', 'imagenes', 'guisante_hielo.png'))

    #----ZOMBIES----
    ima_zombie_n = pg.image.load(os.path.join('assets', 'imagenes', 'zombie_sf_n.png'))
    ima_zombie_cono = pg.image.load(os.path.join('assets', 'imagenes', 'zombie_cono.png'))
    ima_zombie_balde = pg.image.load(os.path.join('assets', 'imagenes', 'zombie_balde.png'))

    #----PLANTAS_BOTONOES----
    ima_papa_boton = pg.image.load(os.path.join('assets', 'imagenes', 'papa.png'))
    ima_girasol_boton = pg.image.load(os.path.join('assets', 'imagenes', 'girasol.png'))
    ima_pee_boton = pg.image.load(os.path.join('assets', 'imagenes', 'lanzaguizantes.png'))
    ima_pee_frio_boton = pg.image.load(os.path.join('assets', 'imagenes', 'lanzaguizantes_hielo.png'))

    #----OBJETOS----
    ima_patio = pg.image.load(os.path.join('assets', 'imagenes', 'patio_definitivo2.png'))
    ima_pasto = pg.image.load(os.path.join('assets', 'imagenes', 'pasto.png'))
    ima_sol = pg.image.load(os.path.join('assets', 'imagenes', 'sol.png'))

    #----GAME-OVER----
    ima_game_over = pg.image.load(os.path.join('assets', 'imagenes', 'game_over.jpg'))
    w, h = ima_patio.get_size()
    ima_game_over = pg.transform.scale(pg.image.load(os.path.join('assets', 'imagenes', 'game_over.jpg')), (w,h))
    
    print('The bluetooth device is connected as succesfully')
except pg.error as e: 
    print(f'Error Pygame cargando la ima!: {e}')
    print('cuak')
    pg.quit()
    exit()
except FileNotFoundError as e:
    print(f'No se encontro el archivo, error: {e}')
    pg.quit()
    exit()

# ==== Configuración de oleadas ====
WAVE_DATA = [
    # (inicio_seg, duracion_seg, [tipos_zombie], spawn_min, spawn_max)
    (5,   30,   [ZombieNormal],          5,  8),   # Oleada 1
    (0,   40,   [ZombieNormal, ZombieConCono], 8,  12),  # Oleada 2
    (0,   60,   [ZombieNormal, ZombieConCono, ZombieConBalde], 12, 15), # Oleada 3
]

class Oleadas:
    ''' Controla la generación de oleadas de zombies.
    Atributos: 
        wave_data (list): configuración de las oleadas
        oleada_actual (int): índice de oleada actual (-1 si no se inició)
        zombies_por_generar (int): cantidad de zombies restantes en la oleada
    '''
    def __init__(self, wave_data:list):
        ''' Argumentos:
                    wave_data (list): lista de tuplas con configuración de oleadas.
        '''
        self.wave_data = wave_data 
        self.oleada_actual = -1 
        self.tiempo_inicio_oleada = 0
        self.zombies_por_generar = 0 
        self.zombies_generados = 0 
        self.tipos_zombies_actuales = [] 
        self.tiempo_ultimo_spawn = 0 
        self.intervalo_spawn = 10  
        self.oleada_activa = False 
        self.tiempo_inicio_juego = time.time()
        
    def actualizar(self, zombis_activos: list, c_size: int, margen_x: float, ancho_grilla: float, ima_zombie_n: pg.Surface = None) -> None:
        '''Actualiza y genera zombies.
        Argumentos:
                zombis_activos (list): lista donde se añaden nuevos zombies.
                c_size (int): tamaño de celdas en pixeles.
                margen_x (float): margen horizontal de la grilla.
                ima_zombie_n (Surface): imagen para zombie normal.
        '''
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio_juego
        
        # Iniciar primera oleada cuando sea tiempo
        if self.oleada_actual == -1 and tiempo_transcurrido >= self.wave_data[0][0]:
            self.iniciar_siguiente_oleada()
        
        if self.oleada_activa and self.zombies_generados < self.zombies_por_generar: 
            if tiempo_actual - self.tiempo_ultimo_spawn > self.intervalo_spawn:
                self.generar_zombie(zombis_activos, c_size, margen_x, ancho_grilla, ima_zombie_n)
                self.tiempo_ultimo_spawn = tiempo_actual
                self.zombies_generados += 1 
        
        # Verificar si debemos pasar a la siguiente oleada
        if (self.oleada_activa and self.zombies_generados >= self.zombies_por_generar and 
            len(zombis_activos) == 0 and 
            self.oleada_actual + 1 < len(self.wave_data)):
            self.iniciar_siguiente_oleada()

    def iniciar_siguiente_oleada(self) -> None:
        '''Prepara parámetros para que inicie la siguiente oleada.
        Argumentos:
        '''
        self.oleada_actual += 1
        _, _, tipos, min_z, max_z = self.wave_data[self.oleada_actual]
        self.tipos_zombies_actuales = tipos
        self.zombies_por_generar = random.randint(min_z, max_z) 
        self.zombies_generados = 0
        self.tiempo_ultimo_spawn = time.time() 
        self.oleada_activa = True 
        print(f"¡OLEADA {self.oleada_actual+1} INICIADA!")
            
    def generar_zombie(self, zombis_activos: list, c_size: int, margen_x: float, ancho_grilla: float, imagen_zombie: pg.Surface = None) -> None:
        ''' Crea nuevo zombie en posición aleatoria. 
        Parámetros:
            zombis_activos (list): lista para agregar el nuevo zombie.
            c_size (int): tamaño de celda en píxeles.
            margen_x (float): margen horizontal del área de juego.
            ancho_grilla (float): ancho total del área de juego.
            imagen_zombie (pg.Surface): Imagen por defecto para zombies.
        '''
        fila = random.randint
        fila = random.randint(0, 4)
        TipoZombie = random.choice(self.tipos_zombies_actuales)
        
        if TipoZombie == ZombieConCono:
            imagen = ima_zombie_cono
        elif TipoZombie == ZombieConBalde:
            imagen = ima_zombie_balde
        else:  
            imagen = ima_zombie_n
        
        ima_escalada = pg.transform.scale(imagen, (c_size, c_size))

        nuevo_zombie = TipoZombie(
            fila=fila,
            imagen_surf=ima_escalada,
            c_size=c_size,
            margen_x=margen_x,
            ancho_grilla=ancho_grilla
        )
        zombis_activos.append(nuevo_zombie)

# === Variables globales ===

filas_destruidas = []
game_over = False
tiempo_game_over = 0
soles_actuales = 0
sol_rate = 8
ultimo_sol_caido_global = time.time()

#=======SOPORTE TECNICO DEL JUEGO=======

#---- CONFIGURACIÓN DE PANTALLA ----
w, h = ima_patio.get_size()
screen = pg.display.set_mode((w, h))
pg.display.set_caption('PVZ')

#---- CONFIGURACIÓN DE GRILLA ----
fil = 5
col = 10
c_size = 84 # Tamaño de celda
alto_grilla = fil * c_size 
ancho_grilla = col * c_size - 90

#----Margenes grilla y ajustes----
margen_x = ((w - ancho_grilla) / 2) + 40
margen_y = ((h - alto_grilla) / 2) - 7
ajuste_vertical = 0 
ajuste_horizontal = 55
margen_y += ajuste_vertical
margen_x += ajuste_horizontal
#///////////////////////////////////

#----Listas de Control----

plantas_en_juego = []
soles_cayendo = []
proyectiles_activos = []
zombis_activos = [] 
grilla_ocupada = [[None for _ in range(col)] for _ in range(fil)]

#----SELECCION DE PLANTAS (valores in)----
planta_seleccionada = None
planta_costo_seleccionada = 0
imagen_seleccionada_para_colocar = None

#----VALORES TECNICOS----
FPS = 60
clock = pg.time.Clock()
test_font = pg.font.Font(None, 40)

#----SOUNDTRACK----
musica_fondo = pg.mixer.music.load(os.path.join('assets', 'soundtrack', 'plants-vs-zombies-soundtrack-day-stage.mp3'))
sonido_game_over = pg.mixer.Sound(os.path.join('assets', 'soundtrack', 'sonido_game_over.mp3'))
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.8)

#===INICIALIZACION COSAS DEL JUEGO===

# --- Inicialización de los botones de planta ---
botones = 90
botones_plantas = []
y_actual_boton = botones

# Creación de botones para cada tipo de planta
y_actual_boton = botones_plantas_armado(botones_plantas, y_actual_boton, Girasol, ima_girasol_boton, ima_girasol_plant)
y_actual_boton = botones_plantas_armado(botones_plantas, y_actual_boton, Nuez, ima_papa_boton, ima_papa_plant)
y_actual_boton = botones_plantas_armado(botones_plantas, y_actual_boton, LanzaGuisantes, ima_pee_boton, ima_pee_plant)
y_actual_boton = botones_plantas_armado(botones_plantas, y_actual_boton, LanzaGuisantesFrio, ima_pee_frio_boton, ima_pee_frio_plant)

# === Inicialización del juego ===
wave_manager = Oleadas(WAVE_DATA)
wave_manager.tiempo_inicio_juego = time.time()

zombis_activos = [] 

# Mapeo de tipos de planta e imágenes
running = True
plant_ima_map = {
    Girasol: ima_girasol_plant,
    Nuez: ima_papa_plant,
    LanzaGuisantes: ima_pee_plant,
    LanzaGuisantesFrio: ima_pee_frio_plant
}

# === GAME LOOP ===

while running:
    ''' Bucle principal del juego, ejecuta 60 frames por segundo. 
    1. Manejo de eventos (input).
    2. Actualización de estado del juego.
    '''
    # --- Preaparación del frame ---
    tiempo_atm = time.time()
    dt = clock.tick(FPS) / 1000.0

    # --- Manejo de eventos ---
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            if planta_seleccionada != None and event.key == pg.K_ESCAPE:
                planta_seleccionada = None
                planta_costo_seleccionada = 0
                imagen_seleccionada_para_colocar = None
            
            # Tecla Q/ESC sale del juego
            elif event.key == pg.K_q or event.key == pg.K_ESCAPE:

                running = False
        # Evento clic para obtener posición del click
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

#---------SELECCIÓN PLANTAS---------
            clic_en_boton = False
            for boton in botones_plantas:
                if boton.clic_en(event.pos):
                    clic_en_boton = True         
                    if soles_actuales >= boton.costo: 
                        planta_seleccionada = boton.tipo_planta
                        planta_costo_seleccionada = boton.costo
                        print(f"Planta seleccionada: {planta_seleccionada.__name__} (Costo: {planta_costo_seleccionada})")
                        imagen_seleccionada_para_colocar = boton.imagen_planta_completa
                    else:
                        print("¡No tienes suficientes soles para esta planta!")
                    break

            # --- Si no fue click en boton, verifica otros elementos ---
            if not clic_en_boton:
                sol_recolectado = False

                # Clic en soles para recolectar
                for sol in list(soles_cayendo):
                    if sol.clic_en(event.pos):
                        soles_actuales += sol.valor
                        soles_cayendo.remove(sol)
                        sol_recolectado = True
                        break

                # Clic en grilla para colocar planta
                if not sol_recolectado:

                    # Verifica que el clic esté dentro del área del juego
                    if planta_seleccionada and margen_x <= mouse_x < (margen_x + ancho_grilla) and margen_y <= mouse_y < (margen_y + alto_grilla):
                        celda_col = int((mouse_x - margen_x) // c_size)
                        celda_fila = int((mouse_y - margen_y) // c_size)

                        if grilla_ocupada[celda_fila][celda_col] is None:
                                
                                # Crea la nueva planta según el tipo
                                if planta_seleccionada == Girasol:
                                    nueva_planta = planta_seleccionada(celda_fila, celda_col, imagen_seleccionada_para_colocar, c_size, margen_y, margen_x, h, ima_sol)
                                else: 
                                    nueva_planta = planta_seleccionada(celda_fila, celda_col, imagen_seleccionada_para_colocar, c_size, margen_y, margen_x)
                                if soles_actuales >= nueva_planta.costo:
                                    plantas_en_juego.append(nueva_planta) 
                                    grilla_ocupada[celda_fila][celda_col] = nueva_planta
                                    soles_actuales -= nueva_planta.costo

                                    planta_seleccionada = None
                                    planta_costo_seleccionada = 0
                                    imagen_seleccionada_para_colocar = None
                                else:
                                    print("¡No tienes suficientes soles para colocar esta planta!")
                        else:
                            print("¡Esta celda ya está ocupada!")
                    elif planta_seleccionada: 
                        print("Haz clic en una celda válida de la grilla para colocar la planta.")

#---------SELECCION SOLES---------
    # Generación GLOBAL de soles (caen del cielo)
    if tiempo_atm - ultimo_sol_caido_global > sol_rate:
        rand_col_idx = random.randint(0, col - 1)
        sol_x = margen_x + rand_col_idx * c_size + (c_size // 2) - (c_size // 4)
        sol_y_inicio = -50 
        soles_cayendo.append(Sol(sol_x, sol_y_inicio, c_size, margen_y, h, ima_sol))
        ultimo_sol_caido_global = tiempo_atm

    # --- ACTUALIZACIÓN DE ENTIDADES ---
    # Actualiza soles existentes
    soles_a_eliminar = []
    for sol in soles_cayendo:
        if sol.actualizar():
            soles_a_eliminar.append(sol)
    for sol in soles_a_eliminar:
        soles_cayendo.remove(sol)

    # Actualiza plantas
    for planta in plantas_en_juego:
        if isinstance(planta, Girasol):
            planta.actualizar(soles_cayendo, c_size, margen_y, h, ima_sol)
        elif isinstance(planta, (LanzaGuisantes, LanzaGuisantesFrio)):
            ima_guisante_a_usar = ima_guisante_frio if isinstance(planta, LanzaGuisantesFrio) else ima_guisante
            planta.actualizar(zombis_activos, proyectiles_activos, dt, ima_guisante_a_usar)
   
   # --- Gestión de oleadas y zombies ---
    wave_manager.actualizar(zombis_activos, c_size, margen_x, ancho_grilla, ima_zombie_n)

    # Actualiza zombies
    zombies_a_eliminar = [] 
    for i, zombie in enumerate(zombis_activos):
        resultado = zombie.actualizar(plantas_en_juego, dt)
        
        # 1. Zombie llegó a la casa (Game Over)
        if resultado == 'gameOver':
            fila_destruida = zombie.fila in filas_destruidas
            if not fila_destruida: 
                filas_destruidas.append(zombie.fila)
                # Añade todos los zombies de la misma fila
                zombies_a_eliminar = []
                for i, z in enumerate(zombis_activos):
                    if z.fila == zombie.fila: 
                        zombies_a_eliminar.append(i) 
            else:
                # Activa secuencia del Game Over
                print("¡GAME OVER! Te llegó otro zombie en la misma fila.")
                game_over = True
                tiempo_game_over = time.time()
                pg.mixer.music.stop()
                sonido_game_over.play()
                
                # Muestra pantalla de Game Over
                screen.blit(ima_game_over,(0,0))
                pg.display.update()

                # Espera 6 segundos antes de cerrar
                while time.time() - tiempo_game_over < 6:
                    for event in pg.event.get():
                        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                            running = False
                            game_over = False
                            break
                    if not running:
                        break
                    clock.tick(FPS)
                running = False

        # 2. Zombie destruyó una planta
        elif resultado:
            plantas_en_juego.remove(resultado) 
            grilla_ocupada[resultado.fila][resultado.col] = None

        # 3. Zombies muertos por daño
        if zombie.hp <= 0:
            zombies_a_eliminar.append(i)

    # Elimina zombies muertos 
    for i in sorted(zombies_a_eliminar, reverse=True):
        if i < len(zombis_activos): 
            zombis_activos.pop(i)
    
    # Actualiza proyectiles (guisantes)
    pee_a_eliminar = []
    for i, proyectil in enumerate(proyectiles_activos):
        proyectil.actualizar(dt) 
        zombie_golpeado = None
        for zombie in zombis_activos:
            if proyectil.fila == zombie.fila and proyectil.rect.colliderect(zombie.rect) and zombie.hp > 0 and i not in pee_a_eliminar:
                zombie_golpeado = zombie
                break 
        if zombie_golpeado:
            zombie_golpeado.hp -= proyectil.daño
            print(f'DEBUGG: Pee golpeo a zombie en fila {zombie_golpeado.fila}. HP Zombie: {zombie_golpeado.hp}')
            if proyectil.es_congelante:
                zombie_golpeado.aplicar_slowmow(tiempo_atm)
            pee_a_eliminar.append(i)

        # Elimina proyectiles que salen de la pantalla
        if proyectil.rect.x > (w + 50):
            pee_a_eliminar.append(i)

        # Elimina proyectiles marcados
        for i in sorted(list(set(pee_a_eliminar)), reverse=True):
            if i < len(proyectiles_activos):
                proyectiles_activos.pop(i)

        wave_manager.actualizar(zombis_activos, c_size, margen_x, ancho_grilla, ima_zombie_n)
        
        # Verifica la colisión con los zombies
        for zombie in zombis_activos:
            if zombie.rect.colliderect(proyectil.rect):
                if zombie.recibir_dano(proyectil.daño):
                    if proyectil.es_congelante:
                        zombie.aplicar_slowmow(time.time())
                break

#---------SCREEN---------
    
    # Capa 1: Fondo
    screen.blit(ima_patio, (0,0)) # Usar la imagen de patio cargada

    # Capa 2: Grilla del juego
    dibujar_fondo_grilla(ancho_grilla, alto_grilla, col, fil, c_size, screen, margen_x, margen_y, ima_pasto) # Dibujar la grilla del pasto

    # Capa 3: Plantas
    for planta in plantas_en_juego:
        planta.dibujar(screen)

    # Capa 4: Soles
    for sol in soles_cayendo:
        sol.dibujar(screen)

    # Capa 5: Proyectiles
    for proyectil in proyectiles_activos:
        proyectil.dibujar(screen)

    # Capa 6: Zombies
    for zombie in zombis_activos:
        zombie.actualizar(plantas_en_juego, dt) 
        zombie.dibujar(screen)

    # Capa 7: Barra lateral con botones de plantas
    dibujar_barra_lateral(botones_plantas, soles_actuales, screen, planta_seleccionada, test_font)
    
    # Capa 8: "Fantasma" de planta al arrancar.
    if planta_seleccionada:
        mouse_pos = pg.mouse.get_pos()
        fantasma_img = plant_ima_map.get(planta_seleccionada)
        if fantasma_img:
            fantasma = pg.transform.scale(fantasma_img, (c_size, c_size))
            fantasma.set_alpha(100)
            screen.blit(fantasma, mouse_pos)

    pg.display.update()
    
    # Control de velocidad, mantiene 60 FPS
    clock.tick(FPS)

pg.quit()
print('Se cerró pygame exitosamente')