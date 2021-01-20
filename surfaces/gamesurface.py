import pygame
from mcm import MovingCameraManager
import player
import monsters

class GameSurface(object):
    def __init__(self, game, *args, **kwargs):
        self.game = game

        self.SURFACE = pygame.Surface(
            size = self.game.screen.get_size()
        )

        self.mcm = MovingCameraManager(self.game, self.SURFACE)
        self.game.ENTITY_CACHE.push_important("PLAYER", player.PlayerObject(self.game))
        self.game.ENTITY_CACHE.push_unsorted(monsters.Monster())



    def event_hook(self, event):
        #print()
        if event.type == pygame.KEYDOWN:
            print(event)
            if event.key == pygame.K_DOWN:
                self.game.fetch_player().move(0, 16)
            elif event.key == pygame.K_UP:
                self.game.fetch_player().move(0, -16)
            elif event.key == pygame.K_LEFT:
                self.game.fetch_player().move(-16, 0)
            elif event.key == pygame.K_RIGHT:
                self.game.fetch_player().move(16, 0)


    def draw_surface(self):
        self.SURFACE.fill(
            'purple'
        )




        self.game.ENTITY_CACHE.draw_all_entities(self.SURFACE)
        #self.mcm.render_bottom_level_mapping(self.SURFACE)
        self.game.screen.blit(self.SURFACE, (0, 0))
