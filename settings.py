from random import randint as rand


class Settings:

    def __init__(self):
        # Основные параметры игры
        self.width_screen, self.height_screen = 1200, 600
        self.width_bg_info, self.height_bg_info = self.width_screen - self.width_screen // 6, \
                                                  self.height_screen // 6
        self.width_tree_river, self.height_tree_river = 40, 40
        self.width_hospital_shop, self.height_hospital_shop = 100, 80
        self.width_cloud, self.height_cloud = 80, 80
        self.bg_k = 30
        self.text_k = 400
        self.text_size = 20
        self.FPS = 30
        self.interval_cloud = [rand(self.height_cloud // 2,
                                    self.height_screen - self.height_cloud) for _ in range(5)]
        self.quantity_trees = 30
        self.quantity_lakes = 7
        self.scores = 0
        self.score_up = 500
        self.score_down = 20
        self.lives = 2
        self.num_water = 2
        self.op_water = 2
        self.upgrade_water = 500
        self.upgrade_lives = 1000
        self.max_water = 5
        self.max_lives = 5
