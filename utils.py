from random import randint as rand
from settings import Settings

setting = Settings()


def generate():
    # Рандомное создание координат облаков
    k = rand(setting.width_tree_river, (setting.width_screen - setting.width_tree_river * 2))
    m = rand(setting.width_tree_river, (setting.height_screen - setting.width_tree_river))
    return k, m


def entrance(obj, group):
    # Функция проверки пересечения объектов
    counter = 0
    for row in group:
        if obj.rect.colliderect(row.rect):
            counter += 1
            break
    if counter == 0:
        return True


def gen_num(a, b):
    # Генерация рандомного числа
    num = rand(a, b)
    return num
