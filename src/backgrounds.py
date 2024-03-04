import pygame 

class Backgrounds:
    def __init__(self, game):
        self.screen = game.screen
        self.settings = game.settings
        self.index = 0
        self.pause_img = pygame.transform.scale(pygame.image.load('images/bg/bg5.png').convert(), (self.screen.get_size()))
        self.main = pygame.transform.scale(pygame.image.load('images/bg/0.png').convert(), (self.screen.get_size()))
        self.bg = [pygame.transform.scale(pygame.image.load('images/bg/bg1.png').convert(), (self.screen.get_size())),
                   pygame.transform.scale(pygame.image.load('images/bg/bg2.png').convert(), (self.screen.get_size())),
                   pygame.transform.scale(pygame.image.load('images/bg/bg3.png').convert(), (self.screen.get_size())),
                   pygame.transform.scale(pygame.image.load('images/bg/bg4.png').convert(), (self.screen.get_size())), ]

        self.bg_x = 0
        self.bg_y = 0


    def blit_background(self):
        self.screen.blit(self.bg[self.index],(self.bg_x, self.bg_y))
        self.screen.blit(self.bg[self.index],(self.bg_x + self.settings.screen_width, self.bg_y))
        if self.bg_x <= -self.settings.screen_width:
            self.bg_x = 0


    def menu_background(self):
        self.screen.blit(self.main,(0, 0))

    def pause(self):
        self.screen.blit(self.pause_img, (0,0))

    def update(self):
        self.bg_x -= self.settings.speed_char

