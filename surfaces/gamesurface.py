import pygame
from mcm import MovingCameraManager
import player
import monsters
import dungeons

class GameSurface(object):
    def __init__(self, game, *args, **kwargs):
        self.game = game

        self.SURFACE = pygame.Surface(
            size = self.game.screen.get_size()
        )

        self.mcm = MovingCameraManager(self.game, self.SURFACE)
        self.game.ENTITY_CACHE.push_important("PLAYER", player.PlayerObject(self.game))
        self.game.fetch_player().set_position_coordinate(1, 1)

    def event_hook(self, event):
        
        # Handles player controls on this screen
        self.game.fetch_player().control_hook(event)

    def draw_surface(self):
        self.SURFACE.fill(
            'black'
        )

        self.game.DUNGEON_MAP.draw_at(0, 0, self.SURFACE)




        self.game.ENTITY_CACHE.draw_all_entities(self.SURFACE)
        #self.mcm.render_bottom_level_mapping(self.SURFACE)
        self.game.screen.blit(self.SURFACE, (0, 0))
