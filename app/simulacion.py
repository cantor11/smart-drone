import pygame
import time
import os
from algortimos.bfs import bfs
import copy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Constantes de la matriz
DIMENSION_CELDA = 50
FILAS, COLUMNAS = 10, 10
COLORES = {
    "vacio": (255, 255, 255),  # Espacio vacío (blanco)
    "obstaculo": (0, 0, 0)     # Obstáculo (negro)
}

# Rutas de imágenes
RUTAS_IMAGENES = {
    "dron": os.path.join(BASE_DIR, "assets", "imagenes", "dron.png"),
    "caja": os.path.join(BASE_DIR, "assets", "imagenes", "caja.png"),
    "peligro": os.path.join(BASE_DIR, "assets", "imagenes", "precaucion.png")
}

class SimulacionDron:
    def __init__(self, mundo, camino=None):
        self.mundo = mundo
        self.camino = camino    # Camino calculado (lista de posiciones) que seguirá el dron
        self.ejecutando = True

        # Inicializar Pygame y cargar imágenes
        pygame.init()
        self.pantalla = pygame.display.set_mode((COLUMNAS * DIMENSION_CELDA, FILAS * DIMENSION_CELDA))
        pygame.display.set_caption("Smart Drone")

        # Cambiar el ícono de la ventana
        icono = pygame.image.load(RUTAS_IMAGENES["dron"])
        pygame.display.set_icon(icono)

        # Cargar imágenes y escalarlas
        self.img_dron = pygame.image.load(RUTAS_IMAGENES["dron"])
        self.img_dron = pygame.transform.scale(self.img_dron, (DIMENSION_CELDA, DIMENSION_CELDA))

        self.img_caja = pygame.image.load(RUTAS_IMAGENES["caja"])
        self.img_caja = pygame.transform.scale(self.img_caja, (DIMENSION_CELDA, DIMENSION_CELDA))

        self.img_peligro = pygame.image.load(RUTAS_IMAGENES["peligro"])
        self.img_peligro = pygame.transform.scale(self.img_peligro, (DIMENSION_CELDA, DIMENSION_CELDA))

    def ejecutar_simulacion(self):
        """Inicia la ventana de Pygame y muestra la animación."""
        while self.ejecutando:
            self.pantalla.fill((220, 220, 220))  # Fondo gris claro
            self.dibujar_matriz()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.ejecutando = False

            pygame.display.flip()
            time.sleep(0.1)  # Pequeña pausa para animación

        pygame.quit()

    def dibujar_matriz(self):
        """Dibuja la cuadrícula y coloca imágenes en la pantalla."""
        for i in range(FILAS):
            for j in range(COLUMNAS):
                x, y = j * DIMENSION_CELDA, i * DIMENSION_CELDA

                if self.mundo[i][j] == 1:
                    pygame.draw.rect(self.pantalla, COLORES["obstaculo"], (x, y, DIMENSION_CELDA, DIMENSION_CELDA))  # Obstáculo (negro)
                elif self.mundo[i][j] == 2:
                    self.pantalla.blit(self.img_dron, (x, y))  # Dron 
                elif self.mundo[i][j] == 3:
                    self.pantalla.blit(self.img_peligro, (x, y))  # Zona peligrosa 
                elif self.mundo[i][j] == 4:
                    self.pantalla.blit(self.img_caja, (x, y))  # Caja 

                pygame.draw.rect(self.pantalla, (0, 0, 0), (x, y, DIMENSION_CELDA, DIMENSION_CELDA), 1)  # Borde negro

    def animar_camino(self):
        """Anima el dron moviéndose a lo largo del camino calculado."""
        if not self.camino:
            print("No se ha calculado un camino.")
            return
        
        # Remover la posición inicial del dron (valor 2) para evitar superposición
        inicio = None
        for i in range(FILAS):
            for j in range(COLUMNAS):
                if self.mundo[i][j] == 2:
                    inicio = (i, j)
                    self.mundo[i][j] = 0  # Limpiar la posición inicial del dron
                    break
            if inicio:
                break
            
        # Iterar sobre cada posicion del camino
        for posicion in self.camino:
            i, j = posicion
            # Si en la posición hay un paquete (valor 4), se considera recogido y se limpia la celda
            if self.mundo[i][j] == 4:
                self.mundo[i][j] = 0  # Limpiar la posición del paquete
            # Colocar el dron en la nueva posición (valor 2)
            self.mundo[i][j] = 2
            
            # Actualizar la pantalla para mostrar el movimiento
            self.pantalla.fill((240, 240, 240))
            self.dibujar_matriz()
            pygame.display.flip()
            time.sleep(0.5)
            
            # Si no es la última posición, limpiar la celda actual para continuar la animación
            if posicion != self.camino[-1]:
                self.mundo[i][j] = 0

