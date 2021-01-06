from enum import Enum

class GameState(Enum):
    playing = 0 # Shown if the game is active
    menu_screen = 1 # Shown if you're on the main menu screen
    paused = 2 # Shown if game is in a paused state

class DungeonRoomSize(Enum):
    tiny = 0
    small = 1
    medium = 2
    large = 3
    massive = 4
    
    def get_size(self):
        if self.value == 0: # IF TINY
            return 32, 32
        elif self.value == 1:
            return 64, 64
        elif self.value == 2:
            return 128, 128
        elif self.value == 3:
            return 256, 256
        elif self.value == 4:
            return 512, 512
        else:
            return 64, 64# Defaults to Small

class DungeonTiles(Enum):
    DUNGEON_VOID = -1 # Space which is occupied by nothingness, and the player shouldn't be able to walk on it
    empty = 0
    wall = 1

    # TODO: Implement Doors
    door = 2