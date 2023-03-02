from random import randint as rand

class Settings:

    def __init__(self):
        self.width_screen, self.height_screen = 1200, 600

        self.width_tree_river, self.height_tree_river = 40, 40

        self.width_cloud, self.height_cloud = 80, 80

        self.FPS = 20

        self.interval_cloud = [rand(self.height_cloud // 2,
                                    self.height_screen - self.height_cloud) for _ in range(5)]


