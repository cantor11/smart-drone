import time
from collections import deque
from .modComun import Nodo, obtener_vecinos

def bfs(mundo, inicio, objetivo):

    tiempo_inicio = time.time()  # Tiempo de inicio de la búsqueda
    nodos_expandidos = 0  # Contador de nodos expandidos
    max_profundidad = 0  # Profundidad máxima alcanzada

    # Cola para almacenar los nodos por explorar (FIFO)
    cola = deque([Nodo(inicio)])
    visitados = set()  # Conjunto de posiciones visitadas para evitar visitar el mismo nodo varias veces

    while cola:
        nodo_actual = cola.popleft()
        nodos_expandidos += 1

        # Calcular la profundidad actual
        profundidad = len(nodo_actual.camino) - 1       # Profundidad del nodo actual
        max_profundidad = max(max_profundidad, profundidad)  # Actualizar la profundidad máxima

        # Si llegamos al objetivo, retornamos resultados
        if nodo_actual.posicion == objetivo:
            tiempo_total = time.time() - tiempo_inicio  # Tiempo total de la búsqueda
            # Calcular el costo considerando zonas de peligro (3) como costo 8
            costo_total = sum(1 if mundo[vecino[0]][vecino[1]] != 3 else 8 for vecino in nodo_actual.camino[1:])
            return nodo_actual.camino, nodos_expandidos, max_profundidad, tiempo_total, costo_total     # Retorna el camino encontrado y las métricas

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