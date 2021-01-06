import pygame
import math
import random
import classes as forsakenclasses

# I really don't know how well my dungeon generator will work

# We're making this it's own class

class boopDungeonRoom(forsakenclasses.DungeonRoom):
    def __init__(self, game, width, height, *args, **kwargs):
        super().__init__(
            game, width, height
        )

    def generate_at(self, x, y):
        pass

class boopDungeonGenerator(forsakenclasses.DungeonGenerator):
    def __init__(self, game, *args, **kwargs):
        super().__init__(
            prioity = 1, # Highest Priority
        )
        self.game = game

        self.dungeon_size = self.game.DUNGEON_SIZE
        self.total_dungeon_size = self.dungeon_size.get_size()

        