import time
import heapq
from .modComun import Nodo, obtener_vecinos

def gbfs(mundo, inicio, objetivo):
    """
    Realiza la búsqueda avara (Greedy Best-First Search) desde 'inicio' hasta 'objetivo'.
    Retorna el camino encontrado o None si no existe solución.
    """
    
    tiempo_inicio = time.time()  # Tiempo de inicio de la búsqueda
    nodos_expandidos = 0  # Contador de nodos expandidos
    max_profundidad = 0  # Profundidad máxima alcanzada

    # Función heurística (distancia Manhattan)
    heuristica = lambda pos: abs(pos[0] - objetivo[0]) + abs(pos[1] - objetivo[1])

    # Cola de prioridad (Heap) con nodos ordenados por heurística
    cola = []
    heapq.heappush(cola, (heuristica(inicio), Nodo(inicio)))  

    visitados = set()  # Conjunto de posiciones visitadas

    while cola:
        _, nodo_actual = heapq.heappop(cola)
        nodos_expandidos += 1  # Incrementa el contador de nodos expandidos
        profundidad = len(nodo_actual.camino) - 1  # Profundidad del nodo actual
        max_profundidad = max(max_profundidad, profundidad)  # Actualiza la profundidad máxima

        if nodo_actual.posicion == objetivo:
            tiempo_total = time.time() - tiempo_inicio  # Tiempo total de la búsqueda
            costo_total = sum(1 if mundo[vecino[0]][vecino[1]] != 3 else 8 for vecino in nodo_actual.camino[1:])
            return nodo_actual.camino, nodos_expandidos, max_profundidad, tiempo_total, costo_total

        if nodo_actual.posicion in visitados:
            continue  # Ignora nodos ya visitados
        visitados.add(nodo_actual.posicion)

        for vecino in obtener_vecinos(nodo_actual.posicion, mundo):
            if vecino not in visitados:
                nuevo_camino = nodo_actual.camino + [vecino]
                heapq.heappush(cola, (heuristica(vecino), Nodo(vecino, camino=nuevo_camino)))

    tiempo_total = time.time() - tiempo_inicio  
    return None  # No se encontró un camino hacia el objetivo
