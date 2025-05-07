import time
import heapq
from .modComun import Nodo, obtener_vecinos, costo_movimiento

def ucs(mundo, inicio, objetivo):
    # Marcar el tiempo de inicio
    tiempo_inicio = time.time()
    nodos_expandidos = 0
    max_profundidad = 0

    # Inicializamos una cola de prioridad (heapq) para explorar siempre el nodo con menor costo
    cola = []
    heapq.heappush(cola, Nodo(inicio, costo=0))

    # Diccionario para almacenar el menor costo registrado para cada posición
    visitados = {}

    while cola:
        # Extraer el nodo de menor costo
        nodo_actual = heapq.heappop(cola)
        nodos_expandidos += 1

        # Actualizar profundidad máxima si es necesario
        profundidad = len(nodo_actual.camino) - 1
        max_profundidad = max(max_profundidad, profundidad)

        # Si llegamos al objetivo, retornamos resultados
        if nodo_actual.posicion == objetivo:
            tiempo_total = time.time() - tiempo_inicio
            return nodo_actual.camino, nodos_expandidos, max_profundidad, tiempo_total, nodo_actual.costo

        # Si ya hemos visitado esta posición con menor o igual costo, la ignoramos
        if nodo_actual.posicion in visitados and visitados[nodo_actual.posicion] <= nodo_actual.costo:
            continue

        # Registramos el costo actual para esta posición
        visitados[nodo_actual.posicion] = nodo_actual.costo

        # Expandimos los vecinos
        for vecino in obtener_vecinos(nodo_actual.posicion, mundo):
            nuevo_costo = nodo_actual.costo + costo_movimiento(vecino, mundo)
            nuevo_camino = nodo_actual.camino + [vecino]
            # Insertar el vecino en la cola de prioridad
            heapq.heappush(cola, Nodo(vecino, nuevo_costo, nuevo_camino))

    # Si terminamos y no encontramos camino al objetivo
    tiempo_total = time.time() - tiempo_inicio
    return None, nodos_expandidos, max_profundidad, tiempo_total, None
