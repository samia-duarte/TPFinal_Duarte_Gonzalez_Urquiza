import time
import pygame as pg
import random
#Bienvenido a la sección de clases de plantas. Por ahora aca vamos a dejar solo a los NPC y plantas
#Contenidos: Sol, Podadora, NPC, Plantas (todas)
# --- CONSTANTES DE COLORES ---
AMARILLO = (255, 255, 0)
DARK_GREEN = (0, 100, 0)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE_OSCURO_SELECCION = (0,70,0,150)

class Sol:
    """
    Maneja a los soles dentro del juego, los que jugadores pueden recolectar.
    Los soles caen desde la parte superior de la pantalla o son generados por Girasoles.
    """
    def __init__(self, posi_x:int, posi_y:int, c_size:int, margen_y:int, h:int, imagen_surf:pg.surface=None, es_de_girasol:bool =False, sol_val:int =25):
        """
        Inicializa un nuevo objeto Sol.

        Input:
            posi_x (int): Posición inicial X del sol.
            posi_y (int): Posición inicial Y del sol.
            c_size (int): Tamaño de celda de referencia, usado para escalar la imagen del sol.
            margen_y (int): Margen superior del área de juego.
            h (int): Altura total del área de juego.
            imagen_surf (pg.Surface, optional): Superficie de la imagen del sol. Si es None, se crea un cuadrado amarillo. Defaults to None.
            es_de_girasol (bool, optional): Indica si el sol fue generado por un Girasol. Defaults to False.
            sol_val (int, optional): Valor en soles que otorga al ser recolectado. Defaults to 25.
        """
        self.rect = pg.Rect(posi_x, posi_y, c_size // 2, c_size // 2)
        self.valor = sol_val
        if imagen_surf:
            self.image = pg.transform.scale(imagen_surf,(c_size // 2, c_size // 2))
        else:
            self.image = pg.Surface((c_size // 2, c_size // 2))
            self.image.fill((255, 255, 0))
        self.velocidad_caida = random.randint(1, 2) 
        self.tiempo_creacion = time.time()
        self.vida_util = 8 
        self.es_de_girasol = es_de_girasol #para que no se interrumpan entre si los timings y distancias caida
        if es_de_girasol == True:
            self.destino_posi_y = posi_y + c_size // 2 # Aterrizan cerca de la base de la planta
            self.rect.y -= 20 
        else:
            self.destino_posi_y = random.randint(int(margen_y + c_size), int(margen_y + h - c_size // 2))
    def actualizar(self) -> bool:
        """
        Actualiza la posición del sol a medida que cae y verifica si ha caducado.

        Returns:
            bool: True si el sol debe ser eliminado (llegó a su destino y caducó), False en caso contrario.
        """
        if self.rect.y < self.destino_posi_y:
            self.rect.y += self.velocidad_caida
            if self.rect.y > self.destino_posi_y:
                self.rect.y = self.destino_posi_y
        if self.rect.y >= self.destino_posi_y and time.time() - self.tiempo_creacion > self.vida_util:
            return True
        return False
    def dibujar(self, screen:pg.surface):
        """
        Dibuja en la pantalla al Sol
        Input: 
            screen, la pantalla/lienzo del juego
        """
        screen.blit(self.image, self.rect)

    def clic_en(self, posi: tuple[int, int]) -> bool:
        """
        Verifica si se ha hecho clic en la posición del sol.

        Input:
            posi (tuple[int, int]): La posición (x, y) del clic del mouse.

        Returns:
            bool: True si el clic ocurrió dentro del área del sol, False en caso contrario.
        """
        return self.rect.collidepoint(posi)
print('Todo bien con los soles')
class Podadora:
    """
    Representa una podadora que se muestra en cada fila y desaparece
    una vez que un zombie logra pasar por esa fila (una "vida" por fila).
    """
    def __init__(self, fila: int, margen_y: int, margen_x: int, c_size: int, imagen_surf: pg.Surface):
        super().__init__()
        """
        Inicializa un objeto Podadora.

        Input:
            fila (int): La fila en la que se encuentra esta podadora (0-indexado).
            margen_y (int): Margen superior del área de juego.
            margen_x (int): Margen izquierdo del área de juego.
            c_size (int): Tamaño de celda de referencia, usado para escalar la imagen de la podadora.
            imagen_surf (pg.Surface): Superficie de la imagen de la podadora.
        """
        self.fila = fila
        self.imagen_surf = pg.transform.scale(imagen_surf, (int(c_size * 1.2), c_size)) 
        self.rect = self.imagen_surf.get_rect()
        self.rect.y = margen_y + fila * c_size
        self.rect.x = margen_x - self.rect.width - 10 
        self.activa = True

    def dibujar(self, superficie: pg.Surface):
        """
        Dibuja la podadora en la pantalla si está activa.

        Input:
            superficie (pg.Surface): La superficie donde se dibujará la podadora.
        """
        if self.activa:
            superficie.blit(self.imagen_surf, self.rect)
#====================TODOS LOS BICHOS DEL JUEGO====================   
class NPC:
    """
    Clase base para todos los Personajes No Jugables (Non-Player Characters, NPC) en el juego,
    incluyendo plantas y zombies. Provee funcionalidades básicas de posicionamiento y salud.
    """
    def __init__(self, posi_x:int, posi_y:int, ancho:int, alto:int, imagen_surf:pg.surface=None):
        """
        Inicializa un nuevo NPC.

        Input:
            posi_x (int): Posición X inicial del NPC.
            posi_y (int): Posición Y inicial del NPC.
            ancho (int): Ancho del NPC.
            alto (int): Alto del NPC.
            imagen_surf (pg.Surface, optional): Superficie de la imagen del NPC. Si es None, se crea un cuadrado rojo. Defaults to None.
        """
        self.rect = pg.Rect(posi_x, posi_y, ancho, alto)
        if imagen_surf:
            self.image = pg.transform.scale(imagen_surf, (ancho, alto))
        else:
            RED = (255, 0, 0)
            self.image = pg.Surface((ancho, alto))
            self.image.fill(RED)
        self.hp = 1
        self.max_hp = 1
    def dibujar(self, screen:pg.surface):
        """
        Dibuja al NPC en la pantalla
        Input:
            screen, pantalla/lienzo del juego
        """
        screen.blit(self.image, self.rect)
print('Todo bien con los NPC')
#====================PLANTAS====================
class Planta(NPC):
    """
    Clase base para todas las plantas en el juego. Hereda de NPC y añade
    atributos específicos de las plantas como costo, fila, columna y estado de vida.
    """
    def __init__(self, fila:int, col:int, imagen_surf:pg.surface, c_size:int, margen_y:int, margen_x:int, costo:int, salud_inicial:int):
        super().__init__(
            margen_x + col * c_size,
            margen_y + fila * c_size,
            c_size, c_size,
            imagen_surf
        )
        """
        Inicializa una nueva Planta.

        Input:
            fila (int): Fila en la grilla donde se ubicará la planta.
            col (int): Columna en la grilla donde se ubicará la planta.
            imagen_surf (pg.Surface): Superficie de la imagen de la planta.
            c_size (int): Tamaño de celda en píxeles.
            margen_y (int): Margen superior del área de juego.
            margen_x (int): Margen izquierdo del área de juego.
            costo (int): Costo en soles para plantar esta planta.
            salud_inicial (int): Puntos de salud iniciales de la planta.
        """
        self.fila = fila
        self.col = col
        self.costo = costo
        self.hp = salud_inicial
        self.max_hp = salud_inicial
        self.viva = True
        self.ultimo_uso = time.time()
        self.cooldown_activo = False

    def recibir_dmg(self, cantidad:int) -> bool:
        """
        Calcula el daño recibido por la planta y actualiza su salud.

        Input:
            cantidad (int): Cantidad de daño a aplicar.

        Returns:
            bool: True si la planta ha sido destruida (salud <= 0), False en caso contrario.
        """
        self.hp -= cantidad
        if self.hp <= 0:
            self.viva = False
            return True
        return False
#----Sunflower :3----
class Girasol(Planta):
    """
    Representa una planta Girasol. Hereda de Planta y se especializa
    en la generación de soles periódicamente.
    """
    costo = 50
    salud_inicial = 6
    generacion_intervalo = 8 
    sol_generado_valor = 25
    cooldown = 10
    def __init__(self, fila:int, col:int, imagen_surf:pg.surface, c_size:int, margen_y:int, margen_x:int, h:int, ima_sol:int):
        super().__init__(
            fila, col,
            imagen_surf,
            c_size, margen_y, margen_x,
            Girasol.costo, Girasol.salud_inicial)
        """
        Inicializa un nuevo Girasol.

        Input:
            fila (int): Fila en la grilla donde se ubicará la planta.
            col (int): Columna en la grilla donde se ubicará la planta.
            imagen_surf (pg.Surface): Superficie de la imagen del Girasol.
            c_size (int): Tamaño de celda en píxeles.
            margen_y (int): Margen superior del área de juego.
            margen_x (int): Margen izquierdo del área de juego.
            h (int): Altura total del área de juego.
            ima_sol (pg.Surface): Superficie de la imagen del sol para los soles que genera.
        """
        self.ultimo_sol_generado = time.time()
        self.c_size_ref = c_size
        self.margen_y_ref = margen_y
        self.h_ref = h
        self.ima_sol_ref = ima_sol

    def actualizar(self, soles_cayendo, c_size, margen_y, h, imagen_sol_surf):
        """
        Actualiza el estado del Girasol, generando soles si ha pasado el intervalo.

        Input:
            soles_cayendo (list): Lista de soles activos en el juego, donde se añadirá el nuevo sol.
            c_size (int): Tamaño de celda de referencia.
            margen_y (int): Margen superior del área de juego.
            h (int): Altura total del área de juego.
            imagen_sol_surf (pg.Surface): Superficie de la imagen del sol.
        """
        if time.time() - self.ultimo_sol_generado > self.generacion_intervalo:
            # Los soles de girasol aparecen un poco más arriba de la planta y caen
            sol_x = self.rect.centerx - (c_size // 4)
            sol_y = self.rect.centery - (c_size // 4) - 30 # Empieza más arriba del girasol
            soles_cayendo.append(Sol(sol_x, sol_y, self.c_size_ref, self.margen_y_ref, self.h_ref, self.ima_sol_ref, es_de_girasol=True))
            self.ultimo_sol_generado = time.time()
class Nuez(Planta):
    """
    Representa una planta Nuez. Hereda de Planta y se especializa
    en tener una alta cantidad de salud para actuar como defensa.
    La mejor papa de todas <3
    """
    costo = 50
    salud_inicial = 60
    cooldown = 40
    def __init__(self, fila:int, col:int, imagen_surf:pg.surface, c_size:int, margen_y:int, margen_x:int):
        super().__init__(
            fila, col,
            imagen_surf, 
            c_size, margen_y, margen_x,
            Nuez.costo, Nuez.salud_inicial)
        """
        Inicializa una nueva Nuez.

        Input:
            fila (int): Fila en la grilla donde se ubicará la planta.
            col (int): Columna en la grilla donde se ubicará la planta.
            imagen_surf (pg.Surface): Superficie de la imagen de la Nuez.
            c_size (int): Tamaño de celda en píxeles.
            margen_y (int): Margen superior del área de juego.
            margen_x (int): Margen izquierdo del área de juego.
        """

class Guisante(NPC):
    """
    Representa un proyectil Guisante disparado por LanzaGuisantes o LanzaGuisantesFrio.
    Hereda de NPC y se mueve horizontalmente para dañar zombies.
    """
    def __init__(self, posi_x: int, posi_y: int, c_size: int, imagen_surf: pg.surface, daño: int = 0, velocidad: float = 8.0, es_congelante: bool = False):
        ancho_guisante = int(c_size * 0.4) 
        alto_guisante = int(c_size * 0.4)
        
        #mini ajustes para que quede en el centro de la boca.
        posi_x_salida = posi_x + int(c_size * 0.7) 
        posi_y_salida = posi_y + int(c_size * 0.25) 

        super().__init__(posi_x_salida, posi_y_salida, ancho_guisante, alto_guisante, imagen_surf)
        """
        Inicializa un nuevo Guisante.

        Input:
            posi_x (int): Posición X inicial del guisante.
            posi_y (int): Posición Y inicial del guisante.
            c_size (int): Tamaño de celda de referencia, usado para escalar la imagen del guisante.
            imagen_surf (pg.Surface): Superficie de la imagen del guisante.
            daño (int, optional): Cantidad de daño que inflige el guisante. Defaults to 0.
            velocidad (float, optional): Velocidad de movimiento del guisante en píxeles por segundo. Defaults to 8.0.
            es_congelante (bool, optional): Indica si el guisante tiene efecto de congelación. Defaults to False.
        """
        self.fila = 0
        self.daño = 1
        self.velocidad = velocidad
        self.es_congelante = es_congelante
        self.x = float(self.rect.x)

    def actualizar(self, dt:float):
        """
        Actualiza la posición del guisante en cada fotograma.

        Input:
            dt (float): Delta time, el tiempo transcurrido desde el último fotograma en segundos.
        """
        self.x += self.velocidad * dt
        self.rect.x = int(self.x)

    def dibujar(self, screen:pg.surface):
        """
        Dibuja el guisante en la pantalla.

        Input:
            screen (pg.Surface): La superficie principal de la pantalla del juego.
        """
        super().dibujar(screen)

class LanzaGuisantes(Planta):
    """
    Representa una planta LanzaGuisantes. Hereda de Planta y se especializa
    en disparar proyectiles Guisante a los zombies en su fila.
    """
    costo = 100
    salud_inicial = 6
    cadencia_disparo = 1.5  # Tiempo entre disparos en segundos
    dano_guisante = 20
    velocidad_guisante = 300.0
    cooldown = 10
    def __init__(self, fila: int, col: int, imagen_surf: pg.Surface, c_size: int, margen_y: int, margen_x: int):
        super().__init__(
            fila, col,
            imagen_surf, c_size, 
            margen_y, margen_x,
            costo=LanzaGuisantes.costo,
            salud_inicial=LanzaGuisantes.salud_inicial,
        )
        """
        Inicializa una nueva planta LanzaGuisantes.

        Input:
            fila (int): Fila en la grilla donde se ubicará la planta.
            col (int): Columna en la grilla donde se ubicará la planta.
            imagen_surf (pg.Surface): Superficie de la imagen del LanzaGuisantes.
            c_size (int): Tamaño de celda en píxeles.
            margen_y (int): Margen superior del área de juego.
            margen_x (int): Margen izquierdo del área de juego.
        """
        self.tiempo_ultimo_disparo = time.time()
        
        
    def actualizar(self, zombis_en_juego: list, proyectiles_activos: list, dt: float, ima_guisante: pg.Surface):
        """
        Actualiza el estado del LanzaGuisantes, disparando guisantes si hay zombies
        en su fila y el cooldown de disparo lo permite.

        Input:
            zombis_en_juego (list): Lista de todos los zombies activos en el juego.
            proyectiles_activos (list): Lista de todos los proyectiles activos, donde se añadirá el nuevo guisante.
            dt (float): Delta time, el tiempo transcurrido desde el último fotograma en segundos.
            ima_guisante (pg.Surface): Superficie de la imagen del guisante normal.
        """
        # Filtra los zombies que están en la misma fila y a la derecha de la planta
        zombis_en_fila = [z for z in zombis_en_juego if z.fila == self.fila and z.rect.x > self.rect.x]
        
        if zombis_en_fila and (time.time() - self.tiempo_ultimo_disparo >= self.cadencia_disparo):
            #Si hay zombies Y paso el suficiente tiempo entre disparo y disparo
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
    """
    Representa una planta LanzaGuisantes de Hielo. Hereda de LanzaGuisantes
    y dispara proyectiles Guisante que tienen un efecto congelante.
    """
    costo = 175
    salud_inicial = 6
    cooldown = 15
    def __init__(self, fila: int, col: int, imagen_surf: pg.Surface, c_size: int, margen_y: int, margen_x: int):
        super().__init__(
            fila, col,
            imagen_surf,
            c_size, margen_y, margen_x,
        )
        """
        Inicializa una nueva planta LanzaGuisantesFrio.

        Input:
            fila (int): Fila en la grilla donde se ubicará la planta.
            col (int): Columna en la grilla donde se ubicará la planta.
            imagen_surf (pg.Surface): Superficie de la imagen del LanzaGuisantesFrio.
            c_size (int): Tamaño de celda en píxeles.
            margen_y (int): Margen superior del área de juego.
            margen_x (int): Margen izquierdo del área de juego.
        """
    def actualizar(self, zombis_en_juego: list, proyectiles_activos: list, dt: float, ima_guisante_frio: pg.Surface):
        """
        Actualiza el estado del LanzaGuisantesFrio, disparando guisantes congelantes
        si hay zombies en su fila y el cooldown de disparo lo permite.

        Input:
            zombis_en_juego (list): Lista de todos los zombies activos en el juego.
            proyectiles_activos (list): Lista de todos los proyectiles activos, donde se añadirá el nuevo guisante.
            dt (float): Delta time, el tiempo transcurrido desde el último fotograma en segundos.
            ima_guisante_frio (pg.Surface): Superficie de la imagen del guisante congelante.
        """
        # Filtra los zombies que están en la misma fila y a la derecha de la planta
        zombis_en_fila = [z for z in zombis_en_juego if z.fila == self.fila and z.rect.x > self.rect.x]
        
        if zombis_en_fila and (time.time() - self.tiempo_ultimo_disparo >= self.cadencia_disparo):
            #Si hay zombies Y paso el suficiente tiempo entre disparo y disparo
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
class Boton:
    """
    Clase base para todos los botones de la interfaz de usuario.
    Provee funcionalidades básicas de clic y dibujo.
    """
    def __init__(self, x, y, ancho, alto, imagen_boton_surf):
        """
        Inicializa un nuevo Botón.

        Input:
            x (int): Posición X del botón.
            y (int): Posición Y del botón.
            ancho (int): Ancho del botón.
            alto (int): Alto del botón.
            imagen_boton_surf (pg.Surface): Superficie de la imagen del botón.
        """
        self.rect = pg.Rect(x, y, ancho, alto)
        self.imagen = pg.transform.scale(imagen_boton_surf, (ancho, alto))
        self.font = pg.font.Font(None, 24)

    def clic_en(self, pos: tuple[int, int]) -> bool:
        """
        Verifica si se ha hecho clic en la posición del botón.

        Input:
            pos (tuple[int, int]): La posición (x, y) del clic del mouse.

        Returns:
            bool: True si el clic ocurrió dentro del área del botón, False en caso contrario.
        """
        return self.rect.collidepoint(pos)

    def dibujar(self, surface: pg.Surface):
        """
        Dibuja el botón en la superficie dada.

        Input:
            surface (pg.Surface): La superficie donde se dibujará el botón.
        """
        surface.blit(self.imagen, self.rect)

class BotonPlanta(Boton):
    """
    Representa un botón en la barra lateral para seleccionar y plantar un tipo específico de planta.
    Hereda de Boton y gestiona el costo, el cooldown y el estado de selección.
    """
    def __init__(self, x, y, ancho, alto, tipo_planta, imagen_boton_surf, imagen_planta_completa_surf):
        super().__init__(x, y, ancho, alto, imagen_boton_surf)
        """
        Inicializa un nuevo BotonPlanta.

        Args:
            x (int): Posición X del botón.
            y (int): Posición Y del botón.
            ancho (int): Ancho del botón.
            alto (int): Alto del botón.
            tipo_planta: La clase de la planta asociada a este botón (e.g., Girasol, LanzaGuisantes).
            imagen_boton_surf (pg.Surface): Superficie de la imagen del botón (icono pequeño).
            imagen_planta_completa_surf (pg.Surface): Superficie de la imagen completa de la planta (para el "fantasma" al seleccionar).
        """
        self.rect = pg.Rect(x, y, ancho, alto)
        self.tipo_planta = tipo_planta
        self.costo = tipo_planta.costo
        self.imagen_planta_completa = imagen_planta_completa_surf
        self.tiempo_ultimo_uso = 0

        self.font = pg.font.Font(None, 24)
        self.color_borde_normal = (50, 50, 50)
        self.color_borde_seleccionado = AMARILLO
        self.color_borde_deshabilitado = RED
        self.cooldown_overlay_color = (0, 0, 0, 150)

    def esta_disponible(self) -> bool:
        """
        Verifica si la planta asociada al botón está disponible para ser plantada
        (es decir, si su cooldown ha terminado).

        Returns:
            bool: True si la planta está disponible, False en caso contrario.
        """
        return (time.time() - self.tiempo_ultimo_uso) >= self.tipo_planta.cooldown
    def iniciar_cooldown(self):
        """
        Inicia el cooldown del botón, registrando el tiempo actual.
        """
        self.tiempo_ultimo_uso = time.time()
    
    def dibujar(self, surface, soles_actuales, planta_seleccionada_actual):
        """
        Dibuja el botón de la planta, mostrando su costo, estado de selección,
        disponibilidad (por soles) y cooldown.

        Args:
            surface (pg.Surface): La superficie donde se dibujará el botón.
            soles_actuales (int): La cantidad actual de soles del jugador.
            planta_seleccionada_actual: La clase de la planta actualmente seleccionada por el jugador.
        """
        super().dibujar(surface)
        texto_costo = self.font.render(str(self.costo), True, BLANCO)
        surface.blit(texto_costo, (self.rect.x + 5, self.rect.y + self.rect.height - 20))

        
        if self.tipo_planta == planta_seleccionada_actual:
            #todo bien
            pg.draw.rect(surface, self.color_borde_seleccionado, self.rect, 3)
        elif soles_actuales < self.costo:
            #no hay soles
            pg.draw.rect(surface, self.color_borde_deshabilitado, self.rect, 2)
            sombreado = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
            sombreado.fill((0, 0, 0, 150))
            surface.blit(sombreado, self.rect)
        elif not self.esta_disponible():
            #esta en cooldown
            tiempo_restante = max(0, self.tipo_planta.cooldown - (time.time() - self.tiempo_ultimo_uso))
            porcentaje_completado = 1 - (tiempo_restante / self.tipo_planta.cooldown)

            #capa de cooldown
            cooldown_height = int(self.rect.height * (1 - porcentaje_completado))
            cooldown_surface = pg.Surface((self.rect.width, cooldown_height), pg.SRCALPHA)
            cooldown_surface.fill(self.cooldown_overlay_color)
            surface.blit(cooldown_surface, (self.rect.x, self.rect.y))

            pg.draw.rect(surface, self.color_borde_deshabilitado, self.rect, 2)
        else:
            pg.draw.rect(surface, self.color_borde_normal, self.rect, 1)
    
class BotonPala(Boton):
    """
    Representa el botón de la Pala en la barra lateral. Hereda de Boton y
    gestiona su estado de selección.
    """
    def __init__(self, x, y, ancho, alto, imagen_boton_surf):
        """
        Inicializa un nuevo BotonPala.

        Args:
            x (int): Posición X del botón.
            y (int): Posición Y del botón.
            ancho (int): Ancho del botón.
            alto (int): Alto del botón.
            imagen_boton_surf (pg.Surface): Superficie de la imagen del botón de la pala.
        """
        super().__init__(x, y, ancho, alto, imagen_boton_surf)
        self.selected = False
        self.nombre = "Pala"

    def dibujar(self, surface, seleccionado_actual):
        """
        Dibuja el botón de la Pala, resaltándolo si está seleccionado.

        Args:
            surface (pg.Surface): La superficie donde se dibujará el botón.
            seleccionado_actual: El objeto o tipo actualmente seleccionado (puede ser este botón de pala).
        """
        super().dibujar(surface)
        if self.selected or (seleccionado_actual == self):
            pg.draw.rect(surface, AMARILLO, self.rect, 3) # Resaltar si está seleccionada

    def diggy_on(self):
        """
        Activa el estado de selección de la pala.
        """
        self.selected = True

    def diggy_off(self):
        """
        Desactiva el estado de selección de la pala.
        """
        self.selected = False

print('Clases cargadas con Exito!')