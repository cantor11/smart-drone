import time
import heapq
from .modComun import Nodo, obtener_vecinos, costo_movimiento

def ucs(mundo, inicio, objetivo):
    """
    Implementación de la búsqueda de costo uniforme (UCS).
    Retorna el camino más barato dependiendo el costo del movimiento desde 'inicio' hasta 'objetivo'.
    """
    tiempo_inicio = time.time()
    nodos_expandidos = 0
    max_profundidad = 0

    # Cola de prioridad para explorar siempre el nodo con menor costo acumulado
    cola = []
    heapq.heappush(cola, Nodo(inicio, costo=0))

    visitados = {}  # Diccionario que almacena el menor costo conocido para cada posición

    while cola:
        nodo_actual = heapq.heappop(cola)
        nodos_expandidos += 1
        profundidad = len(nodo_actual.camino) - 1
        max_profundidad = max(max_profundidad, profundidad)

        # Si encontramos el objetivo, retornamos los datos
        if nodo_actual.posicion == objetivo:
            tiempo_total = time.time() - tiempo_inicio
            return nodo_actual.camino, nodos_expandidos, max_profundidad, tiempo_total, nodo_actual.costo

        # Si ya visitamos esta posición con un costo menor, la ignoramos
        if nodo_actual.posicion in visitados and visitados[nodo_actual.posicion] <= nodo_actual.costo:
            continue

        visitados[nodo_actual.posicion] = nodo_actual.costo

        # Expandimos los vecinos válidos
        for vecino in obtener_vecinos(nodo_actual.posicion, mundo):
            nuevo_costo = nodo_actual.costo + costo_movimiento(vecino, mundo)
            nuevo_camino = nodo_actual.camino + [vecino]
            heapq.heappush(cola, Nodo(vecino, nuevo_costo, nuevo_camino))

    # Si no hay camino al objetivo
    return None, nodos_expandidos, max_profundidad, time.time() - tiempo_inicio, None
