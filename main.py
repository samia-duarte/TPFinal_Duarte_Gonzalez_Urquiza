import time
import random
import pygame as pg
import os
from clases_plantas import Sol, NPC, Planta, Girasol, Nuez, BotonPlanta, Guisante, LanzaGuisantes, LanzaGuisantesFrio
from funciones_dibujos import dibujar_fondo_grilla, dibujar_soles_hud, dibujar_barra_lateral, botones_plantas_armado
from clase_zombies import ZombieNormal, ZombieConCono, ZombieConBalde

pg.init()
pg.mixer.init()
try:
    #=======Implementación de imaes=======

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
    w, h = ima_patio.get_size()
    ima_game_over = pg.image.load(os.path.join('assets', 'imagenes', 'game_over.jpg'))
    ima_game_over = pg.transform.scale(pg.image.load(os.path.join('assets', 'imagenes', 'game_over.jpg')), (w,h))
    sonido_game_over = pg.mixer.Sound(os.path.join('assets', 'soundtrack', 'sonido_game_over.mp3'))
    
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

# Configuración de oleadas
WAVE_DATA = [
    # (inicio_seg, duracion_seg, [tipos_zombie], spawn_min, spawn_max)
    (5,   30,   [ZombieNormal],          5,  8),   # Oleada 1
    (0,   40,   [ZombieNormal, ZombieConCono], 8,  12),  # Oleada 2 (inicio=0 porque se activa al terminar la anterior)
    (0,   60,   [ZombieNormal, ZombieConCono, ZombieConBalde], 12, 15), # Oleada 3
]

class Oleadas:
    def __init__(self, wave_data):
        self.wave_data = wave_data #configuracion de las oleadas
        self.oleada_actual = -1 #indica la oleada actual (-1 es que no comenzó ninguna)
        self.tiempo_inicio_oleada = 0 #tiempo que comenzó la oleada actual
        self.zombies_por_generar = 0 
        self.zombies_generados = 0 
        self.tipos_zombies_actuales = [] 
        self.tiempo_ultimo_spawn = 0 
        self.intervalo_spawn = 20  # segundos entre zombies
        self.oleada_activa = False #si hay una oleada activa
        self.tiempo_inicio_juego = time.time() #sirve para calcular segs desde la primera oleada
        
    def actualizar(self, zombis_activos, c_size, margen_x, ancho_grilla, ima_zombie_n=None):
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio_juego
        
        # inicia primera oleada si es tiempo y no hay oleada activa
        if self.oleada_actual == -1 and tiempo_transcurrido >= self.wave_data[0][0]:
            self.iniciar_siguiente_oleada()
        
        # si hay una oleada de zombies en curso y todavía no salieron todos los zombies que deberían
        if self.oleada_activa and self.zombies_generados < self.zombies_por_generar: 
            if tiempo_actual - self.tiempo_ultimo_spawn > self.intervalo_spawn:
                self.generar_zombie(zombis_activos, c_size, margen_x, ancho_grilla, ima_zombie_n)
                self.tiempo_ultimo_spawn = tiempo_actual
                self.zombies_generados += 1 #incrementa contador de zombies generadors
        
        # Verificar si debemos pasar a la siguiente oleada
        if (self.oleada_activa and self.zombies_generados >= self.zombies_por_generar and 
            len(zombis_activos) == 0 and 
            self.oleada_actual + 1 < len(self.wave_data)):
            self.iniciar_siguiente_oleada()
    
    #esto basicamente reinicia todo para que comience la siguiente oleada
    def iniciar_siguiente_oleada(self):
        #incremento del indice de oleada
        self.oleada_actual += 1
        #obtener datos de oleada actual ignorando duración pq se mantiene igual
        _, _, tipos, min_z, max_z = self.wave_data[self.oleada_actual]
        self.tipos_zombies_actuales = tipos
        self.zombies_por_generar = random.randint(min_z, max_z) #para que sea random la cant d zombies que se generen
        self.zombies_generados = 0 #reinicio del contador d zombies generados
        self.tiempo_ultimo_spawn = time.time() #ahora el tiempo desde el ult spawn es el tiempo actual
        self.oleada_activa = True 
        print(f"¡OLEADA {self.oleada_actual+1} INICIADA!")
            
    def generar_zombie(self, zombis_activos, c_size, margen_x, ancho_grilla, imagen_zombie=None):
        fila = random.randint(0, 4)
        TipoZombie = random.choice(self.tipos_zombies_actuales)
        
        # Selecciona la imagen según el tipo de zombie
        if TipoZombie == ZombieConCono:
            imagen = ima_zombie_cono
        elif TipoZombie == ZombieConBalde:
            imagen = ima_zombie_balde
        else:  # ZombieNormal
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

