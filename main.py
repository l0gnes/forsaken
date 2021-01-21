import sys, os

x = os.path.split(__file__)[0]
sys.path.extend(
    (
        x,
        x + "\\utility",
        x + "\\extensions",
        x + "\\assets"
    )
)

import pygame
import queue
from utility import boop, sethand
from stuff import models
import time


import events, window, game

__verison__ = "Alpha v0.3"

if __name__ == "__main__":
    # Adding a dummy driver for the PI
    #os.environ['SDL_VIDEODRIVER'] = 'dummy'


    global SETTINGS
    global WindowHandle
    SETTINGS = sethand.load_settings_file(create_if_not_exists=True)

    pygame.display.set_caption("Forsaken")
    screen = pygame.display.set_mode((960, 800), 0, 32)
    pygame.init()
    pygame.display.init()
    pygame.font.init()

    GAME = game.GameHandler(screen, SETTINGS)
    GAME.start_game_loop()
