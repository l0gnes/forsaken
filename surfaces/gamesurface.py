import pygame
import player
import monsters
import dungeons
#import itertools


class GameSurface(object):
    def __init__(self, game, *args, **kwargs):
        self.game = game

        self.SURFACE = pygame.Surface(
            size = self.game.screen.get_size()
        )

        #self.mcm = MovingCameraManager(self.game, self.SURFACE)
        self.game.ENTITY_CACHE.push_important("PLAYER", player.PlayerObject(self.game))
        self.game.fetch_player().set_position_coordinate(10, 10)

        # New Camera Management inside this file
        self.CAMERA_OFFSET_X = 0
        self.CAMERA_OFFSET_Y = 0

        # However many points (points on the map where a tile can be drawn)
        # which the camera will check for before shifting the offsets defined
        # above, which render the map differently. (CONSTANT SETTING)
        self.CAMERA_OFFSET_CAP_POINTS = 4

    def get_camera_partition(self):
        w, h = self.game.WindowHandle.screen.get_size()
        W,H = w/16, h/16 # Point based coordinate scheme
        return W + self.CAMERA_OFFSET_X, H + self.CAMERA_OFFSET_Y

    def camera_check_hook(self, event):
        # Player coordinates
        if event.type == pygame.KEYDOWN:
            x, y = self.game.fetch_player().coordinates
            #partition = self.get_camera_partition()
            w, h = self.game.WindowHandle.screen.get_size()
            W, H = w / 16 , h / 16
            #print(partition)

            if not x + self.CAMERA_OFFSET_X >= self.CAMERA_OFFSET_CAP_POINTS:
                self.CAMERA_OFFSET_X += 1

            elif x + self.CAMERA_OFFSET_X >= W - self.CAMERA_OFFSET_CAP_POINTS:
                self.CAMERA_OFFSET_X -= 1

            # ---------------------------------------------------------------------------------------

            if not y + self.CAMERA_OFFSET_Y >= self.CAMERA_OFFSET_CAP_POINTS:
                self.CAMERA_OFFSET_Y += 1

            elif y + self.CAMERA_OFFSET_Y >= H - self.CAMERA_OFFSET_CAP_POINTS:
                self.CAMERA_OFFSET_Y -= 1

            self.game.fetch_player().COLLISION_OFFSETS = (self.CAMERA_OFFSET_X, self.CAMERA_OFFSET_Y)


    def event_hook(self, event):
        # Handles player controls on this screen
        self.game.fetch_player().control_hook(event)

        # Handles camera movement
        self.camera_check_hook(event)

    def draw_surface(self):
        self.SURFACE.fill(
            'black'
        )

        self.game.DUNGEON_MAP.draw_at(0 + self.CAMERA_OFFSET_X, 0 + self.CAMERA_OFFSET_Y, self.SURFACE)

        #self.game.ENTITY_CACHE.draw_all_entities(self.SURFACE)
        self.game.fetch_player().draw_with_camera(self.SURFACE, self.CAMERA_OFFSET_X, self.CAMERA_OFFSET_Y)
        #self.mcm.render_bottom_level_mapping(self.SURFACE)
        self.game.screen.blit(self.SURFACE, (0, 0))
