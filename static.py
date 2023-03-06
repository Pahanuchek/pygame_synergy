import pygame


class StaticObject(pygame.sprite.Sprite):
    # Класс статических объектов
    def __init__(self, obj, x, y, wpic, hpic):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(obj)
        self.image = pygame.transform.scale(self.image, (wpic,
                                                         hpic))
        self.rect = self.image.get_rect(center=(x, y))
