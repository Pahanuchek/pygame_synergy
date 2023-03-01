import pygame

from settings import Settings


class Cloud(pygame.sprite.Sprite):

    def __init__(self, x, y, obj, speed):
        pygame.sprite.Sprite.__init__(self)
        self.setting = Settings()
        self.image = pygame.image.load(obj)
        self.image = pygame.transform.scale(self.image, (self.setting.width_cloud,
                                                         self.setting.height_cloud))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed


    def update(self, *args):
        if args[1] == 0:
            if self.rect.x < args[0]:
                self.rect.x += self.speed
            else:
                self.rect.x = - self.setting.width_cloud
        if args[1] == 1:
            if self.rect.x > args[0] - self.setting.width_cloud:
                self.rect.x -= self.speed
            else:
                self.rect.x = self.setting.width_screen







