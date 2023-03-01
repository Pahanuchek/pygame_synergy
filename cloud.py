import random

import pygame

W, H = 1400, 700

class Cloud(pygame.sprite.Sprite):

    def __init__(self, obj):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(obj)
        self.image = pygame.transform.scale(self.image, (100, 80))
        self.rect = self.image.get_rect(center=(50, 100))


    def update(self):
        track = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        num = random.randint(0, 1)
        self.rect.x += track[num][0]
        self.rect.y += track[num][1]



