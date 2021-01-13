import pygame
import inventory

PLAYER_SIZE = (16, 16)

class PlayerObject(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        # Init base class
        pygame.sprite.Sprite.__init__(self)

        self.height, self.width = PLAYER_SIZE
        self.image = pygame.Surface((self.height, self.width))
        self.image.fill('red') # TODO: Do something about this

        self.rect = self.image.get_rect()

        self.INVENTORY = inventory.InventoryHandler(self)

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
