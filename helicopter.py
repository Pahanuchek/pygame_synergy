import pygame

from settings import Settings


class Helicopter(pygame.sprite.Sprite):
    def __init__(self, obj, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.setting = Settings()
        self.image = pygame.image.load(obj)
        self.image = pygame.transform.scale(self.image, (self.setting.width_tree_river + 20,
                                                         self.setting.height_tree_river + 20))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, *args):
        if args[0]:
            self.rect.x += 3
            if self.rect.x > self.setting.width_screen - 60:
                self.rect.x = self.setting.width_screen - 60
        elif args[1]:
            self.rect.x -= 3
            if self.rect.x < 0:
                self.rect.x = 0
        elif args[2]:
            self.rect.y += 3
            if self.rect.y > self.setting.height_screen - 60:
                self.rect.y = self.setting.height_screen - 60
        elif args[3]:
            self.rect.y -= 3
            if self.rect.y < 0:
                self.rect.y = 0
