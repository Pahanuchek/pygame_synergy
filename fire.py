import pygame
from settings import Settings
from utils import gen_num


class Fire(pygame.sprite.Sprite):
    def __init__(self, obj, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.setting = Settings()
        self.image = pygame.image.load(obj)
        self.image = pygame.transform.scale(self.image, (self.setting.width_tree_river,
                                                         self.setting.height_tree_river))
        self.rect = self.image.get_rect(center=(x, y))


def fire_go(q, group_1, group_2, time):
    num = gen_num(0, q)
    tree_n = list(group_1)[num]
    fire = Fire('img/fire.png', tree_n.rect.x + 20, tree_n.rect.y + 20)
    group_2.add(fire)
    if time % 30 == 0 and len(group_2) >= 3:
        for row in group_2:
            row.kill()
            break