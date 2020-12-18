import pygame
from utility import boop
from enums import GameState
from surfaces import startmenu

class WindowHandler(object):
    def __init__(self, game):
        self.game = game


        self.screen = self.game.screen
        self.clock = self.game.Ticker
        self.entity_cache = self.game.ENTITY_CACHE
        self.settings = self.game.SETTINGS

        self.window_cache = {}

        self.BACKGROUND_COLOR = pygame.Color('black')
        self.SURFACE_CACHE = {}
        self.ACTIVE_SURFACE = None

    def cache_surfaces(self):
        self.SURFACE_CACHE['menu'] = startmenu.MainMenuSurface(self.game)

    def draw_background(self):
        self.screen.fill(
            self.BACKGROUND_COLOR
        )

    def draw_entities(self):
        for item in self.entity_cache:
            item.draw(screen=self.screen)

    def draw_nerd_display(self, force : bool = False):
       
        if self.settings.fetch('fps-display'):
            boop.draw_fps_counter(self.screen, self.clock)

        if self.settings.fetch('ram-display'):
            boop.draw_mem_counter(self.screen)

    def do_init_stuff(self):
        self.cache_surfaces() # Caches surfaces so im not constantly creating menus
        
        if self.game.GAMESTATE == GameState.menu_screen:
            self.ACTIVE_SURFACE = self.SURFACE_CACHE['menu']

    def draw_all(self):
        self.draw_background()
        
        #if self.game.GAMESTATE == GameState.menu_screen:
        #    self.SURFACE_CACHE['menu'].draw_surface()

        #elif self.game.GAMESTATE == GameState.playing:
        #    self.draw_entities() # We only draw our entities while playing the game

        self.ACTIVE_SURFACE.draw_surface()

        self.draw_nerd_display() # Should always be last since it overlaps
        pygame.display.flip()