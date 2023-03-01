import pygame

from settings import Settings


class TreeRiver(pygame.sprite.Sprite):
    def __init__(self, obj, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.setting = Settings()
        self.image = pygame.image.load(obj)
        self.image = pygame.transform.scale(self.image, (self.setting.width_tree_river,
                                                         self.setting.height_tree_river))
        self.rect = self.image.get_rect(center=(x, y))


