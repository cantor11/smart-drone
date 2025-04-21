import time
import heapq
from .modComun import Nodo, obtener_vecinos, costo_movimiento

def astar(mundo, inicio, objetivo):
    """
    Realiza la búsqueda A* desde 'inicio' hasta 'objetivo'.
    Combina el costo acumulado (g) con la heurística (h).
    """
    tiempo_inicio = time.time()
    nodos_expandidos = 0
    max_profundidad = 0

    heuristica = lambda pos: abs(pos[0] - objetivo[0]) + abs(pos[1] - objetivo[1])

    cola = []
    nodo_inicial = Nodo(inicio)
    heapq.heappush(cola, (heuristica(inicio), nodo_inicial))

    visitados = set()

    while cola:
        _, nodo_actual = heapq.heappop(cola)
        nodos_expandidos += 1
        profundidad = len(nodo_actual.camino) - 1
        max_profundidad = max(max_profundidad, profundidad)

        if nodo_actual.posicion == objetivo:
            tiempo_total = time.time() - tiempo_inicio
            costo_total = nodo_actual.costo
            return nodo_actual.camino, nodos_expandidos, max_profundidad, tiempo_total, costo_total

        if nodo_actual.posicion in visitados:
            continue
        visitados.add(nodo_actual.posicion)

        for vecino in obtener_vecinos(nodo_actual.posicion, mundo):
            if vecino not in visitados:
                nuevo_costo = nodo_actual.costo + costo_movimiento(vecino, mundo)
                nuevo_camino = nodo_actual.camino + [vecino]
                f = nuevo_costo + heuristica(vecino)
                heapq.heappush(cola, (f, Nodo(vecino, nuevo_costo, nuevo_camino)))

    tiempo_total = time.time() - tiempo_inicio
    return None
