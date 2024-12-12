import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Aquí gestionarías lo que ocurre cuando se hace clic
            pass

    def draw(self):
        # Dibuja la interfaz, como botones, texto, etc.
        text = self.font.render("Juego IA", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
