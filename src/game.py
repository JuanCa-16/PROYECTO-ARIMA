import pygame
import os
import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board_size = 8  # Tablero principal de 8x8
        self.cell_size = 50  # Tamaño de cada celda en píxeles(70)
        self.margin = 20  # que tan pegado a la izq el tablero
        self.board = self.create_board()
        self.board_status = self.create_board_status()  # Tablero de estado inicial
        self.pieces = []
        self.initialize_pieces()

        # Cargar imágenes de las fichas grises
        assets_path = os.path.join(os.path.dirname(__file__), "..", "assets")
        self.piece_images = {
            "conejoGris": pygame.image.load(os.path.join(assets_path, "conejoGris.png")),
            "gatoGris": pygame.image.load(os.path.join(assets_path, "gatoGris.png")),
            "perroGris": pygame.image.load(os.path.join(assets_path, "perroGris.png")),
            "caballoGris": pygame.image.load(os.path.join(assets_path, "caballoGris.png")),
            "camelloGris": pygame.image.load(os.path.join(assets_path, "camelloGris.png")),
            "elefanteGris": pygame.image.load(os.path.join(assets_path, "elefanteGris.png")),
        }

        self.piece_images_gold = {
            "conejo": pygame.image.load(os.path.join(assets_path, "conejo.png")),
            "gato": pygame.image.load(os.path.join(assets_path, "gato.png")),
            "perro": pygame.image.load(os.path.join(assets_path, "perro.png")),
            "caballo": pygame.image.load(os.path.join(assets_path, "caballo.png")),
            "camello": pygame.image.load(os.path.join(assets_path, "camello.png")),
            "elefante": pygame.image.load(os.path.join(assets_path, "elefante.png")),
        }

        # Estado para arrastrar fichas
        self.selected_piece = None
        self.mouse_offset = (0, 0)

        # Configurar la fuente para mostrar las coordenadas
        self.font = pygame.font.SysFont('Arial', 10)

    def create_board(self):
        # Genera un diccionario con las coordenadas del tablero
        board = {}
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for row in range(self.board_size):
            for col in range(self.board_size):
                coordinate = f"{letters[col]}{self.board_size - row}"
                board[coordinate] = (col, row)
        return board

    def create_board_status(self):
        # Inicializa el estado del tablero con 0
        board_status = {}
        for key in self.board:
            board_status[key] = 0  # Representa celdas vacías
        return board_status

    def initialize_pieces(self):
        """Colocar las piezas iniciales en posiciones predeterminadas"""
        piece_names = ["conejo"] * 8 + ["perro", "perro", "gato", "gato", "caballo", "caballo", "elefante", "camello"]
        random.shuffle(piece_names)
        
        y_pos = self.margin + self.cell_size * 0  # En qué Y empieza las cartas
        for i, name in enumerate(piece_names[:8]):
            pos = (self.margin + i * self.cell_size, y_pos)
            self.pieces.append({"name": name, "pos": pos})
            # Actualizar el estado del tablero
            coordinate = f"{chr(65 + i)}{self.board_size - 0}"  # Posiciones A1, B1, ..., H1
            self.board_status[coordinate] = self.get_piece_initial(name)  # Usa la nueva función

        y_pos = self.margin + self.cell_size * 1
        for i, name in enumerate(piece_names[8:]):
            pos = (self.margin + i * self.cell_size, y_pos)
            self.pieces.append({"name": name, "pos": pos})
            # Actualizar el estado del tablero
            coordinate = f"{chr(65 + i)}{self.board_size - 1}"  # Posiciones A2, B2, ..., H2
            self.board_status[coordinate] = self.get_piece_initial(name)  # Usa la nueva función

        # Fichas grises fuera del tablero
        for i in range(8):
            pos = (self.margin + i * self.cell_size, self.margin + self.cell_size * (self.board_size + 0))
            self.pieces.append({"name": "conejoGris", "pos": pos})

        y_pos_gris = self.margin + self.cell_size * (self.board_size + 1)
        piece_names_gris = ["perroGris", "perroGris", "gatoGris", "gatoGris", "caballoGris", "caballoGris", "elefanteGris", "camelloGris"]
        
        for i, name in enumerate(piece_names_gris):
            pos = (self.margin + i * self.cell_size, y_pos_gris)
            self.pieces.append({"name": name, "pos": pos})

    def get_piece_initial(self, name):
        """Devuelve la inicial correspondiente para las fichas doradas y grises"""
        piece_initials_gold = {
            "conejo": "r",
            "caballo": "h",
            "perro": "d",
            "gato": "g",
            "camello": "c",
            "elefante": "e"
        }
        piece_initials_gris = {
            "conejoGris": "R",
            "caballoGris": "H",
            "perroGris": "D",
            "gatoGris": "G",
            "camelloGris": "C",
            "elefanteGris": "E"
        }
        
        if name in piece_initials_gold:
            return piece_initials_gold[name]
        elif name in piece_initials_gris:
            return piece_initials_gris[name]
        return 0  # Default si no se encuentra la pieza

    def print_board_status(self):
        # Imprimir el estado del tablero
        for row in range(self.board_size):
            row_state = ""
            for col in range(self.board_size):
                coordinate = f"{chr(65 + col)}{self.board_size - row}"
                row_state += f"{self.board_status[coordinate]} "  # Estado de cada celda
            print(row_state)

        print()

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for piece in reversed(self.pieces):
                    piece_rect = pygame.Rect(piece["pos"], (self.cell_size, self.cell_size))
                    if piece_rect.collidepoint(event.pos):
                        self.selected_piece = piece
                        self.mouse_offset = (event.pos[0] - piece["pos"][0], event.pos[1] - piece["pos"][1])
                        self.original_position = piece["pos"]  # Guardar la posición original
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.selected_piece:
                    # Calcular la celda a la que se intentará mover la pieza
                    mouse_x, mouse_y = event.pos
                    col = (mouse_x - self.margin) // self.cell_size
                    row = (mouse_y - self.margin) // self.cell_size

                    # Verificar si las coordenadas están dentro del tablero
                    if 0 <= col < self.board_size and 0 <= row < self.board_size:
                        x = self.margin + col * self.cell_size
                        y = self.margin + row * self.cell_size

                        # Obtener coordenada tipo A1 a partir de (col, row)
                        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                        coordinate = f"{letters[col]}{self.board_size - row}"  # 

                        # Verificar si la celda está ocupada
                        cell_occupied = any(p["pos"] == (x, y) for p in self.pieces)

                        if not cell_occupied:

                            # Primero, actualizar la celda anterior a 0 (vacía)
                            old_coordinate = f"{chr(65 + self.original_position[0] // self.cell_size)}{self.board_size - (self.original_position[1] // self.cell_size)}"
                            self.board_status[old_coordinate] = 0  # Celda vacía

                            # Mover la pieza a la nueva posición
                            self.selected_piece["pos"] = (x, y)
                            self.board_status[coordinate] = self.get_piece_initial(self.selected_piece["name"])  # Usar la nueva función
                            self.print_board_status()  # Imprimir el estado del tablero
                        else:
                            # Celda ocupada: devolver a la posición original
                            self.selected_piece["pos"] = self.original_position
                            print(f"Celda ocupada: {coordinate}. No se puede mover la pieza.")
                            print(f"Celda ocupada: ({row}, {col}). No se puede mover la pieza.")
                            self.print_board_status()  # Imprimir el estado del tablero
                    else:
                        # Movimiento fuera del tablero: devolver a la posición original
                        self.selected_piece["pos"] = self.original_position
                        print("Intento de mover fuera del tablero.")
                        self.print_board_status()  # Imprimir el estado del tablero

                    # Resetear la pieza seleccionada y posición original
                    self.selected_piece = None
                    self.original_position = None

        elif event.type == pygame.MOUSEMOTION:
            if self.selected_piece:
                # Actualizar la posición de la pieza mientras se arrastra
                self.selected_piece["pos"] = (event.pos[0] - self.mouse_offset[0], event.pos[1] - self.mouse_offset[1])

    def draw(self):
        """Dibujar el tablero y las piezas"""
        # Coordenadas específicas que deben ser azules
        blue_coordinates = ["C3", "F3", "C6", "F6"]

        # Dibujar el tablero principal
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = self.margin + col * self.cell_size
                y = self.margin + row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                # Obtener la coordenada de la celda
                coordinate = list(self.board.keys())[row * self.board_size + col]

                # Verificar si la celda coincide con una de las coordenadas azules
                if coordinate in blue_coordinates:
                    pygame.draw.rect(self.screen, (189, 210, 219), rect)  # Azul
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)  # Blanco

                pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

                text = self.font.render(coordinate, True, (0, 0, 0))
                self.screen.blit(text, (x + self.cell_size - text.get_width() - 5, y + self.cell_size - text.get_height() - 5))

        # Dibujar todas las piezas
        for piece in self.pieces:
            image = self.piece_images.get(piece["name"]) or self.piece_images_gold.get(piece["name"])
            if image:
                scaled_image = pygame.transform.scale(image, (self.cell_size - 10, self.cell_size - 10))
                x_offset = (self.cell_size - scaled_image.get_width()) // 2
                y_offset = (self.cell_size - scaled_image.get_height()) // 2
                self.screen.blit(scaled_image, (piece["pos"][0] + x_offset, piece["pos"][1] + y_offset))

        # Dibujar la pieza seleccionada encima de todas las demás
        if self.selected_piece:
            image = self.piece_images.get(self.selected_piece["name"]) or self.piece_images_gold.get(self.selected_piece["name"])
            if image:
                scaled_image = pygame.transform.scale(image, (self.cell_size - 10, self.cell_size - 10))
                x_offset = (self.cell_size - scaled_image.get_width()) // 2
                y_offset = (self.cell_size - scaled_image.get_height()) // 2
                self.screen.blit(scaled_image, (self.selected_piece["pos"][0] + x_offset, self.selected_piece["pos"][1] + y_offset))