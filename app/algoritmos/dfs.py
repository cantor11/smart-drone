import time
from .modComun import Nodo, obtener_vecinos

def dfs(mundo, inicio, objetivo):
    """
    Realiza la búsqueda en profundidad (Depth-First Search, DFS) evitando ciclos desde 'inicio' hasta 'objetivo'.
    
    Explora siempre el último nodo insertado primero (LIFO - Last In First Out), utilizando una pila.
    Retorna el primer camino encontrado al objetivo.

    Args:
        mundo (list of list): Matriz que representa el entorno (0: vacío, 1: obstáculo, 3: peligro, 4: paquete).
        inicio (tuple): Posición inicial del dron (fila, columna).
        objetivo (tuple): Posición objetivo (fila, columna).

    Returns:
        tuple: (camino, nodos_expandidos, max_profundidad, tiempo_total, costo_total)
            - camino (list): Lista de posiciones (tuplas) del camino encontrado.
            - nodos_expandidos (int): Número de nodos expandidos.
            - max_profundidad (int): Máxima profundidad alcanzada.
            - tiempo_total (float): Tiempo total de ejecución en segundos.
            - costo_total (int): Costo total del camino basado en el terreno (1 o 8 por casilla).
    """

    # Marcar tiempo de inicio de la búsqueda
    tiempo_inicio = time.time()
    nodos_expandidos = 0
    max_profundidad = 0

    # Inicializar pila con el nodo inicial
    pila = [Nodo(inicio)]
    visitados = set()

    while pila:
        # Sacar el último nodo de la pila
        nodo_actual = pila.pop()
        nodos_expandidos += 1

        # Calcular profundidad del nodo actual
        profundidad = len(nodo_actual.camino) - 1
        max_profundidad = max(max_profundidad, profundidad)

        # Verificar si hemos alcanzado el objetivo
        if nodo_actual.posicion == objetivo:
            tiempo_total = time.time() - tiempo_inicio
            # Cálculo de costo total basado en el recorrido
            costo_total = sum(1 if mundo[vecino[0]][vecino[1]] != 3 else 8 for vecino in nodo_actual.camino[1:])
            return nodo_actual.camino, nodos_expandidos, max_profundidad, tiempo_total, costo_total

        # Si ya visitamos esta posición, la ignoramos
        if nodo_actual.posicion in visitados:
            continue

        visitados.add(nodo_actual.posicion)

        # Expandir vecinos válidos no visitados
        for vecino in obtener_vecinos(nodo_actual.posicion, mundo):
            if vecino not in visitados:
                nuevo_camino = nodo_actual.camino + [vecino]
                pila.append(Nodo(vecino, camino=nuevo_camino))

    # Si no se encontró un camino, retornar None
    tiempo_total = time.time() - tiempo_inicio
    return None