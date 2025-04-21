"""
Este archivo sirve como un módulo común que contiene definiciones de estructuras de datos y f
unciones auxiliares que pueden ser utilizadas en diferentes partes del proyecto. Su propósito es centralizar y 
reutilizar código común para evitar duplicación y facilitar el mantenimiento.

Funciones:
    # Aquí se deben listar las funciones definidas en el módulo con una breve descripción de cada una.

Clases:
    # Aquí se deben listar las clases definidas en el módulo con una breve descripción de cada una.
"""

class Nodo:
    def __init__(self, posicion, costo=0, camino=None):
        self.posicion = posicion                    # Tupla (fila, columna) que representa la posición del nodo.
        self.costo = costo                          # Costo acumulado para llegar a este nodo.
        self.camino = camino or [posicion]          # Costo recorrido hasta el nodo.
        
    # Método para comparar nodos basados en su costo (para usar en la cola de prioridad).
    def __lt__(self, otro):
        return self.costo < otro.costo
    
def obtener_vecinos(posicion, mundo):
    """Obtiene las celdas adyacentes (arriba, abajo, izquierda, derecha) 
    que no sean obstáculos (valor 1) y que se encuentren dentro de la matriz."""

    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha.
    vecinos = []
    filas = len(mundo)
    columnas = len(mundo[0])
    for movimiento in movimientos:
        nueva_fila = posicion[0] + movimiento[0]
        nueva_columna = posicion[1] + movimiento[1]
        if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
            if mundo[nueva_fila][nueva_columna] != 1:  # No es un obstáculo.
                vecinos.append((nueva_fila, nueva_columna))
    return vecinos

def costo_movimiento(posicion, mundo):
    """Calcula el costo de moverse a una posición específica en el mundo.
    Si la celda tiene campo electromagnético (valor 3), el costo es 8; en otro caso, 1."""
    
    fila, col = posicion
    if mundo[fila][col] == 3:
        return 8
    return 1