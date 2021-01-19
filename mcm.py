import pygame
from player import PlayerObject

class MovingCameraManager(object):
    def __init__(self, game, s : pygame.Surface, *args, **kwargs):
        self.game = game
        self.mapped_surface = s

        self.offset_x = 0
        self.offset_y = 0

    def render_bottom_level_mapping(self):
        self.game.ACTIVE_SURFACE.SURFACE.blit(
            self.mapped_surface,
            (
                0 - self.offset_x,
                0 - self.offset_y
            )
        )

    def render_character(self, char):
        # Call this post-render_bottom_level_mapping
        self.game.ACTIVE_SURFACE.SURFACE.blit(
            self.game.fetch_player(),
            (
                char.x - self.offset_x,
                char.y - self.offset_y
            )
        )
