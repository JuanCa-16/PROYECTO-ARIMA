def evaluate_board(board_status):
        """Evalúa el tablero asignando puntuaciones a las piezas."""
        piece_values = {
            "r": 1,  # Conejo dorado
            "d": 3,  # Perro dorado
            "g": 3,  # Gato dorado
            "h": 5,  # Caballo dorado
            "c": 7,  # Camello dorado
            "e": 9,  # Elefante dorado
            "R": -1,  # Conejo gris
            "D": -3,  # Perro gris
            "G": -3,  # Gato gris
            "H": -5,  # Caballo gris
            "C": -7,  # Camello gris
            "E": -9,  # Elefante gris
        }

        score = 0
        for piece in board_status.values():
            score += piece_values.get(piece, 0)
        return score


def get_valid_moves(board_status, piece, pos):
    """Genera todos los movimientos válidos para una pieza dada en una posición dada."""
    valid_moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha

    # Asegurarse de que pos es una tupla con dos valores
    if isinstance(pos, str) and len(pos) == 2:
        col = ord(pos[0]) - 65  # 'A' = 0, 'B' = 1, etc.
        row = 8 - int(pos[1])  # Fila del tablero
        pos = (col, row)
    elif not isinstance(pos, tuple) or len(pos) != 2:
        raise ValueError(f"Posición inválida: {pos}")

    x, y = pos

    for direction in directions:
        new_x = x + direction[0]
        new_y = y + direction[1]
        if 0 <= new_x < 8 and 0 <= new_y < 8:  # Dentro del tablero
            coordinate = f"{chr(65 + new_y)}{8 - new_x}"  # Corrige el orden de filas y columnas
            if board_status.get(coordinate, 0) == 0:  # Celda vacía, usa get para evitar KeyError
                valid_moves.append(coordinate)

    return valid_moves



def minimax(board_status, depth, maximizing_player):
    if depth == 0:
        return evaluate_board(board_status), None

    if not maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for pos, piece in board_status.items():
            if isinstance(piece, str) and piece.islower():  # Solo las piezas doradas (si son cadenas)
                valid_moves = get_valid_moves(board_status, piece, pos)
                for move in valid_moves:
                    new_board_status = board_status.copy()
                    new_board_status[move] = new_board_status.pop(pos)
                    eval, _ = minimax(new_board_status, depth - 1, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (pos, move)
        return max_eval, best_move
