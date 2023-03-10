import shelve
import sys
import pygame

from button import Button
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

        # Загрузка музыкальных файлов
        self.fire_sound = pygame.mixer.Sound('sounds/fire.mp3')
        self.fire_del_sound = pygame.mixer.Sound('sounds/fire_del.mp3')
        self.water_sound = pygame.mixer.Sound('sounds/water.mp3')
        self.die_tree_sound = pygame.mixer.Sound('sounds/die_tree.mp3')
        self.upgrade_sound = pygame.mixer.Sound('sounds/upgrade_music.mp3')
        self.rec_liv_sound = pygame.mixer.Sound('sounds/lives.mp3')
        self.light_sound = pygame.mixer.Sound('sounds/light.mp3')
        self.down_live_sound = pygame.mixer.Sound('sounds/down_live.mp3')

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
        self.bg_inform = pygame.sprite.Group()

        # Стартовые условия
        self.create = True
        self.save_s = True
        self.loading = True
        self.start = True
        self.stopped = True
        self.paused = True

        # Задание начального значения клавиш
        self.keys_pos_right = False
        self.keys_pos_left = False
        self.keys_pos_down = False
        self.keys_pos_up = False
        self.keys_pos_space = False
        self.keys_pause = False
        self.pos_mouse = False

    def helicopter_music(self):
        # Фоновый звук вертолета
        pygame.mixer.music.load('sounds/helicopter.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)

    def chek_keydown_events(self, event):
        # Функция обработки нажатия клавиш
        if event.key == pygame.K_RIGHT:
            self.keys_pos_left = True
        elif event.key == pygame.K_LEFT:
            self.keys_pos_right = True
        elif event.key == pygame.K_DOWN:
            self.keys_pos_down = True
        elif event.key == pygame.K_UP:
            self.keys_pos_up = True
        elif event.key == pygame.K_SPACE:
            self.keys_pos_space = True
        elif event.key == pygame.K_ESCAPE:
            self.keys_pause = True

    def chek_keyup_events(self, event):
        # Функция обработки отжатых клавиш
        if event.key == pygame.K_RIGHT:
            self.keys_pos_left = False
        elif event.key == pygame.K_LEFT:
            self.keys_pos_right = False
        elif event.key == pygame.K_DOWN:
            self.keys_pos_down = False
        elif event.key == pygame.K_UP:
            self.keys_pos_up = False
        elif event.key == pygame.K_SPACE:
            self.keys_pos_space = False
        elif event.key == pygame.K_ESCAPE:
            self.keys_pause = False

    def buttons(self, height, func, msg, flag):
        # Функция создания кнопок
        button = Button(self.setting.width_screen // 2 - self.setting.width_buttom // 2,
                        height, self.setting.width_buttom,
                        self.setting.height_buttom, msg, flag)
        button.process(self.screen, func)

    def first_game(self):
        # Условия первого запуска игры
        while self.create:
            self.control_event()
            self.draw_text('Save The Forest', self.setting.width_screen // 2,
                           self.setting.height_screen // 3, self.setting.text_size_score * 5, 'font.ttf')
            self.buttons(self.setting.height_screen // 2, self.new_game, 'Play', self.pos_mouse)
            self.buttons(self.setting.height_screen // 1.5, self.exit_game, 'Exit', self.pos_mouse)
            self.buttons(self.setting.height_screen // 1.71, self.load, 'Load game', self.pos_mouse)
            pygame.display.update()

    def draw_obj(self):
        # Вывод нециклирующихся объектов
        if self.start == True:
            self.flight_clouds()
            self.in_helicopter()
            self.info_bg()
            self.helicopter_music()
            self.start = False

    def new_game(self):
        # Запуск первого цикла игры
        self.create = False
        self.run_game()

    def pause(self):
        # Обработка событий при паузе
        if self.keys_pause:
            while self.paused:
                self.control_event()
                self.draw_text('Paused!', self.setting.width_screen // 2,
                               self.setting.height_screen // 3, self.setting.text_size_score * 3, 'font.ttf')
                self.buttons(self.setting.height_screen // 2, self.in_pause, 'Continue', self.pos_mouse)
                self.buttons(self.setting.height_screen // 1.71, self.saves, 'Save game', self.pos_mouse)
                self.buttons(self.setting.height_screen // 1.5, self.exit_game, 'Exit', self.pos_mouse)
                pygame.display.update()

    def saves(self):
        # Сохранение игры
        if self.save_s == True:
            self.s_save_lst = [self.helicopter, self.clouds_left, self.clouds_right, self.lighter_left,
                               self.lighter_right, self.trees, self.lakes, self.hospit, self.shop_waters, self.fires]
            self.a_save_num = [self.setting.scores, self.setting.lives, self.setting.num_water, self.setting.op_water]
            self.data = [[] for i in range(len(self.s_save_lst))]
            for i in range(len(self.data)):
                for obj in self.s_save_lst[i]:
                    self.data[i].append(obj.rect)
            print(self.helicopter)
            self.data.append(self.a_save_num)
            print('w', self.data)
            with shelve.open('level') as lvl:
                lvl['a'] = self.data
            lvl.close()
            self.save_s = False

    def load(self):
        # Загрузка игры
        if self.loading == True:
            with shelve.open('level') as lvl:
                state = lvl.get('a')
                self.setting.scores = state[-1][0]
                self.setting.lives = state[-1][1]
                self.setting.num_water = state[-1][2]
                self.setting.op_water = state[-1][3]
                del state[-1]
                self.group_load(state[0], Helicopter, 'img/helicopter.png', self.helicopter)
                self.group_load(state[1], Cloud, 'img/cloud.png', self.clouds_left, gen_num(1,4))
                self.group_load(state[2], Cloud, 'img/cloud.png', self.clouds_right, gen_num(1,4))
                self.group_load(state[3], Cloud, 'img/cloud.png', self.lighter_left, gen_num(1,4))
                self.group_load(state[4], Cloud, 'img/cloud.png', self.lighter_right, gen_num(1,4))
                self.group_load(state[5], StaticObject, 'img/tree.png', self.trees,
                                self.setting.width_tree_river, self.setting.height_tree_river)
                self.group_load(state[6], StaticObject, 'img/lake.png', self.lakes,
                                self.setting.width_tree_river, self.setting.height_tree_river)
                self.group_load(state[7], StaticObject, 'img/hospital.png', self.hospit,
                                self.setting.width_hospital_shop, self.setting.height_hospital_shop)
                self.group_load(state[8], StaticObject, 'img/shop.png', self.shop_waters,
                                self.setting.width_hospital_shop, self.setting.height_hospital_shop)
                self.group_load(state[9], StaticObject, 'img/fire.png',
                                self.fires, self.setting.width_tree_river, self.setting.height_tree_river)
            self.loading = False
            self.start = False
            self.create = False
            self.run_game()

    def group_load(self, lst, cl, img, grup, *args):
        # Формирование груп при загрузке игры
        if len(lst) != 0 and cl == Helicopter:
            for i in range(len(lst)):
                object = cl(img, 0, 0)
                object.rect = lst[i]
                grup.add(object)
        elif len(lst) != 0 and cl == Cloud:
            for i in range(len(lst)):
                object = cl(0, 0, img, args[0])
                object.rect = lst[i]
                grup.add(object)
        elif len(lst) != 0 and cl == StaticObject:
            for i in range(len(lst)):
                object = cl(img, 0, 0, args[0], args[1])
                object.rect = lst[i]
                grup.add(object)

    def in_pause(self):
        # Выход из паузы
        self.paused = False

    def game_overs(self):
        # Обработка событий при проигрыше
        if self.setting.lives <= 0:
            while self.stopped:
                self.control_event()
                self.draw_text('Game over!', self.setting.width_screen // 2,
                               self.setting.height_screen // 3, self.setting.text_size_score * 3, 'font.ttf')
                self.buttons(self.setting.height_screen // 2, self.rest_new_game, 'new game', self.pos_mouse)
                self.buttons(self.setting.height_screen // 1.5, self.exit_game, 'exit', self.pos_mouse)
                pygame.display.update()

    def exit_game(self):
        # Выход из игры
        pygame.quit()
        sys.exit()

    def rest_new_game(self):
        # Создание новой игры при проигрыше
        self.stopped = False
        SaveTheForest().run_game()

    def rand_tree(self):
        # Создание рандомного расположеных деревьев
        while len(self.trees) <= self.setting.quantity_trees:
            tree = StaticObject('img/tree.png', *generate(),
                                self.setting.width_tree_river, self.setting.height_tree_river)
            if entrance(tree, self.trees):
                if entrance(tree, self.lakes):
                    if entrance(tree, self.hospit):
                        if entrance(tree, self.shop_waters):
                            if entrance(tree, self.bg_inform):
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
                self.fire_sound.play()
                self.fires.add(fire)
        self.fires.draw(self.screen)

    def fire_kill_tree(self):
        # Если дерево за определенное количество времени не было потушено
        # оно сгорает, вычитаются очки
        if len(self.fires) > 0 and self.timer_games % 450 == 0:
            fire = list(self.fires)[0]
            for tree in self.trees:
                if fire.rect.colliderect(tree.rect):
                    self.die_tree_sound.play()
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
                    if entrance(lake, self.bg_inform):
                        self.lakes.add(lake)
        self.lakes.draw(self.screen)

    def create_hospital(self):
        # Создание рандомного расположенного госпиталя
        while len(self.hospit) < 1:
            hospital = StaticObject('img/hospital.png', *generate(), self.setting.width_hospital_shop,
                                    self.setting.height_hospital_shop)
            if entrance(hospital, self.trees):
                if entrance(hospital, self.lakes):
                    if entrance(hospital, self.bg_inform):
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
                        if entrance(shop, self.bg_inform):
                            self.shop_waters.add(shop)
        self.shop_waters.draw(self.screen)

    def flight_clouds(self):
        # Создание двух групп облаков
        for _ in range(self.setting.quantity_clouds):
            self.clouds_left.add(Cloud(*generate(), 'img/cloud.png', gen_num(1, 4)))
            self.clouds_right.add(Cloud(*generate(), 'img/cloud.png', gen_num(1, 4)))

    def light_strike(self, group_1, group_2):
        #  Создание молний
        if self.timer_games % gen_num(100, 150) == 0:
            cloud = list(group_1)[gen_num(0, 2)]
            light = Cloud(*cloud.rect.center, 'img/lighter.png', cloud.speed)
            self.light_sound.play()
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
        self.lighter_right.update(-self.setting.width_cloud, 1)
        self.light_strike(self.clouds_right, self.lighter_right)

    def in_helicopter(self):
        # Инициализация вертолета
        helic = Helicopter('img/helicopter.png', self.setting.width_screen // 2,
                           self.setting.height_screen // 2)
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
                if fire.rect.collidepoint(hel.rect.center) and self.keys_pos_space\
                        and self.setting.num_water > 0:
                    self.fire_del_sound.play()
                    self.setting.num_water -= 1
                    fire.kill()
                    self.setting.scores += self.setting.score_up

    def set_water(self):
        # Набор воды
        for hel in self.helicopter:
            for lake in self.lakes:
                if lake.rect.collidepoint(hel.rect.center) and self.keys_pos_space and \
                        self.setting.num_water < self.setting.op_water:
                    self.water_sound.play()
                    self.setting.num_water += 1
                    pygame.time.delay(50)

    def upgrade_water(self):
        # Увеличение емкостей воды
        for hel in self.helicopter:
            for shop in self.shop_waters:
                if shop.rect.collidepoint(hel.rect.center) and self.keys_pos_space and \
                        self.setting.op_water < self.setting.max_water and\
                        self.setting.scores > self.setting.upgrade_water:
                    self.upgrade_sound.play()
                    self.setting.op_water += 1
                    pygame.time.delay(50)
                    self.setting.scores -= self.setting.upgrade_water

    def upgrade_live(self):
        # Увеличение жизней
        for hel in self.helicopter:
            for hos in self.hospit:
                if hos.rect.collidepoint(hel.rect.center) and self.keys_pos_space and \
                        self.setting.lives < self.setting.max_lives and\
                        self.setting.scores > self.setting.upgrade_lives:
                    self.rec_liv_sound.play()
                    self.setting.lives = 100
                    pygame.time.delay(50)
                    self.setting.scores -= self.setting.upgrade_lives

    def live_down(self):
        # Отнимает жизнь у вертолета если по нему ударила молния
        for hel in self.helicopter:
            for light in self.lighter_left:
                if hel.rect.colliderect(light.rect):
                    self.down_live_sound.play()
                    self.setting.lives -= 1
            for right in self.lighter_right:
                if hel.rect.colliderect(right.rect):
                    self.down_live_sound.play()
                    self.setting.lives -= 1

    def info_bg(self):
        # Рамка информации
        bg_info = StaticObject('img/bg_info.png', self.setting.bg_k * 20, self.setting.bg_k,
                               self.setting.bg_k * 20, self.setting.bg_k)
        self.bg_inform.add(bg_info)

    def draw_text(self, text, x, y, size, style):
        # Функция обработки текста
        font = pygame.font.Font(style, size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def input_info(self):
        # Отображение статистической и игровой информации
        self.bg_inform.draw(self.screen)
        self.draw_text(str(f'Количество емкостей воды: {self.setting.num_water}'
                           f'/{self.setting.op_water}'), self.setting.text_k * 1.5,
                       self.setting.text_size_score * 1.5, self.setting.text_size_score, None)
        self.draw_text(str(f'Очки: {self.setting.scores}'), self.setting.text_k,
                       self.setting.text_size_score * 1.5, self.setting.text_size_score, None)
        self.draw_text(str(f'Жизни: {self.setting.lives}/{self.setting.max_lives}'),
                       self.setting.text_k * 2, self.setting.text_size_score * 1.5,
                       self.setting.text_size_score, None)

    def control_event(self):
        # Задание таймера, контроль завершения игры
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.timer_games += 1
            elif event.type == pygame.KEYDOWN:
                self.chek_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.chek_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button:
                    self.pos_mouse = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button:
                    self.pos_mouse = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run_game(self):
        # Основной функция игры
        self.first_game()
        self.draw_obj()
        # self.flight_clouds()
        # self.in_helicopter()
        # self.info_bg()
        # self.helicopter_music()

        while True:
            # Основной цикл игры
            self.clock.tick(self.setting.FPS)
            self.screen.blit(self.bg, (0, 0))
            self.rand_tree()
            self.rand_lake()
            self.create_hospital()
            self.create_shop()
            self.fire_tree_go()
            self.fire_kill_tree()
            self.move_helicopter()
            self.exting_tree()
            self.set_water()
            self.upgrade_water()
            self.upgrade_live()
            self.live_down()
            self.light_cloud_display()
            self.input_info()
            self.control_event()
            self.game_overs()
            self.pause()
            pygame.display.update()


if __name__ == '__main__':
    ai = SaveTheForest()
    ai.run_game()