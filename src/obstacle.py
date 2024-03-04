import pygame
from pygame.sprite import Sprite

class Obstacle(Sprite):
    def __init__(self,game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        self.image = pygame.image.load('images/2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.settings.screen_width - (2*self.rect.width)
        self.rect.y = self.screen_rect.bottom - (self.rect.width + 60)
        
        self.x = float(self.rect.x)

        self.right= False
        self.left = False

    def update(self):
        self.x -= self.settings.speed_char       
        self.rect.x = self.x


