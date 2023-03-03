import pygame
from settings import Settings
from utils import entrance


class Lake(pygame.sprite.Sprite):
    def __init__(self, obj, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.setting = Settings()
        self.image = pygame.image.load(obj)
        self.image = pygame.transform.scale(self.image, (self.setting.width_tree_river,
                                                         self.setting.height_tree_river))
        self.rect = self.image.get_rect(center=(x, y))


def lake(group_1, group_2, n, m):
    lake = Lake('img/lake.png', n, m)
    if entrance(lake, group_1):
        if len(group_2) == 0:
            group_2.add(lake)
        elif entrance(lake, group_2):
            group_2.add(lake)