filas_destruidas = []

game_over = False
tiempo_game_over = 0
soles_actuales = 100 #vamos a empezar con 100 para poder trabajar, dps empieza en 0
sol_rate = 8
ultimo_sol_caido_global = time.time()


#=======SOPORTE TECNICO DEL JUEGO=======
#----SCREEN SIZE----
screen = pg.display.set_mode((w, h))
pg.display.set_caption('PVZ')
#----STATS GRILLA----
fil = 5
col = 10
c_size = 84 # El tamaño de celda que mejor funcionó
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
zombis_activos = [] # Lista vacía para zombis
grilla_ocupada = [[None for _ in range(col)] for _ in range(fil)]
#----SELECCION DE PLANTAS (valores in)----
planta_seleccionada = None # Almacena la CLASE de la planta seleccionada (ej. Girasol)
planta_costo_seleccionada = 0
imagen_seleccionada_para_colocar = None
#----VALORES TECNICOS----
FPS = 60
clock = pg.time.Clock()
test_font = pg.font.Font(None, 40)
#----SOUNDTRACK----
musica_fondo = pg.mixer.music.load(os.path.join('assets', 'soundtrack', 'plants-vs-zombies-soundtrack-day-stage.mp3'))
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.8)
#===INICIALIZACION COSAS JUEGO===
# --- Inicialización de los botones de planta ---
botones = 90
botones_plantas = []
y_actual_boton = botones
y_actual_boton = botones_plantas_armado(botones_plantas, y_actual_boton, Girasol, ima_girasol_boton, ima_girasol_plant)
y_actual_boton = botones_plantas_armado(botones_plantas, y_actual_boton, Nuez, ima_papa_boton, ima_papa_plant)
# Agregar después de los otros botones
y_actual_boton = botones_plantas_armado(botones_plantas, y_actual_boton, LanzaGuisantes, ima_pee_boton, ima_pee_plant)
y_actual_boton = botones_plantas_armado(botones_plantas, y_actual_boton, LanzaGuisantesFrio, ima_pee_frio_boton, ima_pee_frio_plant)
wave_manager = Oleadas(WAVE_DATA)
zombis_activos = [] 
#----GAME LOOP----
running = True
plant_ima_map = {
    Girasol: ima_girasol_plant,
    Nuez: ima_papa_plant,
    LanzaGuisantes: ima_pee_plant,
    LanzaGuisantesFrio: ima_pee_frio_plant
}
while running:
    tiempo_atm = time.time()
    dt = clock.tick(FPS) / 1000.0 

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if planta_seleccionada != None and event.key == pg.K_ESCAPE:
                planta_seleccionada = None
                planta_costo_seleccionada = 0
                imagen_seleccionada_para_colocar = None
            elif event.key == pg.K_q or event.key == pg.K_ESCAPE:
                running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
