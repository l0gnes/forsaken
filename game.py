import pygame
import events, window, player, enums, sound
from utility import sethand, exthand, boop
import importlib
import glob
import os
import functools

# We're going to try to use logging now :)
import logging

# Using this file to keep all of the game data organized

# Some Important Game Constants
# PLAYER = The character the user is
# game.GAMESTATE = Game State

class GameHandler(object):
    def __init__(self, screen, settings):

        self.screen = screen
        self.ENTITY_CACHE = boop.EntityCache()
        self.SETTINGS = settings

        self.LOGGING = self.init_logging()

        # Some important variables
        self.RUNNING = True
        self.GAMESTATE = enums.GameState.menu_screen # Loads to menu screen

        # Initializing Handlers
        self.Ticker = boop.EnumeratingTicker(
            self.SETTINGS.fetch('fps-limit')
        )

        self.FONT = pygame.font.Font("./assets/Fool.ttf", 14)
        self.LARGE_FONT = pygame.font.Font("./assets/Fool.ttf", 32)

        self.EXTENSIONS = {
            # Extention Reference (ClassName) = Extension Object
        }

        self.DUNGEON_SIZE = enums.DungeonRoomSize.medium # TODO: Allow users to change this at some point?
        self.EVENT_NOTIFIERS = dict()
        self.EVENT_LISTENERS = dict()
    
    def init_logging(self):
        L = logging.getLogger(__name__)
        L.setLevel(
            logging.INFO if not self.SETTINGS.fetch('console-debug-logs') else logging.DEBUG
        )
        return L

    def start_new_game(self):
        self.GAMESTATE = enums.GameState.playing

    def spawn_player(self):
        self.LOGGING.debug("Spawning Player Object")

        ply = player.PlayerObject()
        self.ENTITY_CACHE.push_important('PLAYER', ply)

    # Quick function to get player object
    def fetch_player(self):
        self.LOGGING.debug("Fetching player from entity cache")

        p = self.ENTITY_CACHE.pull_important('PLAYER')
        return p # P may be none, meaning that no player object has spawned in


    def start_game_loop(self, *args, **kwargs):
        self.LOGGING.info("Initializing Game Stuff!")

        self.WindowHandle = window.WindowHandler(self)
        self.EventHandle = events.EventHandler(self)
        self.SoundHandle = sound.SoundHandler(self)
        self.ExtensionHandler = exthand.ExtensionHandler(self)
        #self.spawn_player()

        # Initialization Stuff
        # This function is supposed to only be called once to add things to caches
        self.WindowHandle.do_init_stuff()

        # Extensions stuff
        self.ExtensionHandler.init()
        
        self.LOGGING.info("Game is now running!")
        while self.RUNNING:
            self.EventHandle.handle_events()
            self.WindowHandle.draw_all()
            self.Ticker.ctick()

