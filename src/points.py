import pygame
from pygame.sprite import Sprite

class Points(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.mc = game.MC
        self.image_counter = 0
        self.animpoints = []
        for i in range(0, 10):
            self.animpoints.append(pygame.image.load(f'images\\points\\{i}.png').convert_alpha())
            self.rect = self.animpoints[i].get_rect()
        self.rect.x = self.screen_rect.centerx
        self.rect.y = self.screen_rect.bottom - (2 * self.mc.rect.height )
        self.image = self.animpoints[self.image_counter//2]
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def update(self):
        if self.image_counter == 18:
            self.image_counter = 0
        self.image = self.animpoints[self.image_counter//2]
        self.image_counter += 1
        
        self.x -= self.settings.speed_char
        self.rect.x = self.x

