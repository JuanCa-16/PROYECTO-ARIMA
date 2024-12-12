import pygame
from game import Game


def main():
    pygame.init()

    # Tamaño de la ventana ajustado para tener suficiente espacio alrededor del tablero
    screen = pygame.display.set_mode((450, 550))  # Ventana más grande para márgenes (600,720)
    pygame.display.set_caption("Juego IA")

    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.update(event)

        screen.fill((255, 255, 255))  # Fondo blanco
        game.draw()  # Dibuja el tablero
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()