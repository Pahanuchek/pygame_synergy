import pygame
import sys
from cloud import *
from tree import *
from fire import *
from lake import lake
from utils import generate, entrance, gen_num
from settings import Settings


class SaveTheForest:

    def __init__(self):
        # Инициализация библиотеки pygame
        pygame.init()

        # Инициализация времени, задание данных таймера
        self.clock = pygame.time.Clock()
        self.timer_games = 1
        pygame.time.set_timer(pygame.USEREVENT, 60)

        self.setting = Settings()
        # Создание игрового окна заданного размера, создание подписи названия игры
        self.screen = pygame.display.set_mode((self.setting.width_screen, self.setting.height_screen))
        pygame.display.set_caption("Save The Forest")

        # Загрузка и трансформация фонового рисунка под нужный размер и вывод его на экран
        self.bg = pygame.image.load('img/bg.jpg')
        self.bg = pygame.transform.scale(self.bg, (self.setting.width_screen, self.setting.height_screen))
        self.screen.blit(self.bg, (0, 0))

        # Создание логотипа игры
        self.icon = pygame.image.load('img/icon.jpg')
        self.icon.set_colorkey((255, 255, 255))
        pygame.display.set_icon(self.icon)

        # Создание групп объектов
        self.clouds_left = pygame.sprite.Group()
        self.clouds_right = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.fires = pygame.sprite.Group()
        self.lakes = pygame.sprite.Group()
        self.lighter_left = pygame.sprite.Group()
        self.lighter_right = pygame.sprite.Group()


    def run_game(self):
        # Функция создания облаков, и объединения их в левую и правую группу
        flight_clouds(self.clouds_left, self.clouds_right)

        while True:
            # Задает частоту обновления нашего основного цикла
            self.clock.tick(self.setting.FPS)
            # Задает основной задний фон в виде травы
            self.screen.blit(self.bg, (0, 0))

            # Создание рандомного расположения деревьев
            while len(self.trees) <= 30:
                tree(self.trees, *generate())
            self.trees.draw(self.screen)

            # Создание рандомного расположение озер
            while len(self.lakes) <= 7:
                lake(self.trees, self.lakes, *generate())
            self.lakes.draw(self.screen)

            # Создание рандомного возгарания деревьев
            if self.timer_games % 40 == 0 and len(self.fires) <= len(self.trees):
                    fire_go(len(self.trees) - 1, self.trees, self.fires, self.timer_games )
            self.fires.draw(self.screen)

            # Создание облаков левой группы на карте
            self.clouds_left.draw(self.screen)
            self.clouds_left.update(self.setting.width_screen, 0)
            # Создание полета облаков слева направо
            self.lighter_left.draw(self.screen)
            self.lighter_left.update(self.setting.width_screen, 0)
            # Создание рандомно появляющейся и пропадающей молнии для левой группы облаков
            light_strike(self.clouds_left, self.lighter_left, 2, gen_num(100, 150), self.timer_games)

            # Создание облаков правой группе на карте
            self.clouds_right.draw(self.screen)
            self.clouds_right.update(-self.setting.width_cloud, 1)
            # Создание полета облаков справа налево
            self.lighter_right.draw(self.screen)
            self.lighter_right.update(self.setting.width_cloud, 1)
            # Создание рандомно появляющейся и пропадающей молнии для правой группы облаков
            light_strike(self.clouds_right, self.lighter_right, 1, gen_num(100, 150), self.timer_games)

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.timer_games += 1
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


if __name__ == '__main__':
    ai = SaveTheForest()
    ai.run_game()