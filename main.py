import pygame

import sys

import random

from cloud import Cloud

W, H = 1400, 700

FPS = 20

a_obj = (H // 300) * 10
clock = pygame.time.Clock()

class SaveTheForest:


    def __init__(self):



        pygame.init()

        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("Save The Forest")

        self.bg = pygame.image.load('img/bg.png')
        self.bg = pygame.transform.scale(self.bg, (W, H))
        self.screen.blit(self.bg, (0, 0))

        self.icon = pygame.image.load('img/icon.jpg')
        pygame.display.set_icon(self.icon)

        self.tree = pygame.image.load('img/tree.png')
        self.tree = pygame.transform.scale(self.tree, (a_obj, a_obj))

        self.lake = pygame.image.load('img/lake.png')
        self.lake = pygame.transform.scale(self.lake, (a_obj * 2, a_obj))


    def planting(self, q, obj, s=[]):
        coordinate = []
        while len(coordinate) <= q:
            k = random.randint(a_obj, H - a_obj * 2)
            m = random.randint(a_obj, W - a_obj)
            if self.control(coordinate, k, m) or self.control(s, k, m):
                continue
            else:
                self.screen.blit(obj, (k, m))
                coordinate.append((k, m))
        return coordinate


    def control(self, s, k_tree, m_tree):
        for i,row in enumerate(s):
            if abs(row[0] - k_tree) < a_obj * 2 and abs(row[1] - m_tree) < a_obj:
                return True


    def run_game(self):
        self.list_tree = self.planting(a_obj, self.tree)
        self.list_lake = self.planting(a_obj//10, self.lake, s = self.list_tree)
        cl = Cloud('img/cloud.png')


        while True:
            clock.tick(FPS)
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(cl.image, cl.rect)
            cl.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            pygame.display.update()


if __name__ == '__main__':
    ai = SaveTheForest()
    ai.run_game()