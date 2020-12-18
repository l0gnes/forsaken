from enum import Enum

class GameState(Enum):
    playing = 0 # Shown if the game is active
    menu_screen = 1 # Shown if you're on the main menu screen
    paused = 2 # Shown if game is in a paused state