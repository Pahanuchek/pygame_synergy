from random import randint as rand

import pygame

import sys

from cloud import Cloud

from tree import Tree

from fire import Fire

from lake import Lake

from utils import generate, entrance

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
        self.icon.set_colorkey((255, 255, 255))
        pygame.display.set_icon(self.icon)

        self.clouds_left = pygame.sprite.Group()
        self.clouds_right = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.fires = pygame.sprite.Group()
        self.lakes = pygame.sprite.Group()

    def tree(self, n, m):
        if len(self.trees) == 0:
            self.trees.add(Tree('img/tree.png', n, m))
        else:
            tree = Tree('img/tree.png', n, m)
            if entrance(tree, self.trees):
                self.trees.add(tree)


    def lake(self, n, m):
        lake = Lake('img/lake.png', n, m)
        if entrance(lake, self.trees):
            if len(self.lakes) == 0:
                self.lakes.add(lake)
            elif entrance(lake, self.lakes):
                self.lakes.add(lake)




    def fire_k(self, q):
        num = rand(0, q)
        tree_n = list(self.trees)[num]
        fire = Fire('img/fire.png', 0, 0)
        fire.rect.x = tree_n.rect.x
        fire.rect.y = tree_n.rect.y
        self.fires.add(fire)



    def flight_clouds(self):
        speed_cloud = [rand(1, 5) for _ in range(5)]
        self.clouds_left.add(Cloud((- self.setting.width_cloud * 2), self.setting.interval_cloud[2],
                                   'img/cloud.png', speed_cloud[0]),
                             Cloud((- self.setting.width_cloud * 2), self.setting.interval_cloud[0],
                                   'img/cloud.png', speed_cloud[1]),
                             Cloud((- self.setting.width_cloud * 2), self.setting.interval_cloud[4],
                                   'img/cloud.png', speed_cloud[2]))
        self.clouds_right.add(Cloud(self.setting.width_screen, self.setting.interval_cloud[3],
                                    'img/cloud.png', speed_cloud[3]),
                             Cloud(self.setting.width_screen, self.setting.interval_cloud[1],
                                   'img/cloud.png', speed_cloud[4]))


    def run_game(self):
        self.flight_clouds()

        while True:

            self.clock.tick(self.setting.FPS)
            self.screen.blit(self.bg, (0, 0))

            while len(self.trees) <= 30:
                self.tree(*generate())
            self.trees.draw(self.screen)

            while len(self.lakes) <= 7:
                self.lake(*generate())
            self.lakes.draw(self.screen)

            self.fire_k(7)
            self.fires.draw(self.screen)


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