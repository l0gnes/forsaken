import pygame
from stuff import models
#from main import ENTITY_CACHE

class EventHandler(object):
    def __init__(self, game):
        self.game = game

        self.screen = self.game.screen
        self.clock = self.game.Ticker
        self.entity_cache = self.game.ENTITY_CACHE
        self.settings = self.game.SETTINGS

        self.event_mapping = {
            pygame.QUIT : pygame.quit,
            pygame.KEYDOWN : self.handleKeys
        }

    def handleKeys(self, event, *args, **kwargs):
        if event.key == pygame.K_q:
            pygame.quit()

    def handle_events(self):
        ev = pygame.event.poll()

        # Hook in the current surface's events, but only if the function exists
        if hasattr(self.game.WindowHandle.ACTIVE_SURFACE, 'event_hook'):
            self.game.WindowHandle.ACTIVE_SURFACE.event_hook(ev)

        if ev.type in self.event_mapping.keys():
            return self.event_mapping[ev.type](ev)
        else:
            return
