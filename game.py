import pygame
import events, window, player, enums, sound, deco, animations
from utility import sethand, exthand, boop
import importlib
import glob
import os
import functools


# We're going to try to use logging now :)
import logging

# Yeah yeah
from surfaces.loadingscreen import LoadingScreen

# Using this file to keep all of the game data organized

#BANANA

class GameHandler(object):
    def __init__(self, screen, settings):

        self.screen = screen
        self.ENTITY_CACHE = boop.EntityCache()
        self.SETTINGS = settings

        self.LOGGING = self.init_logging()

        # Some important variables
        self.RUNNING = True
        self.GAMESTATE = enums.GameState.loading # Tell to be menu screen

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

        self.addEventNotifier(self.setGamestate)
        self.addEventNotifier(self.start_new_game)

    def init_logging(self):
        L = logging.getLogger(__name__)
        L.setLevel(
            logging.INFO if not self.SETTINGS.fetch('console-debug-logs') else logging.DEBUG
        )
        return L

    def addEventNotifier(self, func, custom_name : str = None):
        self.EVENT_NOTIFIERS[func.__name__ if custom_name is None else custom_name] = func
        return func.__name__

    def addEventListener(self, funcname, func):
        if funcname in self.EVENT_LISTENERS.keys():
            self.EVENT_LISTENERS[funcname].append(func)
        else:
            self.EVENT_LISTENERS[funcname] = [func,]
        return funcname

    @deco.FUNC_EVENT_CALLER("setGamestate")
    def setGamestate(self, g: enums.GameState):
        self.GAMESTATE = g

    @deco.FUNC_EVENT_CALLER("start_new_game")
    def start_new_game(self):
        self.GAMESTATE = enums.GameState.playing

    # Quick function to get player object
    def fetch_player(self):
        self.LOGGING.debug("Fetching player from entity cache")

        p = self.ENTITY_CACHE.pull_important('PLAYER')
        return p # P may be none, meaning that no player object has spawned in


    def start_game_loop(self, *args, **kwargs):

        LoadingScreen(self).draw_surface()
        pygame.display.flip()

        self.LOGGING.info("Initializing Game Stuff!")

        # Init window handler and load the base loading screen
        self.EventHandle = events.EventHandler(self)
        self.SoundHandle = sound.SoundHandler(self)
        self.WindowHandle = window.WindowHandler(self)
        self.AnimationHandler = animations.AnimationHandler(self)

        self.ExtensionHandler = exthand.ExtensionHandler(self)

        # Extensions stuff
        print(self.SoundHandle.SOUNDS)
        self.ExtensionHandler.init()

        self.LOGGING.info("Game is now running!")
        self.GAMESTATE = self.setGamestate(enums.GameState.menu_screen)
        self.WindowHandle.ACTIVE_SURFACE = self.WindowHandle.SURFACE_CACHE['menu']
        while self.RUNNING:
            self.EventHandle.handle_events()
            self.AnimationHandler.do_animations()
            self.WindowHandle.draw_all()
            self.Ticker.ctick()
