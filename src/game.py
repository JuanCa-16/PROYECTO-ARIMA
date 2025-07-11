import pygame
import os
import random
import tkinter as tk
from tkinter import simpledialog, messagebox
from logica import iniciar, validar_adyacentes_mismo_tipo
import sys  # Importa la librería para salir del programa

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
        self.can_move = False
        self.inicial= True

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

        # Agregar una lista de posiciones válidas iniciales
        self.valid_positions = [
            f"{chr(65 + col)}{row}"
            for row in range(1, 3)  # Filas 1 y 2
            for col in range(8)  # Columnas A-H
        ]

        # Mantener las piezas superiores bloqueadas
        self.locked_pieces = []
        for piece in self.pieces:
            if piece["pos"][1] < self.margin + self.cell_size * 2:  # Piezas en filas superiores
                self.locked_pieces.append(piece)

        # Inicializar contador de movimientos
        self.movimientos_realizados = 0
        self.movimientos_permitidos = 1  # Valor por defecto

    #CREA DICCIONARIO DE COORDENADAS(A8 = (COL,FILA))
    def create_board(self):
        # Genera un diccionario con las coordenadas del tablero
        board = {}
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for row in range(self.board_size):
            for col in range(self.board_size):
                coordinate = f"{letters[col]}{self.board_size - row}"
                board[coordinate] = (col, row)
        return board

    #CREA DICCIONARIO DE 0 y letras
    def create_board_status(self):
        # Inicializa el estado del tablero con 0
        board_status = {}
        for key in self.board:
            board_status[key] = 0  # Representa celdas vacías
        return board_status

    #PONER FICHAS IA EN TABLERO Y LAS DEL JUGADOR ABAJO DEL MAPA
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

    #VENTANA DE CANT DE MOV JUGADOR
    def preguntar_movimientos(self):
        """Pregunta al usuario cuántos movimientos desea hacer usando una ventana emergente."""
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter

        while True:
            try:
                movimientos = simpledialog.askinteger("Movimientos", "¿Cuántos movimientos deseas hacer (1-4)?")
                if movimientos is None:
                    print("Operación cancelada por el usuario.")
                    return
                if 1 <= movimientos <= 4:
                    self.movimientos_permitidos = movimientos
                    break
                else:
                    print("Por favor, ingresa un número entre 1 y 4.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

    #DADO EL NOMBRE DE LA IMAGEN ASIGNA SU FICHA EN LETRA
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

    #DADA LA LETRA RETORNA EL NOMBRE DE LA IMAGEN   
    def get_piece_name(self, initial):
        """Devuelve el nombre de la pieza correspondiente a la inicial dorada o gris."""
        piece_names_gold = {
            "r": "conejo",
            "h": "caballo",
            "d": "perro",
            "g": "gato",
            "c": "camello",
            "e": "elefante"
        }
        piece_names_gris = {
            "R": "conejoGris",
            "H": "caballoGris",
            "D": "perroGris",
            "G": "gatoGris",
            "C": "camelloGris",
            "E": "elefanteGris"
        }
        
        # Buscar en los diccionarios si la inicial está presente
        if initial in piece_names_gold:
            return piece_names_gold[initial]
        elif initial in piece_names_gris:
            return piece_names_gris[initial]
        return None  # Retorna None si no se encuentra la inicial

    #IMPRRIME EL TABLERO EN CONSOLA
    def print_board_status(self):
        # Imprimir el estado del tablero
        for row in range(self.board_size):
            row_state = ""
            for col in range(self.board_size):
                coordinate = f"{chr(65 + col)}{self.board_size - row}"
                row_state += f"{self.board_status[coordinate]} "  # Estado de cada celda
            print(row_state)

        print()

    #ACTUALIZA ALL (MOVIMINTOS USUARIO, ARRASTRAR Y SOLTAR, CAMBIOS DE TURNOS, GANAR Y PERDER)
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Selección de pieza por parte del jugador
                for piece in reversed(self.pieces):

                    piece_rect = pygame.Rect(piece["pos"], (self.cell_size, self.cell_size))
                    if piece_rect.collidepoint(event.pos):
                        self.selected_piece = piece
                        self.mouse_offset = (event.pos[0] - piece["pos"][0], event.pos[1] - piece["pos"][1])
                        self.original_position = piece["pos"]
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            
            if event.button == 1:
                if self.selected_piece:
                    # Calcular la celda destino
                    mouse_x, mouse_y = event.pos
                    col = (mouse_x - self.margin) // self.cell_size
                    row = (mouse_y - self.margin) // self.cell_size

                    if 0 <= col < self.board_size and 0 <= row < self.board_size:  # Dentro del tablero
                        x = self.margin + col * self.cell_size
                        y = self.margin + row * self.cell_size
                        coordinate = f"{chr(65 + col)}{self.board_size - row}"

                        # Verificar si la celda está ocupada
                        cell_occupied = any(p["pos"] == (x, y) for p in self.pieces)

                        if not cell_occupied:
                            # Restricción de posiciones iniciales
                            if self.can_move == False and self.selected_piece not in self.locked_pieces and coordinate not in self.valid_positions:
                                print(f"No se puede colocar la pieza en {coordinate}. Solo se permiten posiciones iniciales válidas.")
                                self.selected_piece["pos"] = self.original_position
                            else:
                                old_coordinate = f"{chr(65 + self.original_position[0] // self.cell_size)}{self.board_size - (self.original_position[1] // self.cell_size)}"
                                self.board_status[old_coordinate] = 0
                                self.selected_piece["pos"] = (x, y)
                                self.board_status[coordinate] = self.get_piece_initial(self.selected_piece["name"])

                                if self.selected_piece in self.locked_pieces:
                                    self.locked_pieces.remove(self.selected_piece)  # Desbloquear pieza

                                self.print_board_status()
                                self.eliminar_ficha()  # Eliminar fichas adyacentes
                                # SE INSERTA GANAR
                        else:
                            print(f"Celda ocupada: {coordinate}. No se puede mover la pieza.")
                            self.selected_piece["pos"] = self.original_position
                    else:
                        print("Intento de mover fuera del tablero.")
                        self.selected_piece["pos"] = self.original_position

                    # Resetear selección
                    self.selected_piece = None
                    self.original_position = None


                    if self.inicial == True:
                        # Verificar si todas las piezas grises han sido colocadas
                        if self.all_grey_pieces_placed():
                            self.can_move = True
                            self.inicial = False
                            print("¡Todas las piezas grises están en el tablero! Turno de la IA.")
                            self.execute_ai_turn()  # Llamar al turno de la IA
                            if(self.ganar('r')):
                                root = tk.Tk()
                                root.withdraw()  # Ocultar la ventana principal de Tkinter
                                messagebox.showinfo("GANADOR IA", "LA IA ES EL FUTURO")
                                root.destroy()
                                pygame.quit()
                                sys.exit() 


                    else:
                        # Incrementar el contador de movimientos
                        self.movimientos_realizados += 1
                        print("Cantidad de movimientos realizados: ",self.movimientos_realizados)
                        if(self.ganar('R')):
                                root = tk.Tk()
                                root.withdraw()  # Ocultar la ventana principal de Tkinter
                                messagebox.showinfo("GANADOR HUMANO", "DIGNO DE DEMOSTRAR EL PODER HUMANO")
                                root.destroy()
                                pygame.quit()
                                sys.exit() 
                        # Verificar si se han realizado los movimientos permitidos
                        if self.movimientos_realizados >= self.movimientos_permitidos:
                            self.movimientos_realizados = 0  # Reiniciar el contador

                            self.execute_ai_turn()  # Ejecutar el turno de la IA
                    
                        

        elif event.type == pygame.MOUSEMOTION:
            if self.selected_piece:
                # Actualizar la posición de la pieza mientras se arrastra
                self.selected_piece["pos"] = (event.pos[0] - self.mouse_offset[0], event.pos[1] - self.mouse_offset[1])

    #SABER SI EL USUARIO YA UBICO SUS FICHAS
    def all_grey_pieces_placed(self):
        """Verifica si todas las piezas grises han sido colocadas en el tablero."""
        for piece in self.pieces:
            if piece["name"].endswith("Gris"):  # Las piezas grises
                col = (piece["pos"][0] - self.margin) // self.cell_size
                row = (piece["pos"][1] - self.margin) // self.cell_size

                if not (0 <= col < self.board_size and 0 <= row < self.board_size):
                    # Si alguna pieza gris sigue fuera del tablero
                    return False
        return True
    
    #IA HACE SU MINIMAX Y EFECTUA EL MOVIMIENTO
    def execute_ai_turn(self):
        """Calcula y ejecuta el movimiento de la IA utilizando Minimax."""
        print(self.board_status)
        tablero, best_move = iniciar(self.board_status, 1)
        
        print("JUAAAN",best_move, type(best_move))
        if best_move:
            old_pos = best_move[0]
            new_pos = best_move[1]

            if(len(best_move) == 3):
                guardar = self.board_status[new_pos]

            piece = self.board_status[old_pos]
            self.board_status[new_pos] = piece
            self.board_status[old_pos] = 0

            # Actualizar posición de la pieza en la lista `self.pieces`
            for p in self.pieces:
                if p["pos"] == self.get_screen_position_from_coordinate(old_pos):
                    p["pos"] = self.get_screen_position_from_coordinate(new_pos)
                    break

            print(f"IA movió {piece} de {old_pos} a {new_pos}.")

            if(len(best_move)==3):
                    
                
                new_new_pos = best_move[2]
                
                self.board_status[new_new_pos] = guardar
                # Actualizar posición de la pieza en la lista `self.pieces`
                nombre = self.get_piece_name(guardar)
                print(nombre)
                for p in self.pieces:
                    if p["pos"] == self.get_screen_position_from_coordinate(new_pos) and p["name"] == nombre:
                        p["pos"] = self.get_screen_position_from_coordinate(new_new_pos)
                        break

                print(f"IA EMPUJO {piece} de {new_pos} a {new_new_pos}.")

            self.print_board_status()

            # Redibujar el tablero y las piezas
            self.screen.fill((255, 255, 255))  # Fondo blanco
            self.draw()
            pygame.display.flip()  # Actualizar la pantalla
            if(self.ganar('r')):
                                root = tk.Tk()
                                root.withdraw()  # Ocultar la ventana principal de Tkinter
                                messagebox.showinfo("GANADOR IA", "LA IA ES EL FUTURO")
                                root.destroy()
                                pygame.quit()
                                sys.exit() 
            # Preguntar al usuario cuántos movimientos desea hacer
        self.preguntar_movimientos()

    #CONVIERTE UNA COORDENADA DE TIPO A8 A X,Y
    def get_screen_position_from_coordinate(self, coordinate):
        """Convierte una coordenada del tablero (A1, B2, etc.) a una posición de pantalla."""
        col = ord(coordinate[0]) - 65  # 'A' = 0, 'B' = 1, etc.
        row = self.board_size - int(coordinate[1])  # Fila del tablero
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        return (x, y)

    #DIBUJA ALL VISUAL
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

    #MENSAJE DE ELIMINAR FICHA Y LOGICA
    def eliminar_ficha(self):

            blue_coordinates = ["C3", "F3", "C6", "F6"]

            for coordinate in blue_coordinates:

                if(coordinate != '0'):
                    if not validar_adyacentes_mismo_tipo(self.board_status, coordinate):
                        # Obtener la ficha eliminada
                        ficha_eliminada = self.board_status[coordinate]

                        # Eliminar la ficha del tablero
                        self.board_status[coordinate] = 0

                        # Actualizar visualmente la ficha en la lista
                        for piece in self.pieces:
                            col, row = self.board[coordinate]  # Obtener coordenada de píxel
                            x = self.margin + col * self.cell_size
                            y = self.margin + row * self.cell_size
                            if piece["pos"] == (x, y):
                                self.pieces.remove(piece)
                                # Mostrar mensaje con tkinter
                                root = tk.Tk()
                                root.withdraw()  # Ocultar la ventana principal de Tkinter
                                messagebox.showinfo("Ficha Eliminada", f"Se eliminó la ficha {ficha_eliminada} en la coordenada {coordinate}")
                                root.destroy()
                                print(f"Ficha eliminada en {coordinate}")
                                break
                        
    #BOOLEANO DE SI GANO UN JUGADOR DADO                
    def ganar(self, jugador):
        """
        Valida si un jugador ha ganado por alguna de las dos condiciones:
        1. Si un conejo alcanza la fila 1 (para 'R') o la fila 8 (para 'r').
        2. Si el jugador contrario se queda sin conejos.
        """
        conejos_rivales = 0

        # Recorrer el tablero para verificar las condiciones
        ganarR = {'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1'}
        ganarr = {'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8'}

        for llave,valor in self.board_status.items():
        
            # Verificar si algún conejo alcanzó la fila objetivo
            if jugador == 'r' and valor == 'r' and (llave in ganarR):  # Minúscula llega a fila 8
                return True
            elif jugador == 'R' and valor == 'R' and (llave in ganarr):  # Mayúscula llega a fila 1
                    return True

            # Contar los conejos rivales
            if jugador == 'r' and valor == 'R':  # Contar conejos mayúscula
                conejos_rivales += 1
            elif jugador == 'R' and valor == 'r':  # Contar conejos minúscula
                conejos_rivales += 1

        print('cantC', conejos_rivales)
        # Verificar si el jugador rival se quedó sin conejos
        if conejos_rivales == 0:
            return True

        return False
    #-----> AQUI VA GANAR -----------
