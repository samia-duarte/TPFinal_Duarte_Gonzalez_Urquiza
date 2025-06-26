import time
import pygame as pg
import random
from clases_plantas import NPC
# --- CONSTANTES DE COLORES ---
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
DARK_GRAY = (64, 64, 64)
BLUE_TINT = (183, 232, 245, 100)
# --- ZOMBI CLASE BASE ---s
class Zombie(NPC):
    '''Clase base para todos los tipos de zombies.
    Hereda la clase NPC y añade comportamientos especificos a cada zombie.
    Atributos:
        dano_ataque_base(int): 
    '''
    dano_ataque_base = 1         
    velocidad_ataque_base = 1 
    def __init__(self, fila: int, salud_inicial: int, imagen_surf: pg.surface, c_size: int, margen_x: int, ancho_grilla: int):
        '''Inicializa nuevo zombie.
         Args:
            fila (int): fila del jardín donde aparecerá (de la 0 a la 4).
            salud_inicial (int): puntos de salud iniciales.
            imagen_surf (pygame.Surface): imagen del zombie.
            c_size (int): tamaño de celda en píxeles.
            margen_x (int): margen horizontal del área de juego.
            ancho_grilla (int): ancho total del área de juego.
        '''
        posi_x = margen_x + ancho_grilla - c_size 
        posi_y = fila * c_size + c_size
        ancho = c_size                
        alto = c_size
        super().__init__(
            posi_x, posi_y,
            ancho, alto, 
            imagen_surf
            )
        
        self.y = float(posi_y)
        self.x = float(posi_x) 
        self.rect.x = int(self.x) 
        self.fila = fila
        self.hp = salud_inicial
        self.velocidad_caminando_base = 0.5
        self.max_hp = salud_inicial
        
        #-----COMPORTAMINETO ZOMBIES------
        self.velocidad_actual = self.velocidad_caminando_base
        self.dano_ataque = self.dano_ataque_base
        self.velocidad_ataque = self.velocidad_ataque_base
        self.velocidad_ataque_base = self.velocidad_ataque
        self.esta_slowmow = False
        self.tiempo_fin_slowmow = 0
        self.factor_slowmow_velocidad = 0.5
        self.factor_slowmow_ataque = 2.0

        self.ultimo_ataque = time.time()
        self.atacando = False 
        self.target_planta = None 
        self.margen_x = margen_x

    def aplicar_slowmow(self, tiempo_actual: float, duracion: float = 3.0):
        '''Aplica efecto de ralentización al zombie.
        Argumentos:
                tiempo_actual(float): marca el tiempo en el que comienza el efecto
                duracion (float): duración del efecto en segundos.'''
        if not self.esta_slowmow:
            self.velocidad_actual *= self.factor_slowmow_velocidad
            self.velocidad_ataque *= self.factor_slowmow_ataque
            self.esta_slowmow = True
        self.tiempo_fin_slowmow = tiempo_actual + duracion

    def off_slowmow(self):
        '''Termina el efecto de ralentización del zombie.'''
        if self.esta_slowmow:
            self.velocidad_actual = self.velocidad_caminando_base
            self.velocidad_ataque = self.velocidad_ataque_base
            self.esta_slowmow = False
            self.tiempo_fin_slowmow = 0 

    def actualizar(self, plantas: list, dt: float):
        '''Actualiza el estado del zombie cada frame
        Argumentos:
                plantas (list): lista de plantas en el juego.
                dt (float): delta time desde el último frame.
        Returns:
            str/None: 'gameOver' si llegó a la casa, None o planta destruida.
        '''
        planta_destruida = None
        self.atacando = False
        if self.esta_slowmow and time.time() >= self.tiempo_fin_slowmow:
                self.off_slowmow()
        if self.target_planta and self.target_planta.hp > 0 and self.rect.colliderect(self.target_planta.rect):
            self.atacando = True
            if time.time() - self.ultimo_ataque > self.velocidad_ataque:
                if self.target_planta.recibir_dmg(self.dano_ataque):
                    planta_destruida = self.target_planta
                    self.target_planta = None
                self.ultimo_ataque = time.time()
        else:
            self.target_planta = None
            for planta in plantas:
                if planta.fila == self.fila and self.rect.colliderect(planta.rect):
                    self.target_planta = planta
                    self.atacando = True
                    break

        if not self.atacando:
            self.x -= self.velocidad_actual * dt * 60
            self.rect.x = int(self.x)

        if self.rect.right <= self.margen_x + 10:
            return 'gameOver'
        
        return planta_destruida

    def recibir_dano(self, cantidad:int) -> bool:
        '''Reduce cantidad de salud del zombie cuando recibe daño.
        Argumentos:
                cantidad (int): cantidad de daño que le va a hacer la planta.
        Returns:
                bool: True si el zombie murió, False si sigue vivo.
        '''
        self.hp -= cantidad
        if self.hp <= 0:
            return True
        return False
    
    def dibujar(self, screen: pg.Surface):
        '''Dibuja el zombie en la pantalla con efecto de congelamiento
        Argumentos:
                screen(pg.Surface): superficie donde se dibujará.
        '''
        screen.blit(self.image, self.rect)
        if self.esta_slowmow:
            blue_overlay = pg.Surface(self.rect.size, pg.SRCALPHA) 
            blue_overlay.fill(BLUE_TINT) 
            screen.blit(blue_overlay, self.rect)
        
# --- ZOMBIS ESPECÍFICOS ---

class ZombieNormal(Zombie):
    '''Es el zombie básico, no tiene ninguna protección.'''
    velocidad_caminando_base = 0.01
    dano_ataque_base = 5
    salud_inicial = 20

    def __init__(self, fila: int, imagen_surf: pg.surface, c_size: int, margen_x: int, ancho_grilla: int):
        super().__init__(
            fila, 
            ZombieNormal.salud_inicial, imagen_surf, 
            c_size, margen_x, ancho_grilla)
        self.velocidad_actual = self.velocidad_caminando_base 

class ZombieConCono(Zombie):
    '''Zombie que tiene un cono de protección, aumenta su resistencia'''
    velocidad_caminando_base = 0.01
    dano_ataque_base = 5
    salud_inicial = 40

    def __init__(self, fila: int, imagen_surf: pg.surface, c_size: int, margen_x: int, ancho_grilla: int):
        super().__init__(fila, ZombieConCono.salud_inicial, imagen_surf, c_size, margen_x, ancho_grilla)
        self.velocidad_actual = self.velocidad_caminando_base


class ZombieConBalde(Zombie):
    '''Zombie con balde de metal de protección, es más resistente que los otros.'''
    velocidad_caminando_base = 0.01
    dano_ataque_base = 5
    salud_inicial = 60

    def __init__(self, fila: int, imagen_surf: pg.surface, c_size: int, margen_x: int, ancho_grilla: int):
        super().__init__(fila, ZombieConBalde.salud_inicial, imagen_surf, c_size, margen_x, ancho_grilla)
        self.velocidad_actual = self.velocidad_caminando_base
print('Clases de Zombis cargadas con Éxito!')