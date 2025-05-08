import pygame
import time
import os
from itertools import permutations
from algoritmos.bfs import bfs
from algoritmos.ucs import ucs 
from algoritmos.dfs import dfs
from algoritmos.gbfs import gbfs
from algoritmos.astar import astar
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

        # Limpiar cualquier dron anterior en la matriz
        for i in range(FILAS):
            for j in range(COLUMNAS):
                if self.mundo[i][j] == 2:
                    self.mundo[i][j] = 0

        # Recorrer el camino paso a paso
        for idx, (i, j) in enumerate(self.camino):
            # Si en la posición hay un paquete (valor 4), limpiarlo
            if self.mundo[i][j] == 4:
                self.mundo[i][j] = 0

            # Colocar el dron
            self.mundo[i][j] = 2

            # Redibujar la pantalla
            self.pantalla.fill((240, 240, 240))
            self.dibujar_matriz()
            pygame.display.flip()
            time.sleep(0.5)

            # Limpiar la posición actual para el siguiente paso (excepto al final)
            if idx != len(self.camino) - 1:
                self.mundo[i][j] = 0


def calcular_camino(mundo, algoritmo):
    FILAS = len(mundo)
    COLUMNAS = len(mundo[0]) if FILAS > 0 else 0

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
                inicio = (i, j)
                break
        if inicio:
            break

    if inicio is None:
        print("No se encontró el punto de inicio.")
        return [], {}

    posicion_actual = inicio

    if algoritmo in ["Costo uniforme", "A*", "Amplitud", "Profundidad", "Avara"]:
        paquetes = [(i, j) for i in range(FILAS) for j in range(COLUMNAS) if mundo[i][j] == 4]

        mejor_camino_global = None
        mejor_metricas = None
        mejor_costo_total = float('inf')

        for orden in permutations(paquetes):
            pos_actual = inicio
            camino_temp = []
            nodos_temp = 0
            profundidad_temp = 0
            tiempo_temp = 0
            costo_temp = 0
            mundo_copia = [fila[:] for fila in mundo]
            exito = True
            
            for objetivo in orden:
                if algoritmo == "Costo uniforme":
                    camino, nodos, profundidad, tiempo, costo = ucs(mundo_copia, pos_actual, objetivo)
                elif algoritmo == "A*":
                    camino, nodos, profundidad, tiempo, costo = astar(mundo_copia, pos_actual, objetivo)
                elif algoritmo == "Amplitud":
                    camino, nodos, profundidad, tiempo, costo = bfs(mundo_copia, pos_actual, objetivo)
                elif algoritmo == "Profundidad":
                    camino, nodos, profundidad, tiempo, costo = dfs(mundo_copia, pos_actual, objetivo)
                elif algoritmo == "Avara":
                    camino, nodos, profundidad, tiempo, costo = gbfs(mundo_copia, pos_actual, objetivo)
                else:
                    continue
                if camino is None:
                    exito = False
                    break
                if camino_temp:
                    camino_temp.extend(camino[1:])
                else:
                    camino_temp.extend(camino)
                nodos_temp += nodos
                tiempo_temp += tiempo
                profundidad_temp = max(profundidad_temp, profundidad)
                costo_temp += costo
                i_obj, j_obj = objetivo
                mundo_copia[i_obj][j_obj] = 0
                pos_actual = objetivo

            if exito and costo_temp < mejor_costo_total:
                mejor_costo_total = costo_temp
                mejor_camino_global = camino_temp
                mejor_metricas = {
                    "nodos_expandidos": nodos_temp,
                    "profundidad_arbol": profundidad_temp,
                    "tiempo_computo": tiempo_temp,
                    "costo_solucion": costo_temp
                }
                
        if mejor_camino_global:
            return mejor_camino_global, mejor_metricas
        else:
            print("No se encontró un camino completo a todos los paquetes.")
            return [], {}


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