def calcular_camino(mundo, algoritmo):
    """
    Calcula un camino total que pase por todos los paquetes.
    Se parte de la posición inicial (valor 2) y, mientras existan paquetes (valor 4),
    se calcula la ruta al siguiente paquete usando el algoritmo seleccionado.
    """
    nodos_totales = 0
    profundidad_total = 0
    tiempo_total = 0
    costo_total = 0
    camino_total = []
    
    # Buscar la posición inicial del dron (valor 2)
    inicio = None
    for i in range(FILAS):
        for j in range(COLUMNAS):
            if mundo[i][j] == 2:
                inicio = (i, j)    # Posición inicial del dron
                break
        if inicio is not None:
            break
        
    posicion_actual = inicio
    # Mientras existan paquetes (valor 4), calcular la ruta al siguiente paquete
    while any(4 in fila for fila in mundo):
        objetivo = None
        # Buscar la posición del siguiente paquete (valor 4)
        for i in range(FILAS):
            for j in range(COLUMNAS):
                if mundo[i][j] == 4:
                    objetivo = (i, j)   # Posición del siguiente paquete
                    break
            if objetivo:
                break
            
        if objetivo is None:
            break    # No hay más paquetes, salir del bucle
        
        # Seleccionar el algoritmo de búsqueda
        if algoritmo == "Amplitud":
            # Calcular el camino con BFS
            camino, nodos, profundidad, tiempo, costo = bfs(mundo, posicion_actual, objetivo)
            
        # elif algoritmo == "Costo uniforme":
        #     # Calcular el camino con Costo uniforme
        #     camino, nodos, profundidad, tiempo, costo = ucs(mundo, posicion_actual, objetivo)
        # elif algoritmo == "Profundidad":  
        #     # Calcular el camino con DFS
        #     camino, nodos, profundidad, tiempo, costo = dfs(mundo, posicion_actual, objetivo)
        
        else:
            # Por defecto, usar BFS si no se selecciona ningún algoritmo
            camino, nodos, profundidad, tiempo, costo = bfs(mundo, posicion_actual, objetivo)  # Por defecto, usar BFS
            
        if camino is None:
            print("No se encontró un camino al siguiente paquete en", objetivo)
            break    # No se encontró un camino, salir del bucle
        
        # Acumular métricas (se suma nodos y tiempos, se toma el máximo de profundidad, y se suma costo si aplica)
        nodos_totales += nodos    # Sumar nodos visitados al total acumulado
        tiempo_total += tiempo    # Sumar tiempo transcurrido al total acumulado
        profundidad_total += max(profundidad_total, profundidad)   # Tomar el máximo de la profundidad
        if costo is not None:
            costo_total += costo
        
        # Evitar duplicar el nodo de partida en la concatenación
        if camino_total:
            camino_total.extend(camino[1:])    # Agregar el camino sin el primer nodo (duplicado)
        else:
            camino_total.extend(camino)    # Agregar el camino completo al camino total
            
        # Marcar el paquete como recogido (valor 0)
        i_objetivo, j_objetivo = objetivo
        mundo[i_objetivo][j_objetivo] = 0    # Marcar el paquete como recogido
        # Actualizar la posición actual del dron al final del camino calculado
        posicion_actual = objetivo
        
    metricas = {
        "nodos_expandidos": nodos_totales,
        "profundidad_arbol": profundidad_total,
        "tiempo_computo": tiempo_total,
        "costo_solucion": costo_total
    }
        
    return camino_total, metricas

def iniciar_simulacion(mundo, algoritmo):
    """
    Carga el mundo, y recibe el algoritmo a utilizar para la búsqueda del camino.
    Calcula el camino total para recoger todos los paquetes y ejecuta la simulación.
    """
    # Realiza una copia profunda de la matriz para la planificación del camino
    mundo_planificacion = copy.deepcopy(mundo)
    
    camino, metricas = calcular_camino(mundo_planificacion, algoritmo)
    print("Camino calculado:", camino)   
         
    # Crear la simulación pasando el mundo y el camino calculado
    simulacion = SimulacionDron(mundo, camino)
    simulacion.animar_camino()   # Animar el movimiento del dron
    simulacion.ejecutar_simulacion()
    
    return metricas
