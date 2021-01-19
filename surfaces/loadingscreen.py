import pygame

class LoadingScreen(object):
    def __init__(self, game, *args, **kwargs):
        self.game = game

        self.SURFACE = pygame.Surface(
            size = self.game.screen.get_size()
        )

    def draw_surface(self):
        self.SURFACE.fill("white")

        self.SURFACE.blit(
            self.game.LARGE_FONT.render(
                "LOADING...",
                True, 'black'
            ),
            (0, 0)
        )

        self.game.screen.blit(
            self.SURFACE, (0, 0)
        )