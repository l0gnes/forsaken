import pygame
import events, window, player, enums
from utility import sethand, boop

# Using this file to keep all of the game data organized

# Some Important Game Constants
# PLAYER = The character the user is
# game.GAMESTATE = Game State

class GameHandler(object):
    def __init__(self, screen, settings):
        self.screen = screen
        self.ENTITY_CACHE = boop.EntityCache()
        self.SETTINGS = settings

        # Some important variables
        self.RUNNING = True
        self.GAMESTATE = enums.GameState.menu_screen # Loads to menu screen

        # Initializing Handlers
        self.Ticker = boop.EnumeratingTicker(
            self.SETTINGS.fetch('fps-limit')
        )

        self.FONT = pygame.font.Font(pygame.font.get_default_font(), 14)
        self.LARGE_FONT = pygame.font.Font(pygame.font.get_default_font(), 24)
    
    def start_new_game(self):
        print('not implemented yet lol')

    def spawn_player(self):
        ply = player.PlayerObject()
        self.ENTITY_CACHE.push_important('PLAYER', ply)

    # Quick function to get player object
    def fetch_player(self):
        p = self.ENTITY_CACHE.pull_important('PLAYER')
        return p # P may be none, meaning that no player object has spawned in


    def start_game_loop(self, *args, **kwargs):

        self.WindowHandle = window.WindowHandler(self)
        self.EventHandle = events.EventHandler(self)

        #self.spawn_player()

        # Initialization Stuff
        # This function is supposed to only be called once to add things to caches
        self.WindowHandle.do_init_stuff()

        while self.RUNNING:
            self.EventHandle.handle_events()
            self.WindowHandle.draw_all()
            self.Ticker.ctick()

