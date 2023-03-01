from random import randint as rand

import pygame

import sys

from cloud import Cloud

from tree_river import TreeRiver

from utils import planting

from settings import Settings


class SaveTheForest:

    def __init__(self):

        pygame.init()

        self.clock = pygame.time.Clock()

        self.setting = Settings()

        self.screen = pygame.display.set_mode((self.setting.width_screen, self.setting.height_screen))
        pygame.display.set_caption("Save The Forest")

        self.bg = pygame.image.load('img/bg.jpg')
        self.bg = pygame.transform.scale(self.bg, (self.setting.width_screen, self.setting.height_screen))
        self.screen.blit(self.bg, (0, 0))

        self.icon = pygame.image.load('img/icon.jpg')
        pygame.display.set_icon(self.icon)

        self.clouds_left = pygame.sprite.Group()
        self.clouds_right = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()

    def tree(self, q, obj, s=None):
        if s is None:
            s = []
        self.lst = planting(q, s)
        for row in self.lst:
            self.trees.add(TreeRiver(obj, row[0], row[1]))
        return self.lst


    def flight_clouds(self):
        self.speed_cloud = [rand(1, 3) for _ in range(5)]
        self.clouds_left.add(Cloud((- self.setting.width_cloud * 2), self.setting.interval_cloud[2],
                                   'img/cloud.png', self.speed_cloud[0]),
                             Cloud((- self.setting.width_cloud * 2), self.setting.interval_cloud[0],
                                   'img/cloud.png', self.speed_cloud[1]),
                             Cloud((- self.setting.width_cloud * 2), self.setting.interval_cloud[4],
                                   'img/cloud.png', self.speed_cloud[2]))
        self.clouds_right.add(Cloud(self.setting.width_screen, self.setting.interval_cloud[3],
                                    'img/cloud.png', self.speed_cloud[3]),
                             Cloud(self.setting.width_screen, self.setting.interval_cloud[1],
                                   'img/cloud.png', self.speed_cloud[4]))


    def run_game(self):
        self.flight_clouds()
        self.list_trees = self.tree(30, 'img/tree.png')
        self.list_trees = self.tree(6, 'img/lake.png', self.list_trees)




        while True:
            self.clock.tick(self.setting.FPS)

            self.screen.blit(self.bg, (0, 0))

            self.trees.draw(self.screen)

            self.clouds_left.draw(self.screen)
            self.clouds_right.draw(self.screen)
            self.clouds_left.update(self.setting.width_screen, 0)
            self.clouds_right.update(-self.setting.width_cloud, 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            pygame.display.update()


if __name__ == '__main__':
    ai = SaveTheForest()
    ai.run_game()