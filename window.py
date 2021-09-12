import pygame
from utility import boop
from enums import GameState
from surfaces import gamesurface, startmenu, loadingscreen
import time

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
        self.ACTIVE_SURFACE = loadingscreen.LoadingScreen(self.game)

        self.FADE = pygame.Surface(size = self.screen.get_size())
        self.FADE.fill('black') # Fill Color = Black because yes
        self.FADE.set_alpha(0) # Initially transparent

        self.do_init_stuff()

    def cache_surfaces(self):
        self.SURFACE_CACHE['menu'] = startmenu.MainMenuSurface(self.game)
        self.SURFACE_CACHE['game'] = gamesurface.GameSurface(self.game)
        self.SURFACE_CACHE['loading'] = loadingscreen.LoadingScreen(self.game)

    def draw_background(self):
        self.screen.fill(
            self.BACKGROUND_COLOR
        )

    def draw_entities(self):
        for item in self.entity_cache:
            item.draw(screen=self.screen)

    def draw_nerd_display(self, force : bool = False):
       
        if self.game.DEBUG_MODE:
            boop.draw_fps_counter(self.screen, self.clock)
            boop.draw_mem_counter(self.screen)
            boop.draw_player_pos(self.screen, self.game.fetch_player())

    def do_init_stuff(self):
        self.cache_surfaces() # Caches surfaces so im not constantly creating menus
        
    def ensure_active_surface(self):
        if self.game.GAMESTATE == GameState.menu_screen:
            self.ACTIVE_SURFACE = self.SURFACE_CACHE['menu']

        elif self.game.GAMESTATE == GameState.playing:
            self.ACTIVE_SURFACE = self.SURFACE_CACHE['game']

        elif self.game.GAMESTATE == GameState.loading:
            self.ACTIVE_SURFACE = self.SURFACE_CACHE['loading']

    def draw_fade_effects(self):
        self.screen.blit(self.FADE, (0, 0))

    def do_with_fade(self, func):
        if not hasattr(func, '__call__'):
            raise ValueError("Function has no call?")

        for i in range(12):
            self.FADE.set_alpha((255 / 12) * i+1)
            self.draw_all()
            pygame.time.delay(5)
        
        func() # Calls the function

        for i in range(12):
            self.FADE.set_alpha(255 - ((255 / 12) * i+1))
            self.draw_all()
            pygame.time.delay(5)


    def draw_all(self):
        self.draw_background()
        self.ensure_active_surface()

        self.ACTIVE_SURFACE.draw_surface()

        self.draw_fade_effects()
        self.draw_nerd_display() # Should always be last since it overlaps
        pygame.display.flip()