import pygame
from settings import Settings
from utils import entrance


class Tree(pygame.sprite.Sprite):
    def __init__(self, obj, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.setting = Settings()
        self.image = pygame.image.load(obj)
        self.image = pygame.transform.scale(self.image, (self.setting.width_tree_river,
                                                         self.setting.height_tree_river))
        self.rect = self.image.get_rect(center=(x, y))


def tree(group, n, m):
    if len(group) == 0:
        group.add(Tree('img/tree.png', n, m))
    else:
        tree = Tree('img/tree.png', n, m)
        if entrance(tree, group):
            group.add(tree)




