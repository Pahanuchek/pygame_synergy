import sys
import pygame
from cloud import Cloud
from static import StaticObject
from settings import Settings
from utils import generate, gen_num, entrance
from helicopter import Helicopter


class SaveTheForest:

    def __init__(self):
        # Инициализация библиотеки pygame
        pygame.init()

        # Инициализация времени, задание данных таймера
        self.clock = pygame.time.Clock()
        self.timer_games = 1
        pygame.time.set_timer(pygame.USEREVENT, 30)

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
        self.hospit = pygame.sprite.Group()
        self.shop_waters = pygame.sprite.Group()
        self.helicopter = pygame.sprite.Group()

        # Задание начального значения клавиш
        self.keys_pos_right = False
        self.keys_pos_left = False
        self.keys_pos_down = False
        self.keys_pos_up = False
        self.keys_pos_space = False

    def keys_position(self):
        # Функция обработки нажатия клавиш
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.keys_pos_left = True
        elif keys[pygame.K_LEFT]:
            self.keys_pos_right = True
        elif keys[pygame.K_DOWN]:
            self.keys_pos_down = True
        elif keys[pygame.K_UP]:
            self.keys_pos_up = True
        elif keys[pygame.K_SPACE]:
            self.keys_pos_space = True

    def rand_tree(self):
        # Создание рандомного расположеных деревьев
        while len(self.trees) <= self.setting.quantity_trees:
            tree = StaticObject('img/tree.png', *generate(),
                                self.setting.width_tree_river, self.setting.height_tree_river)
            if entrance(tree, self.trees):
                if entrance(tree, self.lakes):
                    if entrance(tree, self.hospit):
                        if entrance(tree, self.shop_waters):
                            self.trees.add(tree)
        self.trees.draw(self.screen)

    def fire_tree_go(self):
        # Рандомное возгорание деревьев
        if len(self.fires) <= len(self.trees) and self.timer_games % 150 == 0:
            counter = 0
            num = gen_num(0, len(self.trees) - 1)
            tree_n = list(self.trees)[num]
            fire = StaticObject('img/fire.png', tree_n.rect.x + self.setting.width_tree_river // 2,
                                tree_n.rect.y + self.setting.height_tree_river // 2,
                                self.setting.width_tree_river, self.setting.height_tree_river)
            for fire_i in self.fires:
                if fire.rect.colliderect(fire_i.rect):
                    counter += 1
                    break
            if counter == 0:
                self.fires.add(fire)
        self.fires.draw(self.screen)

    def fire_kill_tree(self):
        # Если дерево за определенное количество времени не было потушено
        # оно сгорает, вычитаются очки
        if len(self.fires) > 0 and self.timer_games % 450 == 0:
            fire = list(self.fires)[0]
            for tree in self.trees:
                if fire.rect.colliderect(tree.rect):
                    tree.kill()
                    fire.kill()
                    self.setting.scores -= self.setting.score_down
        self.fires.draw(self.screen)

    def rand_lake(self):
        # Создание рандомно расположеных озер
        while len(self.lakes) <= self.setting.quantity_lakes:
            lake = StaticObject('img/lake.png', *generate(), self.setting.width_tree_river,
                                self.setting.height_tree_river)
            if entrance(lake, self.trees):
                if len(self.lakes) == 0:
                    self.lakes.add(lake)
                elif entrance(lake, self.lakes):
                    self.lakes.add(lake)
        self.lakes.draw(self.screen)

    def create_hospital(self):
        # Создание рандомного расположенного госпиталя
        while len(self.hospit) < 1:
            hospital = StaticObject('img/hospital.png', *generate(), self.setting.width_hospital_shop,
                                    self.setting.height_hospital_shop)
            if entrance(hospital, self.trees):
                if entrance(hospital, self.lakes):
                    self.hospit.add(hospital)
        self.hospit.draw(self.screen)

    def create_shop(self):
        # Создание рандомного расположения магазина
        while len(self.shop_waters) < 1:
            shop = StaticObject('img/shop.png', *generate(), self.setting.width_hospital_shop,
                                self.setting.height_hospital_shop)
            if entrance(shop, self.trees):
                if entrance(shop, self.lakes):
                    if entrance(shop, self.hospit):
                        self.shop_waters.add(shop)
        self.shop_waters.draw(self.screen)

    def flight_clouds(self):
        # Создание двух групп облаков
        for _ in range(3):
            self.clouds_left.add(Cloud(*generate(), 'img/cloud.png', gen_num(1, 4)))
            self.clouds_right.add(Cloud(*generate(), 'img/cloud.png', gen_num(1, 4)))

    def light_strike(self, group_1, group_2):
        #  Создание молний
        if self.timer_games % gen_num(100, 150) == 0:
            cloud = list(group_1)[gen_num(0, 2)]
            light = Cloud(cloud.rect.x + self.setting.width_cloud / 2,
                          cloud.rect.y + self.setting.height_cloud / 2, 'img/lighter.png', cloud.speed)
            group_2.add(light)
        elif len(group_2) != 0 and self.timer_games % 40 == 0:
            for row in group_2:
                row.kill()

    def light_cloud_display(self):
        # Отображение облаков и молний левой группы на карте
        self.clouds_left.draw(self.screen)
        self.clouds_left.update(self.setting.width_screen, 0)
        self.lighter_left.draw(self.screen)
        self.lighter_left.update(self.setting.width_screen, 0)
        self.light_strike(self.clouds_left, self.lighter_left)
        # Создание облаков и молний правой группе на карте
        self.clouds_right.draw(self.screen)
        self.clouds_right.update(-self.setting.width_cloud, 1)
        self.lighter_right.draw(self.screen)
        self.lighter_right.update(self.setting.width_cloud, 1)
        self.light_strike(self.clouds_right, self.lighter_right)

    def in_helicopter(self):
        # Инициализация вертолета
        helic = Helicopter('img/helicopter.png', 600, 300)
        self.helicopter.add(helic)

    def move_helicopter(self):
        # Вывод вертолета на экран, перемещение его клавишами
        self.helicopter.draw(self.screen)
        self.helicopter.update(self.keys_pos_left, self.keys_pos_right,
                               self.keys_pos_down, self.keys_pos_up)

    def exting_tree(self):
        # Тушение горящего дерева, начисление очков
        for hel in self.helicopter:
            for fire in self.fires:
                if hel.rect.colliderect(fire.rect) and self.keys_pos_space:
                    fire.kill()
                    self.setting.scores += self.setting.score_up

    def live_up_down(self):
        # Отнимает жизнь у вертолета если по нему ударила молния
        for hel in self.helicopter:
            for light in self.lighter_left:
                if hel.rect.colliderect(light.rect):
                    self.setting.lives -= 1
            for right in self.lighter_right:
                if hel.rect.colliderect(right.rect):
                    self.setting.lives -= 1

    def draw_text(self, text, x):
        # Функция обработки текста
        font = pygame.font.Font(None, 50)
        text_surface = font.render(text, True, (0, 20, 15))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, 20)
        self.screen.blit(text_surface, text_rect)

    def input_info(self):
        # Отображение статистической и игровой информации
        self.draw_text(str(f'Очки: {self.setting.scores}'), 600)
        self.draw_text(str(f'Жизни: {self.setting.lives}'), 800)

    def control_event(self):
        # Задание таймера, контроль завершения игры
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.timer_games += 1
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run_game(self):
        # Основной цикл игры
        self.flight_clouds()
        self.in_helicopter()

        while True:
            self.clock.tick(self.setting.FPS)
            self.screen.blit(self.bg, (0, 0))
            self.keys_position()
            self.rand_tree()
            self.rand_lake()
            self.create_hospital()
            self.create_shop()
            self.fire_tree_go()
            self.fire_kill_tree()
            self.move_helicopter()
            self.exting_tree()
            self.light_cloud_display()
            self.input_info()
            self.control_event()
            pygame.display.update()


if __name__ == '__main__':
    ai = SaveTheForest()
    ai.run_game()
