import pygame, psutil, os

def draw_fps_counter(screen, clock):

    # Make sure this is here so i dont forget
    if not pygame.font.get_init():
        print("> boop.py | Force init pygame.font")
        pygame.font.init()

    fp = pygame.font.get_default_font() # Gets system font
    font = pygame.font.Font(fp, 16)

    # Creates a new surface
    f = clock.get_fps()
    sur = font.render(
        f"{round(f):,} FPS",
        True, # Antialias
        (255, 0, 0)
    )

    screen.blit(sur, (5, 5))

def draw_mem_counter(screen):

    # Make sure this is here so i dont forget
    if not pygame.font.get_init():
        print("> boop.py | Force init pygame.font")
        pygame.font.init()

    fp = pygame.font.get_default_font() # Gets system font
    font = pygame.font.Font(fp, 12)

    # Creates a new surface

    process = psutil.Process(os.getpid())
    ram = process.memory_info().rss / 1024 ** 2

    sur = font.render(
        f"MEM: {round(ram,2):,} MB",
        True, # Antialias
        (0, 255, 0)
    )

    screen.blit(sur, (5, 20))

class EnumeratingTicker():
    def __init__(self, fps : int, maxtick : int = 20):
        self.fps = fps
        self.current_tick = 0
        self.maxtick = maxtick
        self.tick_loops = 0 # How many times the ticker has looped back to 0

        self._clock = pygame.time.Clock()

        self.scheduled_events = {}


    def ctick(self):
        self.current_tick = self.current_tick + 1 if self.current_tick < self.maxtick else 0
        if self.current_tick == 0: self.tick_loops += 1 # Add another count to loop counter if full tickloop completed
        self._clock.tick(self.fps)

    def get_fps(self):
        return self._clock.get_fps()

class EntityResponse(object):
    def __init__(self, entity_cache, entityid, entityobject, isimportant : bool = True):
        self.entity_cache = entity_cache

        self.id = entityid
        self.entity = entityobject
        self.isimportant = self.isimportant

    def pop(self):
        if self.isimportant:
            if self.id in self.entity_cache.important.keys():
                del self.entity_cache.important[self.id]
            else:
                # TODO: Add an error for this? at least something for logging
                return # The entity was alread deleted

        else:
            if self.id in self.entity_cache.unsorted.keys():
                del self.entity_cache.unsorted[self.id]
            else:
                # TODO: Add an error for this
                return


class EntityCache(object):
    def __init__(self, *args, **kwargs):
        self.unsorted = {} # Holds random entities or something idk
        self.important = {} # Holds entities based on keywords

    def push_important(self, key : str, value):
        if key.startswith('0x'):
            raise KeyError('Important entity cannot start with 0x key')
        if key in self.important.keys():
            raise KeyError('Entity Slot alread in use')
        else:
            self.important[key] = value

    def push_unsorted(self, value):
        self.unsorted[str(hex(len(self.unsorted)))] = value

    def pull_important(self, key : str):
        if key not in self.important.keys():
            return None
        return self.important[key]

    @property
    def all_entities(self):
        return dict(self.unsorted, **self.important)

    def __len__(self):
        return len(self.all_entities)

    def __iter__(self):
        self._n = 0
        return self

    def draw_all_entities(self, screen):
        for i in self.all_entities.values():
            if hasattr(i, 'draw_entity'):
                i.draw_entity(screen)
            else:
                print(f"Entity of class ``{i.__class__.__name__}`` has no draw_entity() func")

    def __next__(self):
        if self._n < len(self):
            self._n += 1
            return tuple(self.all_entities.values())[self._n-1]
        else:
            raise StopIteration

def fade_array(L : list):
    """
    Copies an array to the end of itself so the numbers can fade
    1, 2, 3 -> 1, 2, 3, 2, 1
    """
    L.extend(reversed(L[1:-1]))
    return L

class bCordsWrapper(object):
    def __init__(self, a, b, add_to_all : int = 0):
        self.x1 = a[0]
        self.x2 = b[0]

        self.y1 = a[1]
        self.y2 = b[1]
        self.add_to_all = add_to_all

    @property
    def top_left(self):
        return self.x1, self.y1

    @property
    def bottom_right(self):
        return self.x2, self.y2

    @property
    def ppTL(self):
        return self.x1 * 16 + self.add_to_all, self.y1 * 16 + self.add_to_all

    @property
    def ppBR(self):
        return self.x2 * 16 + self.add_to_all, self.y2 * 16 + self.add_to_all

    @property
    def ppdistWidth(self):
        return int((self.x2 * 16) - (self.x1 * 16))

    @property
    def ppdistHeight(self):
        return (self.y2 * 16) - (self.y1 * 16)