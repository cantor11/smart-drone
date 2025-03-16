# Smart Drone
## Proyecto 1 de Inteligencia Artifical

### Autores
    Junior Orlando Cantor Arévalo – 2224949 <junior.cantor@correounivalle.edu.co>
    Junior Orlando Cantor Arévalo – 2224949 <junior.cantor@correounivalle.edu.co>
    Junior Orlando Cantor Arévalo – 2224949 <junior.cantor@correounivalle.edu.co>
    Junior Orlando Cantor Arévalo – 2224949 <junior.cantor@correounivalle.edu.co>

### Descripción del Proyecto
Este proyecto es una simulación de un dron inteligente que debe recoger paquetes en un entorno representado por una matriz de 10x10. El dron puede moverse en las cuatro direcciones (arriba, abajo, izquierda y derecha), y su movimiento tiene un costo base de 1. Sin embargo, si el dron se encuentra con un campo electromagnético, el costo aumenta a 8. El objetivo es utilizar algoritmos de búsqueda para determinar la mejor ruta para recoger todos los paquetes en el entorno.

### Funcionalidades:
- Cargar un mundo desde un archivo de texto con la estructura establecida.
- Mostrar gráficamente el entorno inicial del dron.
- Permitir la selección del tipo de búsqueda: "No informada" o "Informada".
- Si se elige una búsqueda "No informada", se podrá seleccionar entre "Amplitud", "Costo uniforme" y "Profundidad evitando ciclos".
- Si se elige una búsqueda "Informada", se podrá seleccionar entre "Avara" y "A*".
- Ejecutar la simulación del dron según el algoritmo seleccionado, mostrando una animación de sus movimientos.
- Mostrar un reporte con la cantidad de nodos expandidos, la profundidad del árbol y el tiempo de cómputo. Para los algoritmos "Costo uniforme" y "A*", también se mostrará el costo de la solución.

### Estructura y ejecución
1. El proyecto está dividido en dos módulos principales:
- interfaz.py: Contiene la interfaz gráfica con Tkinter para cargar el archivo del mundo, seleccionar el algoritmo y visualizar el reporte.
- simulacion.py: Contiene la lógica de la simulación con Pygame, mostrando la animación del dron.

2. Para ejecutar la aplicación, simplemente ejecuta el archivo interfaz.py:
    python interfaz.py

3. Formato del Archivo de Entrada:
El archivo de entrada debe ser un archivo de texto con una matriz de 10x10 donde:
- 0 representa una casilla libre.
- 1 representa un obstáculo.
- 2 representa la posición inicial del dron.
- 3 representa un campo electromagnético.
- 4 representa un paquete.

        1 1 0 0 0 0 0 1 1 1
        1 1 0 1 0 1 0 1 1 1
        0 2 0 3 4 4 0 0 0 0
        0 1 1 1 0 1 1 1 1 0
        0 1 1 1 0 0 0 0 0 0
        3 3 0 1 0 1 1 1 1 1
        1 1 0 1 0 0 0 0 0 0
        1 1 0 1 1 1 1 1 1 0
        1 1 0 0 0 0 4 0 0 0
        1 1 1 1 1 1 1 1 1 1
