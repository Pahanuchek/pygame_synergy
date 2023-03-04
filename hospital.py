import pygame
from settings import Settings
from utils import entrance


class Hospital(pygame.sprite.Sprite):
    def __init__(self, obj, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.setting = Settings()
        self.image = pygame.image.load(obj)
        self.image = pygame.transform.scale(self.image, (self.setting.width_cloud,
                                                         self.setting.height_cloud))
        self.rect = self.image.get_rect(center=(x, y))


def hospitals(group_1, group_2, group_3, n, m):
    hospital = Hospital('img/hospital.png', n, m)
    if entrance(hospital, group_1):
        if entrance(hospital, group_2):
            group_3.add(hospital)