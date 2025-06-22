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
    """
    ---INPUT---
    ancho_grilla:int, alto_grilla:int, imagen_pasto:pg.Surface, 
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

def dibujar_soles_hud(soles, test_font, screen):
    texto_soles = test_font.render(str(soles), True, BLANCO)
    screen.blit(texto_soles, (posi_x_barra_izq + w_barra_izq // 2 - texto_soles.get_width() // 2, 40))

def dibujar_barra_lateral(li_botones:list, soles_actuales, screen, planta_seleccionada, test_font):
    # Dibujar contador de soles
    dibujar_soles_hud(soles_actuales, test_font, screen)

    # Dibujar botones de plantas
    for boton in li_botones:
        boton.dibujar(screen, soles_actuales, planta_seleccionada)
def botones_plantas_armado(li_botones:list, y_actual_boton:int, type_planta, imagen_surf:pg.Surface, imagen_planta_completa_surf):
    """
    Genera los botones de la izquierda para poner las plantas en el jardin
    Tambien tiene la posi y tamaños definidos aca xsi lo quieren cambiar
    ---INPUT---
    li_botones -> lista de botones 

    """
    #-----FUNCION PARA PONER-----
    li_botones.append(BotonPlanta(posi_x_barra_izq + (w_barra_izq - b_size) // 2,y_actual_boton,b_size, b_size,type_planta, imagen_surf,imagen_planta_completa_surf ))
    y_actual_boton += b_size + tab_bot
    return y_actual_boton