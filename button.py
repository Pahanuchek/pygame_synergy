import pygame


class Button():
    def __init__(self, x, y, width, height, button_text, one_press=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.one_press = one_press
        self.already_pressed = False
        self.fill_color = {
            'normal': '#ffffff',
            'hover': '#666666'
        }
        font = pygame.font.Font('font.ttf', 30)

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button_surf = font.render(button_text, True, (20, 20, 20))
        self.sound_mouse = pygame.mixer.Sound('sounds/mouse.mp3')

    def process(self, disp, func):
        mouse_pos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_color['normal'])
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_color['hover'])
            if self.one_press:
                self.sound_mouse.play()
                func()

        self.button_surface.blit(self.button_surf, [
            self.button_rect.width / 2 - self.button_surf.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_surf.get_rect().height / 2
        ])

        disp.blit(self.button_surface, self.button_rect)
        pygame.draw.rect(disp, (0, 0, 0),
                         (self.x, self.y, self.width, self.height), 2)