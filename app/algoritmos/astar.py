import time
import heapq
from .modComun import Nodo, obtener_vecinos, costo_movimiento

def astar(mundo, inicio, objetivo):
    tiempo_inicio = time.time()
    nodos_expandidos = 0
    max_profundidad = 0

    # Heurística: distancia Manhattan
    heuristica = lambda pos: abs(pos[0] - objetivo[0]) + abs(pos[1] - objetivo[1])

    # Cola de prioridad: (f(n), Nodo)
    cola = []
    nodo_inicial = Nodo(inicio)
    heapq.heappush(cola, (heuristica(inicio), nodo_inicial))

    visitados = {}  # Mapea posición → menor costo encontrado

    while cola:
        _, nodo_actual = heapq.heappop(cola)
        nodos_expandidos += 1

        profundidad = len(nodo_actual.camino) - 1
        max_profundidad = max(max_profundidad, profundidad)

        if nodo_actual.posicion == objetivo:
            tiempo_total = time.time() - tiempo_inicio
            return nodo_actual.camino, nodos_expandidos, max_profundidad, tiempo_total, nodo_actual.costo

        pos_actual = nodo_actual.posicion
        costo_actual = nodo_actual.costo

        # Si ya se visitó con menor costo, ignorar
        if pos_actual in visitados and visitados[pos_actual] <= costo_actual:
            continue

        visitados[pos_actual] = costo_actual

        for vecino in obtener_vecinos(pos_actual, mundo):
            nuevo_costo = costo_actual + costo_movimiento(vecino, mundo)
            if vecino not in visitados or nuevo_costo < visitados.get(vecino, float('inf')):
                nuevo_camino = nodo_actual.camino + [vecino]
                f = nuevo_costo + heuristica(vecino)
                heapq.heappush(cola, (f, Nodo(vecino, nuevo_costo, nuevo_camino)))

    # Si no se encuentra un camino
    tiempo_total = time.time() - tiempo_inicio
    return None, nodos_expandidos, max_profundidad, tiempo_total, float('inf')
import time
import heapq
from .modComun import Nodo, obtener_vecinos, costo_movimiento

def astar(mundo, inicio, objetivo):
    """
    Realiza la búsqueda A* (A estrella) desde 'inicio' hasta 'objetivo'.

    A* combina el costo acumulado real (g) con una estimación heurística (h) 
    del costo restante para alcanzar el objetivo, usando la heurística de distancia Manhattan.

    Args:
        mundo (list of list): Matriz que representa el entorno (0: vacío, 1: obstáculo, 3: peligro, 4: paquete).
        inicio (tuple): Posición inicial (fila, columna) del dron.
        objetivo (tuple): Posición objetivo (fila, columna).

    Returns:
        tuple: (camino, nodos_expandidos, max_profundidad, tiempo_total, costo_total)
            - camino (list): Lista de posiciones (tuplas) del camino encontrado.
            - nodos_expandidos (int): Número de nodos expandidos durante la búsqueda.
            - max_profundidad (int): Profundidad máxima alcanzada.
            - tiempo_total (float): Tiempo de ejecución en segundos.
            - costo_total (int): Costo total del camino encontrado.
    """

    # Tiempo inicial para medir el rendimiento
    tiempo_inicio = time.time()
    nodos_expandidos = 0
    max_profundidad = 0

    # Definición de la heurística: distancia de Manhattan
    heuristica = lambda pos: abs(pos[0] - objetivo[0]) + abs(pos[1] - objetivo[1])

    # Cola de prioridad: (f(n), nodo)
    cola = []
    nodo_inicial = Nodo(inicio)
    heapq.heappush(cola, (heuristica(inicio), nodo_inicial))

    visitados = set()

    while cola:
        # Extrae el nodo con menor costo f(n) = g(n) + h(n)
        _, nodo_actual = heapq.heappop(cola)
        nodos_expandidos += 1

        # Calcula profundidad del nodo actual
        profundidad = len(nodo_actual.camino) - 1
        max_profundidad = max(max_profundidad, profundidad)

        # Verificar si alcanzamos el objetivo
        if nodo_actual.posicion == objetivo:
            tiempo_total = time.time() - tiempo_inicio
            costo_total = nodo_actual.costo
            return nodo_actual.camino, nodos_expandidos, max_profundidad, tiempo_total, costo_total

        if nodo_actual.posicion in visitados:
            continue

        visitados.add(nodo_actual.posicion)

        # Expandir vecinos válidos
        for vecino in obtener_vecinos(nodo_actual.posicion, mundo):
            if vecino not in visitados:
                nuevo_costo = nodo_actual.costo + costo_movimiento(vecino, mundo)
                nuevo_camino = nodo_actual.camino + [vecino]
                f = nuevo_costo + heuristica(vecino)  # f(n) = g(n) + h(n)
                heapq.heappush(cola, (f, Nodo(vecino, nuevo_costo, nuevo_camino)))

    # Si no se encontró solución
    tiempo_total = time.time() - tiempo_inicio
    return None