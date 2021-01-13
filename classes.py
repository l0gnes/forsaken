import enums
import json

# Dungeon Generator Helper Functions
# (I know these aren't classes, but their easier to implement as standalone functions)

def generate_void_dungeon_map(cols, rows):
    m = []
    for row in range(rows):
        m.append(
            [enums.DungeonTiles.DUNGEON_VOID,] * cols
        )
    return DungeonRoomMap(m)

# Dungeon Generator Classes

class DungeonGenerator(object):
    def __init__(self, game, width, height, *args, **kwargs):
        self.game = game
        self.priority = kwargs.pop('priority', 100)
        self.HALLWAY_GENERATOR = DungeonHallwayGenerator()
        self.DUNGEON_MAPPING = generate_void_dungeon_map(width, height)

class FileDungeonGenerator(DungeonGenerator):
    def __init__(self, game, *args, **kwargs):
        super().__init__(
            game, *args, **kwargs
        )
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
        return

class DungeonRoomMap(object):
    def __init__(self, array : list = [], *args, **kwargs):
        self._mapping = array
        self.overlapping_rooms = []

    def overlap_room(self, room):
        pass

    @property
    def map_width(self):
        if len(self._mapping) == 0:
            return 0

        return len(self._mapping[:1]) # Grabs the length of the first width

    @property
    def map_height(self):
        return len(self._mapping)

    @property
    def map_area(self):
        if self.map_width != 0:
            return sum([len(c) for c in self._mapping])
        raise ValueError("Map is Empty")


    def check_for_interference(self, other : DungeonRoom):
        interference_value = 0
        for ri, row in enumerate(other.map._mapping, start=other.pos_x):
            for ci, col in enumerate(other.map_mapping, start=other.pos_y):
                if self._mapping[ri][ci] != enums.DungeonTiles.DUNGEON_VOID:
                    interference_value += 1
        return interference_value

    # Creates a hollow box, filled in boxes are currently not supported
    def make_box(self, a, b, hollow : bool = True):
        if any([len(x) != 2 for x in (a, b)]):
            raise ValueError("Not valid thingy")

        if hollow: # Handles hollow rooms
            for rowindex, row in enumerate(self._mapping):
                
                # Handling top/bottom row
                if rowindex == a[1] or rowindex == b[1]:
                    # now row = what we are working with for x
                    new_row = []
                    for i in range(len(row)):
                        if i >= a[0] and i <= b[0]:
                            new_row.append(enums.DungeonTiles.wall)
                        else:
                            new_row.append(enums.DungeonTiles.empty)
                    self._mapping[a[1]] = new_row # Writes the top row
                
                # Handling hollow middle rows
                if rowindex >= a[1] and rowindex <= b[1]:
                    new_row = [enums.DungeonTiles.empty,] * len(row)

                    for colindex, col in enumerate(new_row):
                        if colindex == a[0] or colindex == b[0]:
                            new_row[colindex] = enums.DungeonTiles.wall
            return self

    # Places a singular wall
    def place_wall(self, x, y):
        self._mapping[y][x] = enums.DungeonTiles.wall

    # Does the exact same thing as above, but places a custom defined tile.
    def place_tile(self, x, y, dungeonTile : enums.DungeonTiles):
        self._mapping[y][x] = dungeonTile 

class DungeonHallwayGenerator(object):
    def __init__(self, *args, **kwargs):
        pass

class DungeonRoom(object):
    def __init__(self, game, width, height, *args, **kwargs):
        self.game = game
        self.width = width
        self.height = height

        self.map = self.generate_array_mapping()

        self.pos_x, self.pos_y = None, None # Nullify the position

    def generate_array_mapping(self, mapping_class = DungeonRoomMap): # Allow the ability to generate map using a custom mapping class in ext
        a = []
        for row in range(self.height):
            a.append(
                [enums.DungeonTiles.empty,] * self.width
            )
        return mapping_class.__init__(a)

    def generate_at(self, x, y):
        raise NotImplementedError

    @property
    def bounding_box_tile_count(self):
        return self.width * self.height

if __name__ == "__main__":
    gen = DungeonGenerator(None, 30, 30)

