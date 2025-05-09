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



# ------------------------------------------------------------------
# Diccionario para invocar los algoritmos sin duplicar condicionales
# ------------------------------------------------------------------
BUSCADORES = {
    "Costo uniforme": ucs,
    "A*": astar,
    "Amplitud": bfs,
    "Profundidad": dfs,
    "Avara": gbfs,
}

def calcular_camino(mundo, algoritmo):
    FILAS = len(mundo)
    COLUMNAS = len(mundo[0]) if FILAS else 0

    # ---------------------------------------------------------------
    # 1. Buscar punto de inicio (valor 2)
    # ---------------------------------------------------------------
    inicio = next(((i, j) for i in range(FILAS)
                   for j in range(COLUMNAS) if mundo[i][j] == 2), None)
    if inicio is None:
        print("No se encontró el punto de inicio.")
        return [], {}

    # ---------------------------------------------------------------
    # 2. Obtener posiciones de todos los paquetes (valor 4)
    # ---------------------------------------------------------------
    paquetes = [(i, j) for i in range(FILAS)
                for j in range(COLUMNAS) if mundo[i][j] == 4]
    if not paquetes:
        print("No hay paquetes que recoger.")
        return [], {}

    # ---------------------------------------------------------------
    # 3. Elegir estrategia según algoritmo
    # ---------------------------------------------------------------
    if algoritmo in ("Costo uniforme", "A*"):
        # -----------------------------------------------------------
        # Estrategia exhaus­tiva: probar todas las permutaciones
        # -----------------------------------------------------------
        mejor_camino = None
        mejor_metricas = None
        mejor_costo   = float('inf')

        for orden in permutations(paquetes):
            camino_tmp, metricas_tmp = _recorre_en_orden(
                mundo, inicio, orden, algoritmo)
            if camino_tmp and metricas_tmp["costo_solucion"] < mejor_costo:
                mejor_camino   = camino_tmp
                mejor_metricas = metricas_tmp
                mejor_costo    = metricas_tmp["costo_solucion"]

        if mejor_camino:
            return mejor_camino, mejor_metricas
        print("No se encontró un camino completo a todos los paquetes.")
        return [], {}

    else:
        # -----------------------------------------------------------
        # Estrategia rápida: ir tomando el primer paquete hallado
        # -----------------------------------------------------------
        camino, metricas = _recorre_secuencial(
            mundo, inicio, algoritmo)
        return camino, metricas


# ------------------------------------------------------------------
# Función auxiliar: recorre un conjunto de paquetes en un orden dado
# ------------------------------------------------------------------
def _recorre_en_orden(mundo, inicio, orden, algoritmo):
    mundo_copia = [fila[:] for fila in mundo]
    pos_actual  = inicio

    camino_total = []
    nodos_totales, tiempo_total, profundidad_max, costo_total = 0, 0, 0, 0

    buscador = BUSCADORES[algoritmo]

    for objetivo in orden:
        camino, nodos, profundidad, tiempo, costo = buscador(
            mundo_copia, pos_actual, objetivo)

        if camino is None:
            return None, {}

        camino_total.extend(camino if not camino_total else camino[1:])
        nodos_totales   += nodos
        tiempo_total    += tiempo
        profundidad_max = max(profundidad_max, profundidad)
        costo_total     += costo

        i, j = objetivo
        mundo_copia[i][j] = 0          # Marcar paquete recogido
        pos_actual = objetivo

    metricas = {
        "nodos_expandidos": nodos_totales,
        "profundidad_arbol": profundidad_max,
        "tiempo_computo": tiempo_total,
        "costo_solucion": costo_total,
    }
    return camino_total, metricas


# ------------------------------------------------------------------
# Función auxiliar: estrategia rápida (primera posición con 4)
# ------------------------------------------------------------------
def _recorre_secuencial(mundo, inicio, algoritmo):
    FILAS = len(mundo)
    COLUMNAS = len(mundo[0])
    pos_actual = inicio
    camino_total = []
    nodos_totales, tiempo_total, profundidad_max, costo_total = 0, 0, 0, 0

    buscador = BUSCADORES[algoritmo]

    while any(4 in fila for fila in mundo):
        # Buscar el primer paquete restante
        objetivo = next(((i, j) for i in range(FILAS)
                         for j in range(COLUMNAS) if mundo[i][j] == 4), None)
        print("Buscando paquete en:", objetivo)
        if objetivo is None:
            break

        camino, nodos, profundidad, tiempo, costo = buscador(
            mundo, pos_actual, objetivo)

        if camino is None:
            print("No se encontró un camino al paquete", objetivo)
            break

        # Recorre el camino y recoge paquetes en el trayecto
        for idx, (i, j) in enumerate(camino):
            if mundo[i][j] == 4:
                print(f"Recogido paquete en: ({i}, {j})")
                mundo[i][j] = 0
        # Evita repetir la posición inicial si ya está en el camino_total
        camino_total.extend(camino if not camino_total else camino[1:])
        nodos_totales += nodos
        tiempo_total += tiempo
        profundidad_max = max(profundidad_max, profundidad)
        costo_total += costo

        pos_actual = objetivo

    metricas = {
        "nodos_expandidos": nodos_totales,
        "profundidad_arbol": profundidad_max,
        "tiempo_computo": tiempo_total,
        "costo_solucion": costo_total,
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