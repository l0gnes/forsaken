import pygame
import inventory
import math
import random
import enums

PLAYER_SIZE = (16, 16)

class EquipmentManager(object):
    def __init__(self, player):
        self.PLAYER = PLAYER

        self.EQUIPS = {}

    def get_health_benefits(self):
        return 0 # TODO: Implement Later

    # COMMON EQUIPS BELOW

    @property
    def helmet(self):
        self.EQUIPS.get(
            'helmet', None
        )

    @property
    def chestplate(self):
        self.EQUIPS.get(
            'chestplate', None
        )

    @property
    def leggings(self):
        self.EQUIPS.get(
            "leggings", None
        )

    @property
    def boots(self):
        self.EQUIPS.get(
            "boots", None
        )

class PlayerObject(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        # Init base class
        pygame.sprite.Sprite.__init__(self)

        self.height, self.width = PLAYER_SIZE
        self.image = pygame.Surface((self.height, self.width))
        self.image.fill('red') # TODO: Do something about this

        self.rect = self.image.get_rect()

        self.experience = 0

        self.SPECIES = random.choice(enums.PlayerSpecies.__members__.values())
        self.CLASS = random.choice(enums.PlayerClasses.__members__.values())
        self.PERK = random.choice(enums.PlayerBoosts.__members__.values())
        
        self.INVENTORY = inventory.InventoryHandler(self)
        self.EQUIPS = EquipmentManager(self)

    def add_experience(self, c):
        self.experience += round(c)
        return round(c)

    def heal(self, a):
        h2h = round(a) if round(a) + self.health <= self.total_health else self.total_health - self.health
        self.health += h2h
        return h2h

    @property
    def health(self):
        return 20 * (5 * self.level) + self.EQUIPS.get_health_benefits()

    @property
    def level(self): # Ensure this works... because it probably doesn't
        return self.experience / 75 * math.floor(self.experience / 75)

    def draw(self, screen):
        screen.blit(self.image, self.location)

    @property
    def location(self):
        return (self.x, self.y)

    @property
    def x(self): return self.rect.x

    @property
    def y(self): return self.rect.y

    def move(self, x : int, y : int, *args, **kwargs):
        new_pos = self.rect.move(x, y)
        self.rect.x, self.rect.y = new_pos.x, new_pos.y
        return self.rect

if __name__ == "__main__":
    char = PlayerObject()
    print(char.height, char.width, sep='\t')
