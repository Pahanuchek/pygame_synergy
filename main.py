import pygame

import sys

import random


class SaveTheForest:


    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Save The Forest")

        self.grass = pygame.image.load('img/grass.jpg')
        self.grass = pygame.transform.scale(self.grass, (1200, 600))
        self.screen.blit(self.grass, (0, 0))

        self.tree = pygame.image.load('img/tree.png')
        self.tree = pygame.transform.scale(self.tree, (40, 40))


    def tree_planting(self, q):
        coord_trees = []
        while len(coord_trees) <= q:
            k = random.randint(40, 1160)
            m = random.randint(40, 540)
            if self.control_tree(coord_trees, k, m):
                continue
            else:
                self.screen.blit(self.tree, (k, m))
                coord_trees.append((k, m))
                print(coord_trees)


    def control_tree(self, s, k_tree, m_tree):
        for i,row in enumerate(s):
            if abs(row[0] - k_tree) < 40 and abs(row[1] - m_tree) < 40:
                return True


    def run_game(self):
        self.tree_planting(30)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()


if __name__ == '__main__':
    ai = SaveTheForest()
    ai.run_game()