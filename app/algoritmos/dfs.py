import time
from .modComun import Nodo, obtener_vecinos

def dfs(mundo, inicio, objetivo):
    """
    Realiza la búsqueda en profundidad evitando ciclos desde 'inicio' hasta 'objetivo'.
    Retorna el camino encontrado o None si no existe solución.
    """
    
    tiempo_inicio = time.time()
    nodos_expandidos = 0
    max_profundidad = 0
    
    pila = [Nodo(inicio)]  # Se usa una pila en lugar de una cola
    visitados = set()
    
    while pila:
        nodo_actual = pila.pop()  # Se extrae el último nodo (LIFO)
        nodos_expandidos += 1
        profundidad = len(nodo_actual.camino) - 1
        max_profundidad = max(max_profundidad, profundidad)
        
        if nodo_actual.posicion == objetivo:
            tiempo_total = time.time() - tiempo_inicio
            costo_total = sum(1 if mundo[vecino[0]][vecino[1]] != 3 else 8 for vecino in nodo_actual.camino[1:])
            return nodo_actual.camino, nodos_expandidos, max_profundidad, tiempo_total, costo_total
        
        if nodo_actual.posicion in visitados:
            continue
        visitados.add(nodo_actual.posicion)
        
        for vecino in obtener_vecinos(nodo_actual.posicion, mundo):
            if vecino not in visitados:
                nuevo_camino = nodo_actual.camino + [vecino]
                pila.append(Nodo(vecino, camino=nuevo_camino))  # Agrega a la pila

    tiempo_total = time.time() - tiempo_inicio
    return None  # No se encontró un camino
