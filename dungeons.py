import pygame
import math
import random
import classes as forsakenclasses
import json
import enums

# I really don't know how well my dungeon generator will work

# We're making this it's own class

class DungeonGenerator(object):
    def __init__(self, game, width, height, *args, **kwargs):
        self.game = game
        self.priority = kwargs.pop('priority', 100)
        self.HALLWAY_GENERATOR = None
        self.DUNGEON_MAPPING = generate_void_dungeon_map(width, height)

class DungeonRoomMap(object):
    def __init__(self, array : list = [], *args, **kwargs):
        self._mapping = array
        self.overlapping_rooms = []

        self.offset_x = None
        self.offset_y = None

    def fetch_tile(self, x : int, y : int):
        return enums.DungeonTiles(self._mapping[y][x])

    def print_map(self):
        for i in self._mapping:
            print(''.join(str(i)))

    def draw_at(self, x, y, screen):
        w, h = len(self._mapping[0]), len(self._mapping)
        self.offset_x, self.offset_y = x, y
        sur = pygame.Surface((w * 16, h * 16))
        sur.fill('black')

        for colnum, colcont in enumerate(self._mapping):
            for rownum, num in enumerate(colcont):
                part = pygame.Surface((16, 16))
                if num == enums.DungeonTiles.wall.value:
                    part.fill('grey')
                elif num == enums.DungeonTiles.empty.value:
                    continue
                elif num == enums.DungeonTiles.door.value:
                    part.fill('brown')

                sur.blit(part, (rownum * 16, colnum * 16))


        screen.blit(sur, (x * 16, y * 16))

    def overlap_room(self, room):
        pass

    @property
    def map_width(self):
        if len(self._mapping) == 0:
            return 0

        return len(self._mapping[0]) # Grabs the length of the first width

    @property
    def map_height(self):
        return len(self._mapping)

    @property
    def map_area(self):
        if self.map_width != 0:
            return sum([len(c) for c in self._mapping])
        raise ValueError("Map is Empty")


    def check_for_interference(self, other):
        interference_value = 0
        for ri, row in enumerate(other.map._mapping, start=other.pos_x):
            for ci, col in enumerate(other.map_mapping, start=other.pos_y):
                if self._mapping[ri][ci] != enums.DungeonTiles.DUNGEON_VOID:
                    interference_value += 1
        return interference_value

class FileDungeonGenerator(DungeonGenerator):
    def __init__(self, game, *args, **kwargs):
        ##super().__init__(
        ##    game, *args, **kwargs
        ##)
        self.RAW_MAP_DATA = {}

    @property
    def DUNGEON_MAPPING(self):
        if 'mapping' in self.RAW_MAP_DATA.keys():
            return self.RAW_MAP_DATA['mapping']
        else:
            return None

    def load_from_file(self, path : str):
        with open(path, 'r') as dfile:
            self.RAW_MAP_DATA = json.load(dfile)
        return DungeonRoomMap(self.DUNGEON_MAPPING)

class boopDungeonGenerator(DungeonGenerator):
    def __init__(self, game, *args, **kwargs):
        self.game = game

        self.dungeon_size = self.game.DUNGEON_SIZE
        self.total_dungeon_size = self.dungeon_size.get_size()
