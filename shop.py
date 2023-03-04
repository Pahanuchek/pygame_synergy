import pygame
from settings import Settings
from utils import entrance


class Shop(pygame.sprite.Sprite):
    def __init__(self, obj, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.setting = Settings()
        self.image = pygame.image.load(obj)
        self.image = pygame.transform.scale(self.image, (self.setting.width_cloud,
                                                         self.setting.height_cloud))
        self.rect = self.image.get_rect(center=(x, y))


def shop_water(group_1, group_2, group_3, n, m):
    shop = Shop('img/shop.png', n, m)
    if entrance(shop, group_1):
        if entrance(shop, group_2):
            group_3.add(shop)
