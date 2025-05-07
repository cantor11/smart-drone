import time
import heapq
from .modComun import Nodo, obtener_vecinos

def gbfs(mundo, inicio, objetivo):
    """
    Realiza la búsqueda avara (Greedy Best-First Search) desde 'inicio' hasta 'objetivo'.
    En esta estrategia, el dron se mueve siempre hacia el nodo que parece más cercano al objetivo
    según una heurística (distancia Manhattan), sin considerar el costo real de los movimientos.

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
            - costo_total (int): Costo total del camino encontrado (sumando costos de celdas peligrosas y normales).
    """

    tiempo_inicio = time.time()  # Tiempo inicial de la búsqueda
    nodos_expandidos = 0
    max_profundidad = 0

    # Heurística: distancia Manhattan (|x1 - x2| + |y1 - y2|)
    heuristica = lambda pos: abs(pos[0] - objetivo[0]) + abs(pos[1] - objetivo[1])

    # Cola de prioridad: ordenada solo por heurística
    cola = []
    heapq.heappush(cola, (heuristica(inicio), Nodo(inicio)))

    visitados = set()  # Posiciones visitadas

    while cola:
        # Extraer el nodo con menor heurística
        _, nodo_actual = heapq.heappop(cola)
        nodos_expandidos += 1

        # Calcular profundidad actual
        profundidad = len(nodo_actual.camino) - 1
        max_profundidad = max(max_profundidad, profundidad)

        # Si llegamos al objetivo
        if nodo_actual.posicion == objetivo:
            tiempo_total = time.time() - tiempo_inicio
            # Calcular el costo real del camino encontrado (1 para normal, 8 para peligros)
            costo_total = sum(1 if mundo[vecino[0]][vecino[1]] != 3 else 8 for vecino in nodo_actual.camino[1:])
            return nodo_actual.camino, nodos_expandidos, max_profundidad, tiempo_total, costo_total

        if nodo_actual.posicion in visitados:
            continue

        visitados.add(nodo_actual.posicion)

        # Expandir vecinos válidos
        for vecino in obtener_vecinos(nodo_actual.posicion, mundo):
            if vecino not in visitados:
                nuevo_camino = nodo_actual.camino + [vecino]
                heapq.heappush(cola, (heuristica(vecino), Nodo(vecino, camino=nuevo_camino)))

    # No se encontró solución
    tiempo_total = time.time() - tiempo_inicio
    return None