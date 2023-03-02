from random import randint as rand

from settings import Settings


setting = Settings()

def generate():
    k = rand(setting.width_tree_river, (setting.width_screen - setting.width_tree_river * 2))
    m = rand(setting.width_tree_river, (setting.height_screen - setting.width_tree_river))
    return k, m

def entrance(obj, group):
    for row in group:
        if row.rect.colliderect(obj.rect) != True:
            return True


