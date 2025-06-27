import pygame as pg
from clases_plantas_final import BotonPlanta, BotonPala
AMARILLO = (255, 255, 0)
DARK_GREEN = (0, 100, 0)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE_OSCURO_SELECCION = (0,70,0,150)
# --------Valores para la barra lateral izquierda (botones)--------
w_barra_izq = 120
posi_x_barra_izq = 0
tab_bot = 10
b_size = 80
def dibujar_fondo_grilla(ancho_grilla: int, alto_grilla: int, col: int, fil: int, c_size: int, screen: pg.Surface, margen_x: int, margen_y: int, imagen_pasto: pg.Surface) -> None:
    """
    Dibuja el fondo de la grilla del jardín con una imagen de pasto y líneas de cuadrícula.

    Input:
        ancho_grilla (int): Ancho total de la grilla en píxeles.
        alto_grilla (int): Alto total de la grilla en píxeles.
        col (int): Número de columnas en la grilla.
        fil (int): Número de filas en la grilla.
        c_size (int): Tamaño de cada celda de la grilla (cuadrada) en píxeles.
        screen (pygame.Surface): Superficie de Pygame donde se dibujará la grilla.
        margen_x (int): Margen horizontal desde el borde izquierdo de la pantalla hasta la grilla.
        margen_y (int): Margen vertical desde el borde superior de la pantalla hasta la grilla.
        imagen_pasto (pygame.Surface): Superficie de Pygame con la imagen del pasto para el fondo.
    """
    # Escala la imagen del pasto al tamaño total de la grilla
    scaled_imagen_pasto = pg.transform.scale(imagen_pasto, (ancho_grilla, alto_grilla))
    screen.blit(scaled_imagen_pasto, (margen_x, margen_y)) #coloco el pasto en posic x,y

    color_lineas = GREEN

    # Lineas verticales
    for c_idx in range(col-1):
        x = int(margen_x + c_idx * c_size)
        pg.draw.line(screen, color_lineas, (x, int(margen_y)), (x, int(margen_y + alto_grilla)))

    # Lineas horizontales
    for f_idx in range(fil + 1): # +1 para dibujar la línea final
        y = int(margen_y + f_idx * c_size)
        pg.draw.line(screen, color_lineas, (int(margen_x), y), (int(margen_x + ancho_grilla), y))

def dibujar_soles_hud(soles: int, test_font: pg.font.Font, screen: pg.Surface) -> None:
    """
    Dibuja el contador de soles en la interfaz de usuario (HUD).

    Input:
        soles (int): La cantidad actual de soles.
        test_font (pygame.font.Font): La fuente de Pygame a utilizar para renderizar el texto.
        screen (pygame.Surface): La superficie de Pygame donde se dibujará el contador.
    """
    texto_soles = test_font.render(str(soles), True, BLANCO)
    screen.blit(texto_soles, (posi_x_barra_izq + w_barra_izq // 2 - texto_soles.get_width() // 2, 40))

def dibujar_barra_lateral(li_botones: list, soles_actuales: int, screen: pg.Surface, seleccionado_atm: str, test_font: pg.font.Font) -> None:
    """
    Dibuja la barra lateral izquierda que contiene el contador de soles y los botones de plantas/pala.

    Input:
        li_botones (list): Lista de objetos BotonPlanta y BotonPala para dibujar.
        soles_actuales (int): Cantidad actual de soles para verificar la disponibilidad de los botones de plantas.
        screen (pygame.Surface): Superficie de Pygame donde se dibujará la barra lateral.
        seleccionado_atm (str): Indica el tipo de elemento actualmente seleccionado (ej. "tipo_planta", "pala_activada").
        test_font (pygame.font.Font): La fuente de Pygame para el contador de soles.
    """
    dibujar_soles_hud(soles_actuales, test_font, screen)
    for boton in li_botones:
        if isinstance(boton, BotonPlanta):
            # BotonPlanta needs soles_actuales and the currently selected plant TYPE
            boton.dibujar(screen, soles_actuales, seleccionado_atm)
        elif isinstance(boton, BotonPala):
            # BotonPala only needs the current selected TOOL (which could be itself)
            boton.dibujar(screen, seleccionado_atm == "pala_activada")
        else:
            # Fallback for any other generic buttons if they exist
            boton.dibujar(screen)

def botones_plantas_armado(li_botones: list, y_actual_boton: int, type_planta, imagen_surf: pg.Surface, imagen_planta_completa_surf: pg.Surface) -> int:
    """
    Genera y añade un botón de planta a la lista de botones de la barra lateral.

    Input:
        li_botones (list): La lista de botones a la que se añadirá el nuevo botón.
        y_actual_boton (int): La posición Y actual para colocar el nuevo botón.
        type_planta (type): El tipo de clase de planta asociada a este botón.
        imagen_surf (pygame.Surface): La imagen a mostrar en el botón de la barra lateral.
        imagen_planta_completa_surf (pygame.Surface): La imagen completa de la planta que se usará al colocarla en el jardín.

    Returns:
        int: La nueva posición Y para el siguiente botón, después de añadir este.
    """
    #-----FUNCION PARA PONER-----
    li_botones.append(BotonPlanta(posi_x_barra_izq + (w_barra_izq - b_size) // 2,y_actual_boton,b_size, b_size,type_planta, imagen_surf,imagen_planta_completa_surf ))
    y_actual_boton += b_size + tab_bot

    return y_actual_boton
def boton_pala_armado(li_botones: list, y_actual_boton: int, ima_pala_boton: pg.Surface) -> int:
    """
    Genera y añade un botón de pala a la lista de botones de la barra lateral.

    Input:
        li_botones (list): La lista de botones a la que se añadirá el nuevo botón.
        y_actual_boton (int): La posición Y actual para colocar el nuevo botón.
        ima_pala_boton (pygame.Surface): La imagen a mostrar en el botón de la pala.

    Returns:
        int: La nueva posición Y para el siguiente botón, después de añadir este.
    """
    li_botones.append(BotonPala(posi_x_barra_izq + (w_barra_izq - b_size) // 2, y_actual_boton + 20, b_size, b_size, ima_pala_boton))
    return y_actual_boton + b_size + tab_bot