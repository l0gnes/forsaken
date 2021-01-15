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

class PlayerEquipType(Enum):
    unknown = 0
    helmet = 1
    chestplate = 2
    leggings = 3
    boots = 4

    # TODO: Implement Later
    ring = 5
    amulet = 6

class PlayerSpecies(Enum):
    human = 0
    elf = 1
    orc = 2

class PlayerClasses(Enum):
    warrior = 0
    ranger = 1
    mage = 2

    @property
    def can_cast_magic(self):
        # Add the ids of the classes which can cast magic
        return self.value in (2,)

class PlayerBoosts(self):
    none = 0
    attack = 1
    defence = 2
    accuracy = 3
    criticals = 4
