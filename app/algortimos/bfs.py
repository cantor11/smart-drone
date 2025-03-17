import time
from collections import deque
from .modComun import Nodo, obtener_vecinos

def bfs(mundo, inicio, objetivo):
    """
    Realiza la búsqueda en anchura desde 'inicio' hasta 'objetivo'.
    Retorna el camino encontrado o None si no existe solución.
    """
    
    tiempo_inicio = time.time()  # Tiempo de inicio de la búsqueda
    nodos_expandidos = 0  # Contador de nodos expandidos
    max_profundidad = 0  # Profundidad máxima alcanzada
    
    cola = deque([Nodo(inicio)])  
    visitados = set()  # Conjunto de posiciones visitadas
    
    while cola:
        nodo_actual = cola.popleft()
        nodos_expandidos += 1   # Incrementa el contador de nodos expandidos
        profundidad = len(nodo_actual.camino) - 1 # Profundidad del nodo actual
        max_profundidad = max(max_profundidad, profundidad) # Actualiza la profundidad máxima
        
        if nodo_actual.posicion == objetivo:
            tiempo_total = time.time() - tiempo_inicio  # Tiempo total de la búsqueda
            # Se calcula el costo sumando 1 o 8 según la celda (opcional)
            costo_total = sum(1 if mundo[vecino[0]][vecino[1]] != 3 else 8 for vecino in nodo_actual.camino[1:])
            return nodo_actual.camino, nodos_expandidos, max_profundidad, tiempo_total, costo_total  # Retorna el camino encontrado y las métricas
        
        if nodo_actual.posicion in visitados:
            continue   # Ignora nodos ya visitados
        visitados.add(nodo_actual.posicion)
        
        for vecino in obtener_vecinos(nodo_actual.posicion, mundo):
            if vecino not in visitados:
                nuevo_camino = nodo_actual.camino + [vecino]
                cola.append(Nodo(vecino, camino=nuevo_camino))

    tiempo_total = time.time() - tiempo_inicio 
    return None  # No se encontró un camino hacia el objetivo