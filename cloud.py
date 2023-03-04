import pygame
from settings import Settings as sett
from utils import gen_num


class Cloud(pygame.sprite.Sprite):

    def __init__(self, x, y, obj, speed):
        pygame.sprite.Sprite.__init__(self)
        self.setting = sett()
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
                self.rect.y = gen_num((self.setting.height_cloud // 2),
                                      (self.setting.height_screen - self.setting.height_cloud))

        if args[1] == 1:
            if self.rect.x > args[0] - self.setting.width_cloud:
                self.rect.x -= self.speed
            else:
                self.rect.x = self.setting.width_screen
                self.rect.y = gen_num((self.setting.height_cloud // 2),
                                      (self.setting.height_screen - self.setting.height_cloud))


def flight_clouds(group_left, group_right):
    group_left.add(Cloud((- sett().width_cloud * 2), sett().interval_cloud[2], 'img/cloud.png', 2),
                    Cloud((- sett().width_cloud * 2), sett().interval_cloud[0], 'img/cloud.png', 1),
                    Cloud((- sett().width_cloud * 2), sett().interval_cloud[4], 'img/cloud.png', 3))
    group_right.add(Cloud(sett().width_screen, sett().interval_cloud[3], 'img/cloud.png', 2),
                          Cloud(sett().width_screen, sett().interval_cloud[1], 'img/cloud.png', 3))


def light_strike(group_1, group_2, q, ran, time):
    if time % ran == 0:
        cloud = list(group_1)[gen_num(0, q)]
        light = Cloud(cloud.rect.x + 40, cloud.rect.y + 40, 'img/lighter.png', cloud.speed)
        group_2.add(light)
    elif len(group_2) != 0 and time % 40 == 0:
        for row in group_2:
            row.kill()


