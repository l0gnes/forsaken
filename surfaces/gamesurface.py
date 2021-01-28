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

        self.DUNGEON_GEN = dungeons.FileDungeonGenerator(self.game)
        self.DUNGEON_MAP = self.DUNGEON_GEN.load_from_file('maptest.json')
        self.DUNGEON_MAP.print_map()



    def event_hook(self, event):
        #print()
        if event.type == pygame.KEYDOWN:
            plr = self.game.fetch_player()
            if event.key == pygame.K_DOWN:
                if plr.can_move(self.DUNGEON_MAP, plr.x, plr.y + 16):
                    plr.move(0, 16)
            elif event.key == pygame.K_UP:
                if plr.can_move(self.DUNGEON_MAP, plr.x, plr.y - 16):
                    plr.move(0, -16)
            elif event.key == pygame.K_LEFT:
                if plr.can_move(self.DUNGEON_MAP, plr.x - 16, plr.y):
                    plr.move(-16, 0)
            elif event.key == pygame.K_RIGHT:
                if plr.can_move(self.DUNGEON_MAP, plr.x + 16, plr.y):
                    plr.move(16, 0)

            x=plr.check_tile(self.DUNGEON_MAP)
            print(x)

    def draw_surface(self):
        self.SURFACE.fill(
            'black'
        )

        self.DUNGEON_MAP.draw_at(7, 4, self.SURFACE)




        self.game.ENTITY_CACHE.draw_all_entities(self.SURFACE)
        #self.mcm.render_bottom_level_mapping(self.SURFACE)
        self.game.screen.blit(self.SURFACE, (0, 0))
