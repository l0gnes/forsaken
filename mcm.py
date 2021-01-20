import pygame
from player import PlayerObject

class MovingCameraManager(object):
    def __init__(self, game, s : pygame.Surface, *args, **kwargs):
        self.game = game
        self.mapped_surface = s

        self.offset_x = 0
        self.offset_y = 0

    def render_bottom_level_mapping(self, s):
        self.game.WindowHandle.ACTIVE_SURFACE.SURFACE.blit(
            s,
            (
                0 - self.offset_x,
                0 - self.offset_y
            )
        )

    def render_character(self, char):
        # Call this post-render_bottom_level_mapping
        self.game.WindowHandle.ACTIVE_SURFACE.SURFACE.blit(
            self.game.fetch_player().image,
            (
                char.x - self.offset_x,
                char.y - self.offset_y
            )
        )
