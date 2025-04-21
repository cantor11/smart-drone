import time
from collections import deque
from .modComun import Nodo, obtener_vecinos

def bfs(mundo, inicio, objetivo):
    """
    Realiza la búsqueda en anchura (BFS: Breadth-First Search) desde 'inicio' hasta 'objetivo'.
    Esta estrategia explora todos los nodos a una misma profundidad antes de avanzar a la siguiente.
    Es óptima en términos de número de pasos si los costos de movimiento son iguales.

    Args:
        mundo (list of list): Matriz que representa el entorno (0: vacío, 1: obstáculo, 3: peligro, 4: paquete).
        inicio (tuple): Posición inicial (fila, columna) del dron.
        objetivo (tuple): Posición objetivo (fila, columna).

    Returns:
        tuple: (camino, nodos_expandidos, max_profundidad, tiempo_total, costo_total)
            - camino (list): Lista de posiciones (tuplas) del camino encontrado.
            - nodos_expandidos (int): Número de nodos expandidos durante la búsqueda.
            - max_profundidad (int): Profundidad máxima alcanzada en el árbol de búsqueda.
            - tiempo_total (float): Tiempo de ejecución de la búsqueda en segundos.
            - costo_total (int): Costo total del camino recorrido, considerando zonas peligrosas.
    """

    tiempo_inicio = time.time()  # Inicio de la medición de tiempo
    nodos_expandidos = 0  # Contador de nodos expandidos
    max_profundidad = 0  # Profundidad máxima alcanzada

    # Cola para almacenar los nodos por explorar (FIFO)
    cola = deque([Nodo(inicio)])
    visitados = set()  # Para evitar visitar el mismo nodo varias veces

    while cola:
        nodo_actual = cola.popleft()
        nodos_expandidos += 1

        # Calcular la profundidad actual
        profundidad = len(nodo_actual.camino) - 1
        max_profundidad = max(max_profundidad, profundidad)

        # Si llegamos al objetivo, retornamos resultados
        if nodo_actual.posicion == objetivo:
            tiempo_total = time.time() - tiempo_inicio
            # Calcular el costo considerando zonas de peligro (3) como costo 8
            costo_total = sum(1 if mundo[vecino[0]][vecino[1]] != 3 else 8 for vecino in nodo_actual.camino[1:])
            return nodo_actual.camino, nodos_expandidos, max_profundidad, tiempo_total, costo_total

        # Si ya visitamos este nodo, lo ignoramos
        if nodo_actual.posicion in visitados:
            continue
        visitados.add(nodo_actual.posicion)

        # Expandir vecinos
        for vecino in obtener_vecinos(nodo_actual.posicion, mundo):
            if vecino not in visitados:
                nuevo_camino = nodo_actual.camino + [vecino]
                cola.append(Nodo(vecino, camino=nuevo_camino))

    # No se encontró un camino válido
    tiempo_total = time.time() - tiempo_inicio
    return None