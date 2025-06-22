import time
import pygame as pg
import random
#Nota de León: Bienvenido a la sección de clases de plantas. Por ahora aca vamos a dejar solo a los NPC y plantas
#Los zombies ponganlos en otra carpeta
# --- CONSTANTES DE COLORES ---
AMARILLO = (255, 255, 0)
DARK_GREEN = (0, 100, 0)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE_OSCURO_SELECCION = (0,70,0,150)
#pg.init()
class Sol:
    def __init__(self, posi_x:int, posi_y:int, c_size:int, margen_y:int, h:int, imagen_surf:pg.surface=None, es_de_girasol=False, sol_val=25):
        self.rect = pg.Rect(posi_x, posi_y, c_size // 2, c_size // 2)
        self.valor = sol_val
        if imagen_surf:
            self.image = pg.transform.scale(imagen_surf,(c_size // 2, c_size // 2))
        else:
            self.image = pg.Surface((c_size // 2, c_size // 2))
            self.image.fill((255, 255, 0))
        self.velocidad_caida = random.randint(1, 2) #pq somos copados
        self.tiempo_creacion = time.time()
        self.vida_util = 8 #segundos antes que desaparezca
        self.es_de_girasol = es_de_girasol #para que no se interrumpan entre si los timings y distancias caida
        if es_de_girasol == True:
            self.destino_posi_y = posi_y + c_size // 2 # Aterrizan cerca de la base de la planta
            self.rect.y -= 20 #OJO! .y es donde esta, que es posi_y pero no lo es!!!
        else:
            self.destino_posi_y = random.randint(int(margen_y + c_size), int(margen_y + h - c_size // 2))
    def actualizar(self):
        """Hace que los soles caigan"""
        if self.rect.y < self.destino_posi_y:
            self.rect.y += self.velocidad_caida
            #mini check para que no se valla (._.''')
            if self.rect.y > self.destino_posi_y:
                self.rect.y = self.destino_posi_y
        if self.rect.y >= self.destino_posi_y and time.time() - self.tiempo_creacion > self.vida_util:
            return True
        return False
    def dibujar(self, screen):
        """
        Dibuja en la pantalla al Sol
        input: screen
        """
        screen.blit(self.image, self.rect)

    def clic_en(self, posi):
        """
        Dibuja en la pantalla al Sol
        input: posi
        """
        return self.rect.collidepoint(posi)
print('Todo bien con los soles')
#====================TODOS LOS BICHOS DEL JUEGO====================   
class NPC:
    def __init__(self, posi_x:int, posi_y:int, ancho:int, alto:int, imagen_surf:pg.surface=None):
        #Nota de Leon: Usamos imagen_surf = None por si nos escapa un error. 
        #Pongo un if que va a poner a la entidad como un cuadrado rojo y se re nota ^^
        self.rect = pg.Rect(posi_x, posi_y, ancho, alto)
        if imagen_surf:
            self.image = pg.transform.scale(imagen_surf, (ancho, alto))
        else:
            RED = (255, 0, 0)
            self.image = pg.Surface((ancho, alto))
            self.image.fill(RED) #ERROR CATCH >:D
        #la salud es una misky-herramienta que nos ayudara mas tarde
        self.hp = 1
        self.max_hp = 1
    def barra_hp(self, screen): 
        """
        Nota de Leon: Esta funcion esta para checkeo. Post terminar de checkear el daño borremosla
        """
        screen.blit(self.image, self.rect)
        if self.hp < self.max_hp:
            hp_bar_width = self.rect.width * (self.hp / self.max_hp)
            hp_bar_rect = pg.Rect(self.rect.x, self.rect.y - 10, hp_bar_width, 5)
            RED = (255, 0, 0)
            pg.draw.rect(screen, RED, hp_bar_rect)
    def dibujar(self, screen):
        screen.blit(self.image, self.rect)
print('Todo bien con los NPC')
#====================PLANTAS====================
class Planta(NPC):
    def __init__(self, fila:int, col:int, imagen_surf:pg.surface, c_size:int, margen_y:int, margen_x:int, costo:int, salud_inicial:int):
        super().__init__(
            margen_x + col * c_size,
            margen_y + fila * c_size,
            c_size, c_size,
            imagen_surf
        )
        self.fila = fila
        self.col = col
        self.costo = costo
        self.hp = salud_inicial
        self.max_hp = salud_inicial
        self.viva = True

    def recibir_dmg(self, cantidad):
        self.hp -= cantidad
        if self.hp <= 0:
            self.viva = False
            return True
        return False
#----Sunflower :3----
class Girasol(Planta):
    costo = 50
    salud_inicial = 6
    generacion_intervalo = 8 
    sol_generado_valor = 25
    def __init__(self, fila:int, col:int, imagen_surf:pg.surface, c_size:int, margen_y:int, margen_x:int, h:int, ima_sol:int):
        super().__init__(
            fila, col,
            imagen_surf,
            c_size, margen_y, margen_x,
            Girasol.costo, Girasol.salud_inicial)
        self.ultimo_sol_generado = time.time()
        self.c_size_ref = c_size
        self.margen_y_ref = margen_y
        self.h_ref = h
        self.ima_sol_ref = ima_sol

    def actualizar(self, soles_cayendo, c_size, margen_y, h, imagen_sol_surf):
        if time.time() - self.ultimo_sol_generado > self.generacion_intervalo:
            # Los soles de girasol aparecen un poco más arriba de la planta y caen
            sol_x = self.rect.centerx - (c_size // 4)
            sol_y = self.rect.centery - (c_size // 4) - 30 # Empieza más arriba del girasol
            soles_cayendo.append(Sol(sol_x, sol_y, self.c_size_ref, self.margen_y_ref, self.h_ref, self.ima_sol_ref, es_de_girasol=True))
            self.ultimo_sol_generado = time.time()
#----Sos nuestra papa favorita <3----
class Nuez(Planta):
    costo = 50
    salud_inicial = 60
    def __init__(self, fila:int, col:int, imagen_surf:pg.surface, c_size:int, margen_y:int, margen_x:int):
        super().__init__(
            fila, col,
            imagen_surf, 
            c_size, margen_y, margen_x,
            Nuez.costo, Nuez.salud_inicial)

#----Peeshooter/iceshooter----
class Guisante(NPC):
    def __init__(self, posi_x: int, posi_y: int, c_size: int, imagen_surf: pg.surface, daño: int = 0, velocidad: float = 8.0, es_congelante: bool = False):
        #escalo 40%
        ancho_guisante = int(c_size * 0.4) 
        alto_guisante = int(c_size * 0.4)
        
        #mini ajustes para que quede en el centro de la boca. Si encuentran mejor cambien
        posi_x_salida = posi_x + int(c_size * 0.7) 
        posi_y_salida = posi_y + int(c_size * 0.25) 

        super().__init__(posi_x_salida, posi_y_salida, ancho_guisante, alto_guisante, imagen_surf)
        self.fila = 0
        self.daño = 1
        self.velocidad = velocidad #no fps, sino tipo pixeles por segundo?
        self.es_congelante = es_congelante
        self.x = float(self.rect.x) #ara que se mueva fluido en no casillas trabajamos en float, no?

    def actualizar(self, dt):
        self.x += self.velocidad * dt # dt ya es en segundos, así que la velocidad es pixeles/segundo
        self.rect.x = int(self.x)

    def dibujar(self, screen):
        super().dibujar(screen)

class LanzaGuisantes(Planta):
    costo = 100
    salud_inicial = 100
    cadencia_disparo = 1.5  # Tiempo entre disparos en segundos
    dano_guisante = 20
    velocidad_guisante = 300.0
    def __init__(self, fila: int, col: int, imagen_surf: pg.Surface, c_size: int, margen_y: int, margen_x: int):
        super().__init__(
            fila=fila,
            col=col,
            imagen_surf=imagen_surf,
            c_size=c_size,
            margen_y=margen_y,
            margen_x=margen_x,
            costo=LanzaGuisantes.costo,
            salud_inicial=LanzaGuisantes.salud_inicial
        )
        self.tiempo_ultimo_disparo = time.time()
        
        
    def actualizar(self, zombis_en_juego: list, proyectiles_activos: list, dt: float, ima_guisante: pg.Surface):
        zombis_en_fila = [z for z in zombis_en_juego if z.fila == self.fila and z.rect.x > self.rect.x]
        
        if zombis_en_fila and (time.time() - self.tiempo_ultimo_disparo >= self.cadencia_disparo):
            nuevo_guisante = Guisante(
                posi_x=self.rect.x,
                posi_y=self.rect.y,
                c_size= self.rect.width,
                imagen_surf=ima_guisante,
                daño=self.dano_guisante,
                velocidad=self.velocidad_guisante,
                es_congelante=False
            )
            proyectiles_activos.append(nuevo_guisante)
            nuevo_guisante.fila = self.fila 
            self.tiempo_ultimo_disparo = time.time()

class LanzaGuisantesFrio(LanzaGuisantes):
    costo = 175
    salud_inicial = 100
    
    def __init__(self, fila: int, col: int, imagen_surf: pg.Surface, c_size: int, margen_y: int, margen_x: int):
        super().__init__(
            fila=fila,
            col=col,
            imagen_surf=imagen_surf,
            c_size=c_size,
            margen_y=margen_y,
            margen_x=margen_x
        )
        
    def actualizar(self, zombis_en_juego: list, proyectiles_activos: list, dt: float, ima_guisante_frio: pg.Surface):
        zombis_en_fila = [z for z in zombis_en_juego if z.fila == self.fila and z.rect.x > self.rect.x]
        
        if zombis_en_fila and (time.time() - self.tiempo_ultimo_disparo >= self.cadencia_disparo):
            nuevo_guisante = Guisante(
                posi_x=self.rect.x,
                posi_y=self.rect.y,
                c_size=self.rect.width,
                imagen_surf=ima_guisante_frio,
                daño=self.dano_guisante,
                velocidad=self.velocidad_guisante,
                es_congelante=True
            )
            proyectiles_activos.append(nuevo_guisante)
            self.tiempo_ultimo_disparo = time.time()
            nuevo_guisante.fila = self.fila 

# --- Clase Botón (para la barra lateral) ---
class BotonPlanta:
    def __init__(self, x, y, ancho, alto, tipo_planta, imagen_boton_surf, imagen_planta_completa_surf):
        self.rect = pg.Rect(x, y, ancho, alto)
        self.tipo_planta = tipo_planta
        self.costo = tipo_planta.costo
        self.imagen = pg.transform.scale(imagen_boton_surf, (ancho, alto))
        self.imagen_planta_completa = imagen_planta_completa_surf

        self.font = pg.font.Font(None, 24)
        self.color_borde_normal = (50, 50, 50)
        self.color_borde_seleccionado = AMARILLO
        self.color_borde_deshabilitado = RED

    def dibujar(self, surface, soles_actuales, planta_seleccionada_actual):
        surface.blit(self.imagen, self.rect)

        texto_costo = self.font.render(str(self.costo), True, BLANCO)
        surface.blit(texto_costo, (self.rect.x + 5, self.rect.y + self.rect.height - 20))

        # Dibujar borde y sombreado si no hay soles
        if self.tipo_planta == planta_seleccionada_actual:
            pg.draw.rect(surface, self.color_borde_seleccionado, self.rect, 3)
        elif soles_actuales < self.costo:
            pg.draw.rect(surface, self.color_borde_deshabilitado, self.rect, 2)
            sombreado = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
            sombreado.fill((0, 0, 0, 150))
            surface.blit(sombreado, self.rect)
        else:
            pg.draw.rect(surface, self.color_borde_normal, self.rect, 1)

    def clic_en(self, pos):
        return self.rect.collidepoint(pos)
print('Clases cargadas con Exito!')