#---------SELECCION PLANTAS---------
            clic_en_boton = False
            for boton in botones_plantas:
                if boton.clic_en(event.pos): #.clic_en es nuestra funcion
                    clic_en_boton = True         
                    if soles_actuales >= boton.costo:
                        planta_seleccionada = boton.tipo_planta
                        planta_costo_seleccionada = boton.costo
                        print(f"Planta seleccionada: {planta_seleccionada.__name__} (Costo: {planta_costo_seleccionada})")
                        imagen_seleccionada_para_colocar = boton.imagen_planta_completa
                    else:
                        print("¡No tienes suficientes soles para esta planta!")
                    #'''
                    break

            if not clic_en_boton:
                sol_recolectado = False
                for sol in list(soles_cayendo):
                    if sol.clic_en(event.pos):
                        soles_actuales += sol.valor
                        soles_cayendo.remove(sol)
                        sol_recolectado = True
                        break
                if not sol_recolectado:
                    if planta_seleccionada and margen_x <= mouse_x < (margen_x + ancho_grilla) and margen_y <= mouse_y < (margen_y + alto_grilla):
                    #Que no se va de la grilla 
                        celda_col = int((mouse_x - margen_x) // c_size)
                        celda_fila = int((mouse_y - margen_y) // c_size)
                        if grilla_ocupada[celda_fila][celda_col] is None:
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
                                    print("¡No tienes suficientes soles para colocar esta planta!") #lo mismo con estas, hay que mostrar en pantalla unos segundos
                        else:
                            print("¡Esta celda ya está ocupada!")
                    elif planta_seleccionada: # Si hay una planta seleccionada pero se hizo clic fuera de la grilla
                        print("Haz clic en una celda válida de la grilla para colocar la planta.")
#---------SELECCION SOLES---------
    # Generación GLOBAL de soles (caen del cielo)
    if tiempo_atm - ultimo_sol_caido_global > sol_rate:
        rand_col_idx = random.randint(0, col - 1) #x random pero siempre arriba
        sol_x = margen_x + rand_col_idx * c_size + (c_size // 2) - (c_size // 4) # c_size//4 para centrar en casilla
        sol_y_inicio = -50 # encima pantalla
        soles_cayendo.append(Sol(sol_x, sol_y_inicio, c_size, margen_y, h, ima_sol))
        ultimo_sol_caido_global = tiempo_atm

    # Actualizar y eliminar soles
    soles_a_eliminar = []
    for sol in soles_cayendo:
        if sol.actualizar(): # Si sol.actualizar() devuelve True, significa que debe ser eliminado
            soles_a_eliminar.append(sol)
    for sol in soles_a_eliminar:
        soles_cayendo.remove(sol)
    for planta in plantas_en_juego:
        if isinstance(planta, Girasol):
            planta.actualizar(soles_cayendo, c_size, margen_y, h, ima_sol)
        elif isinstance(planta, (LanzaGuisantes, LanzaGuisantesFrio)):
            ima_guisante_a_usar = ima_guisante_frio if isinstance(planta, LanzaGuisantesFrio) else ima_guisante
            planta.actualizar(zombis_activos, proyectiles_activos, dt, ima_guisante_a_usar)
   
    wave_manager.actualizar(zombis_activos, c_size, margen_x, ancho_grilla, ima_zombie_n)

    zombies_a_eliminar = [] 

    for i, zombie in enumerate(zombis_activos):
        resultado = zombie.actualizar(plantas_en_juego, dt) # =gameover, planta si destruyó una y None si sigue vivo
        
        if resultado == 'gameOver':
            fila_destruida = zombie.fila in filas_destruidas
            
            if not fila_destruida: #si la fila no estaba marcada como destruida antes
                filas_destruidas.append(zombie.fila) #para detectar game over en otros zombies
                # añade todos los zombies de la misma fila
                zombies_a_eliminar = []
                for i, z in enumerate(zombis_activos):
                    if z.fila == zombie.fila: #filtra los zombies que están en la misma fila que el que activó el gameover
                        zombies_a_eliminar.append(i) #crea lista con indices i de esos zombies
            else:
                print("¡GAME OVER! Te llegó otro zombie en la misma fila.")
                game_over = True
                tiempo_game_over = time.time()
                pg.mixer.music.stop()
                sonido_game_over.play()

                screen.blit(ima_game_over,(0,0))
                pg.display.update()

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



        elif resultado:  # si el zombie destruyó una planta
            plantas_en_juego.remove(resultado) 
            grilla_ocupada[resultado.fila][resultado.col] = None #libera espacio para nuevas plantas
        #es una matriz (list de l) que representa jardín. cada celda puede estar ocupada por una planta:
        #ej: grilla_ocup[1][2] = objeto_planta, vacía(None)

        # zombies muertos por daño
        if zombie.hp <= 0:
            zombies_a_eliminar.append(i)

    # elimina zombies muertos (deja los indices mas altos 1ro para evitar errores)
    for i in sorted(zombies_a_eliminar, reverse=True):
        if i < len(zombis_activos): 
            zombis_activos.pop(i)
    """
    proyectiles_a_eliminar = []
    for i, proyectil in enumerate(proyectiles_activos):
        proyectil.actualizar(dt)
    """
    #------------------------AGREGO LEON LA PARTE DE LOS LANZA GUISANTES-------------------------------
    pee_a_eliminar = []
    for i, proyectil in enumerate(proyectiles_activos):
        proyectil.actualizar(dt) #mueve ->
        zombie_golpeado = None
        for zombie in zombis_activos:
            if proyectil.fila == zombie.fila and proyectil.rect.colliderect(zombie.rect) and zombie.hp > 0 and i not in pee_a_eliminar:
            #coliusiona si misma fila y zombie vivo y si todavia no le pego (si le pego se va)
                zombie_golpeado = zombie
                break #E FIN (para no wombocombo)
        if zombie_golpeado:
            zombie_golpeado.hp -= proyectil.daño
            print(f'DEBUGG: Pee golpeo a zombie en fila {zombie_golpeado.fila}. HP Zombie: {zombie_golpeado.hp}')
            if proyectil.es_congelante:
                zombie_golpeado.aplicar_slowmow(tiempo_atm)
            pee_a_eliminar.append(i)
        if proyectil.rect.x > w:
            pee_a_eliminar.append(i)
    #-------------------------------------------------------------------------------------------------------   
        for i in sorted(list(set(pee_a_eliminar)), reverse=True):
            if i < len(proyectiles_activos):
                proyectiles_activos.pop(i)
        wave_manager.actualizar(zombis_activos, c_size, margen_x, ancho_grilla, ima_zombie_n)
        # verifica la colisión con los zombies
        for zombie in zombis_activos:
            if zombie.rect.colliderect(proyectil.rect):
                if zombie.recibir_dano(proyectil.daño):
                    if proyectil.es_congelante:
                        zombie.aplicar_slowmow(time.time())  # activa slowmow
                break
#---------SCREEN---------
    screen.blit(ima_patio, (0,0)) # Usar la imagen de patio cargada
    dibujar_fondo_grilla(ancho_grilla, alto_grilla, col, fil, c_size, screen, margen_x, margen_y, ima_pasto) # Dibujar la grilla del pasto

    for planta in plantas_en_juego:
        planta.dibujar(screen)

    for sol in soles_cayendo:
        sol.dibujar(screen)

    for proyectil in proyectiles_activos:
        proyectil.dibujar(screen)

    dibujar_barra_lateral(botones_plantas, soles_actuales, screen, planta_seleccionada, test_font) # Dibujar la barra lateral y los botones

    for zombie in zombis_activos:
        zombie.actualizar(plantas_en_juego, dt)  # Actualiza el comportamiento
        zombie.dibujar(screen)
    
    if planta_seleccionada:
        mouse_pos = pg.mouse.get_pos()
        fantasma_img = plant_ima_map.get(planta_seleccionada)
        if fantasma_img:
            fantasma = pg.transform.scale(fantasma_img, (c_size, c_size))
            fantasma.set_alpha(100)
            screen.blit(fantasma, mouse_pos)

    pg.display.update()
    clock.tick(FPS)

pg.quit()
print('Se cerró pygame exitosamente')