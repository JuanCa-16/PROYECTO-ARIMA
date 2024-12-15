class Nodo:
    def __init__(self, tablero, movimiento=None):
        self.tablero = tablero  # Tablero del nodo
        self.movimiento = movimiento  # Movimiento realizado para llegar a este nodo
        self.hijos = []  # Lista de nodos hijos

class JuegoIA:
    def __init__(self, tablero):
        self.tablero = tablero  # El tablero inicial
        self.profundidad = 1  # Profundidad del árbol

    def generar_arbol(self, profundidad):
        """
        Genera el árbol de movimientos posibles para las piezas doradas hasta la profundidad dada.
        """
        raiz = Nodo(self.tablero)  # Nodo raíz con el tablero actual
        self._generar_hijos(raiz, profundidad)  # Llenar los nodos hijos

        return raiz  # Retorna la raíz del árbol con todos los hijos generados

    def _generar_hijos(self, nodo, profundidad):
        """
        Recursivamente genera los nodos hijos para el árbol hasta la profundidad dada.
        """
        if profundidad == 0:
            return

        # Obtener las piezas doradas (minúsculas)
        piezas_doradas = self.obtener_piezas_doradas(nodo.tablero)
        
        # Generar todas las combinaciones posibles de movimientos (1 a 4)
        for num_movimientos in range(1, 5):  # Número de movimientos en un turno
            combinaciones = self.generar_combinaciones_movimientos(piezas_doradas, num_movimientos)
            
            for combinacion in combinaciones:
                # Crear una copia del tablero
                nuevo_tablero = nodo.tablero
                
                # Realizar cada movimiento en la combinación
                movimientos_realizados = []
                for pieza, mov in combinacion:
                    nuevo_tablero = self.realizar_movimiento(nuevo_tablero, pieza, mov)
                    movimientos_realizados.append((pieza, mov))
                
                # Crear un nuevo nodo con el tablero actualizado
                nuevo_nodo = Nodo(nuevo_tablero, movimiento=movimientos_realizados)
                
                # Añadir el nuevo nodo como hijo del nodo actual
                nodo.hijos.append(nuevo_nodo)
                
                # Llamada recursiva para generar los hijos a la siguiente profundidad
                self._generar_hijos(nuevo_nodo, profundidad - 1)

    def obtener_piezas_doradas(self, tablero):
        """
        Encuentra todas las piezas doradas (minúsculas) en el tablero y las devuelve como una lista de posiciones.
        """
        piezas_doradas = []
        for i in range(8):
            for j in range(8):
                if tablero[i][j] in ['r', 'd', 'g', 'h', 'c', 'e']:  # Letras minúsculas
                    piezas_doradas.append((i, j))
        return piezas_doradas

    def obtener_movimientos_validos(self, tablero, pieza):
        """
        Obtiene los movimientos válidos para una pieza dorada (minúscula) en el tablero.
        """
        i, j = pieza
        movimientos = []
        
        # Asegúrate de que no salgas del tablero, por ejemplo solo mueves hacia arriba, abajo, izquierda, derecha
        posibles_movimientos = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
        
        for mov in posibles_movimientos:
            x, y = mov
            if 0 <= x < 8 and 0 <= y < 8 and tablero[x][y] == 0:  # El destino está vacío
                movimientos.append((x, y))
        
        return movimientos

    def realizar_movimiento(self, tablero, pieza, nueva_pos):
        """
        Realiza un movimiento en el tablero.
        """
        x, y = pieza
        nueva_x, nueva_y = nueva_pos
        
        # Copiar el tablero para no modificar el original
        tablero_copia = [fila.copy() for fila in tablero]
        
        # Realizamos el movimiento de la pieza
        tablero_copia[nueva_x][nueva_y] = tablero_copia[x][y]
        tablero_copia[x][y] = 0  # La casilla original queda vacía
        
        return tablero_copia

    def generar_combinaciones_movimientos(self, piezas, num_movimientos):
        """
        Genera todas las combinaciones posibles de movimientos para las piezas.
        """
        from itertools import permutations
        
        movimientos_combinaciones = []
        
        # Para cada combinación de piezas y movimientos
        for combinacion in permutations(piezas, num_movimientos):
            movimientos_validos = []
            for pieza in combinacion:
                movs = self.obtener_movimientos_validos(self.tablero, pieza)
                if movs:
                    movimientos_validos.append((pieza, movs[0]))  # Tomamos el primer movimiento válido
            movimientos_combinaciones.append(movimientos_validos)
        
        return movimientos_combinaciones

    def imprimir_tablero(self, tablero):
        """Imprime el tablero de manera legible en formato matriz."""
        for fila in tablero:
            print(' '.join(str(celda) if celda != 0 else '.' for celda in fila))

# Tablero de ejemplo (inicial)
tablero_inicial = [
    ['r', 'd', 'g', 'r', 'r', 'h', 'r', 'r'],
    ['g', 'h', 'e', 'd', 'r', 'r', 'r', 'c'],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    ['D', 'G', 'G', 'R', 'R', 'R', 'R', 'E'],
    ['R', 'R', 'R', 'D', 'H', 'H', 'R', 'C']
]

# Creamos una instancia de JuegoIA con el tablero inicial
juego_ia = JuegoIA(tablero_inicial)

# Generamos el árbol con profundidad 1
arbol = juego_ia.generar_arbol(1)

# Imprimimos los movimientos posibles (tableros hijos)


for hijo in arbol.hijos:
    print(f"Movimiento: {hijo.movimiento}")
    print("Tablero:")
    juego_ia.imprimir_tablero(hijo.tablero)  # Imprime el tablero de forma legible
    print("\n")  # Salto de línea entre movimientos
    
