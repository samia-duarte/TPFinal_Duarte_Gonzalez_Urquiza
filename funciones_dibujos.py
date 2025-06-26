import pygame as pg
from clases_plantas import BotonPlanta
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
def dibujar_fondo_grilla(ancho_grilla:int, alto_grilla:int, col:int, fil:int, c_size:int, screen, margen_x, margen_y, imagen_pasto:pg.Surface):
    '''Dibuja la grilla de juego con pasto y líneas de división.
    
    Args:
        ancho_grilla (int): Ancho total de la grilla en píxeles.
        alto_grilla (int): Alto total de la grilla en píxeles.
        col (int): Número de columnas.
        fil (int): Número de filas.
        c_size (int): Tamaño de cada celda en píxeles.
        screen (pg.Surface): Superficie donde se dibujará.
        margen_x (float): Margen horizontal de la grilla.
        margen_y (float): Margen vertical de la grilla.
        imagen_pasto (pg.Surface): Imagen del pasto a escalar.
    '''
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

def dibujar_soles_hud(soles: int, test_font: pg.font.Font, screen: pg.Surface)-> None:
    texto_soles = test_font.render(str(soles), True, BLANCO)
    screen.blit(texto_soles, (posi_x_barra_izq + w_barra_izq // 2 - texto_soles.get_width() // 2, 40))
    '''Muestra el contador de soles en la barra lateral.
    Argumentos:
        soles (int): Cantidad actual de soles.
        test_font (pg.font.Font): Fuente para el texto.
        screen (pg.Surface): Superficie donde se dibujará.
    '''
def dibujar_barra_lateral(li_botones:list, soles_actuales, screen, planta_seleccionada, test_font):
    '''Dibuja todos los elementos de la barra lateral izquierda.
    Argumentos:
        li_botones (list): Lista de botones de plantas.
        soles_actuales (int): Cantidad actual de soles.
        screen (pg.Surface): Superficie donde se dibujará.
        planta_seleccionada (type): Clase de la planta seleccionada (o None).
        test_font (pg.font.Font): Fuente para el texto.
    '''
    dibujar_soles_hud(soles_actuales, test_font, screen)

    # Dibujar botones de plantas
    for boton in li_botones:
        boton.dibujar(screen, soles_actuales, planta_seleccionada)
def botones_plantas_armado(li_botones:list, y_actual_boton:int, type_planta, imagen_surf:pg.Surface, imagen_planta_completa_surf):
    """
    Genera los botones de la izquierda para poner las plantas en el jardin
    Tambien tiene la posi y tamaños definidos aca xsi lo quieren cambiar
    Argumentos:
        li_botones (list): Lista donde se agregarán los botones.
        y_actual_boton (int): Posición Y actual para el nuevo botón.
        type_planta (type): Clase de la planta asociada al botón.
        imagen_surf (pg.Surface): Imagen del botón.
        imagen_planta_completa_surf (pg.Surface): Imagen de la planta completa.
    Returns:
        int: Nueva posición Y para el próximo botón.
    """
    #-----FUNCION PARA PONER-----
    li_botones.append(BotonPlanta(posi_x_barra_izq + (w_barra_izq - b_size) // 2,y_actual_boton,b_size, b_size,type_planta, imagen_surf,imagen_planta_completa_surf ))
    y_actual_boton += b_size + tab_bot
    return y_actual_boton