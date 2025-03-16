import pygame
import time
import os

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
    def __init__(self, mundo):
        self.mundo = mundo
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
            self.pantalla.fill((240, 240, 240))  # Fondo gris claro
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

def iniciar_simulacion(mundo):
    """Inicia la simulación con la matriz cargada."""
    simulacion = SimulacionDron(mundo)
    simulacion.ejecutar_simulacion()