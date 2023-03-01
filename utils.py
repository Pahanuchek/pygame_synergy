from random import randint as rand

from settings import Settings


setting = Settings()


def planting(q, s):
    coordinate = []
    while len(coordinate) <= q:
        k = rand(setting.width_tree_river, (setting.width_screen - setting.width_tree_river * 2))
        m = rand(setting.width_tree_river, (setting.height_screen - setting.width_tree_river))
        if control(coordinate, k, m) or control(s, k, m):
            continue
        else:
            coordinate.append((k, m))
    return coordinate


def control(s, k_tree, m_tree):
    for i, row in enumerate(s):
        if abs(row[0] - k_tree) < setting.width_tree_river * 2 and \
                abs(row[1] - m_tree) < setting.width_tree_river * 2:
            return True