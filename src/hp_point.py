import pygame
from pygame.sprite import Sprite

class Hp_Point(Sprite):
    def __init__(self,game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.mc = game.MC
        self.image_counter = 0
        self.animlist = list()
        for i in range(0,6):
            self.animlist.append(pygame.image.load(f'images\\heart\\{i}.png').convert_alpha())
            self.rect = self.animlist[i].get_rect()
        self.rect.x = self.screen_rect.centerx
        self.rect.y = self.screen_rect.bottom - (2 * self.mc.rect.height )
        self.image = self.animlist[self.image_counter // 3]

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        if self.image_counter == 24:
            self.image_counter = 0
        self.image = self.animlist[self.image_counter // 4]
        self.image_counter += 1
        
        self.x -= self.settings.speed_char
        self.rect.x = self.x