import pygame

class Monster(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.size = (16, 16)

        self.image = self.get_icon()
        self.rect = self.image.get_rect()

    def get_icon(self):
        s = pygame.Surface((16, 16))
        s.fill('yellow')
        self.image = s
        return s

    def draw_entity(self, screen):
        screen.blit(
            self.image,
            (
                64, 64
            )
        )
