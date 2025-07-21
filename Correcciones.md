# TPFinal Duarte - Gonzalez - de Urquiza

## Reporte

### **General**

El código presenta una estructura lógica sólida, con una correcta separación en clases y módulos que refleja una buena comprensión de los principios que vimos en clase. Se le suma una demostración clara de un trabajo de investigación y lectura de la documentación de las librerías propuestas. Sin embargo, en algunos sectores (como el del bucle principal) se evidencia una concentración excesiva de lógica que podría beneficiarse de una mayor modularización dividiendo responsabilidades en funciones algo más pequeñas y específicas para hacer más fácil lo relacionado a legibilidad y mantenimiento. Los nombres de las clases y funciones son en general apropiados y expresivos, pero se recomienda evitar ambigüedades o repeticiones innecesarias. Los comentarios cumplen una función útil para la comprensión e interpretación rápida de la lógica pensada e implementada, aunque podrían organizarse mejor con bloques más descriptivos o encabezados que faciliten el escaneo visual del código. En términos generales, es un muy bueno el nivel de implementación que podría perfeccionarse con pequeñas mejoras de estilo y estructura.

Por otro lado, el repositorio está correctamente organizado, con una división clara entre archivos de lógica, clases, funciones gráficas y recursos. Esta separación facilita enormemente la comprensión del flujo del programa y permite ubicar rápidamente los elementos que se desean modificar o revisar. El problema que encontré es que en el `README.md` se podrían dar más detalles que indiquen los pasos para ejecutar el juego, posibles dependencias (como versiones específicas de `pygame`), y una breve explicación del propósito de cada archivo principal. También sería útil agregar un archivo `requirements.txt` para facilitar la instalación del entorno. A pesar de estos detalles menores, la organización general del repositorio es clara, coherente y adecuada para un proyecto de este tipo. En próximos proyectos no olviden de colocar un `.gitignore` para quitarse de encima archivos y carpetas que no aportan nada al repositoio (ej. `__pycache__\`)

**Puntos positivos:**

* Código bien estructurado y separado en módulos temáticos: lógica, clases, interfaz, bucle principal.
* Se cumple completamente con la consigna de juego funcional, con todos los elementos requeridos (plantas, zombis, soles, podadoras, oleadas).
* Uso extensivo de programación orientada a objetos y pygame, con manejo detallado de estados y colisiones. Buen trabajo de investigación.
* Se nota un trabajo cuidadoso y una excelente comprensión del sistema de juego.

**Aspectos a mejorar:**

* El archivo `main_final.py` es excesivamente largo (\~5000 líneas aprox. en total si se suma todo), podría dividirse en más funciones auxiliares para mejorar la legibilidad. Ojo con la repetición de código y de lógicas que pueden se encapsuladas y nucleadas en distintos archivos extas.
* No hay una sección concreta explícita del `README.md` que describa cómo instalar o correr el juego (aunque el resumen del archivo sí explica mucho).

**Recomendaciones:**

* Agregar un `requirements.txt` o una línea en el README con la versión de Pygame.
* Extraer el bucle principal (`while running:`) en una función `main()` para facilitar pruebas o integraciones.

---

### **Backend**

**Puntos positivos:**

* Excelente uso de clases para las plantas, proyectiles y zombis.
* Las clases heredan correctamente (`NPC`, `Planta`, `Zombie`), y se reutilizan métodos con claridad.
* Se implementan efectos como congelamiento, oleadas progresivas, cooldowns, e interacciones múltiples entre entidades. Excelente idea la del congelamiento, me parece algo super original y bien implementado.

**Aspectos a mejorar:**

* Algunas funciones están muy cargadas con muchísimas responsabilidades (por ejemplo, la actualización de proyectiles dentro del `main`). Otras modularizaciones quitarían responsabilidades a esta parte del código y haría más sencillo su mantenimiento.

**Recomendaciones:**

* Mover parte de la lógica de combate o colisión a métodos internos de `Zombie` o `Planta` para seguir principios de encapsulamiento.

---

### **Frontend**

**Puntos positivos:**

* Interfaz visual clara y funcional.
* Efecto de "fantasma" de planta antes de colocarla (muy buen detalle visual).
* Cooldown visual en los botones de las plantas (opacidad y barra de tiempo). Quizas demasiado cooldown en la nuez!
* Indicador de soles y selección de plantas/pala muy bien resuelto.

**Aspectos a mejorar:**

* El texto de `print()` (como “¡Haz clic en una celda válida!” o “¡No tienes suficientes soles!”) aparece solo por consola!! Es mucho mejor tener todo junto enn pantalla. Ese texto lo veo recién despues del game over.

**Recomendaciones:**

* Agregar un sistema de mensajes temporales en pantalla para feedback del usuario (por ejemplo, en HUD). Quitar toda interacción desde la terminal.

---

### **Extras**

**Puntos positivos:**

* Se incluye una planta adicional: **LanzaGuisantesFrio**, con efecto de *ralentización*. Increíble idea, muy bien lograda!
* Se implementa el reembolso parcial al eliminar plantas con la pala. Muy buena mejora inspirada en la segunda entega del juego original.
* Implementación de oleadas complejas con tiempos, tipos y cantidades distintas de zombis.

**Aspectos a mejorar:**

* No se incluye música adicional ni animaciones específicas, pero se usa soundtrack básico y sonidos de fin.

**Recomendaciones:**

* Incluir sonidos para disparos, cosecha de soles o colocación de plantas podría elevar mucho la experiencia de jugabilidad.
