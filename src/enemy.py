from pygame.sprite import Sprite
import pygame
from random import randint

class Enemy(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.image_counter = 0
        self.mc = game.MC
        self.run_enemy = True
        self.obstacle = False
        self.move_left, self.jump= [], []
        self.choice = randint(0,2)
        if self.choice == 0:
            for i in range(0,4):
                self.jump.append(pygame.image.load(f"images\\enemy_jump\\{i}.png").convert_alpha())
            for i in range(0,5):
                self.move_left.append(pygame.image.load(f"images\\enemy_move_left\\{i}.png").convert_alpha())
                self.rect = self.move_left[i].get_rect()
        elif self.choice == 1:
            for i in range(0,7):
                self.jump.append(pygame.image.load(f"images\\enemy2jump\\{i}.png").convert_alpha())
            for i in range(0,5):
                self.move_left.append(pygame.image.load(f"images\\enemy2\\{i}.png").convert_alpha())
                self.rect = self.move_left[i].get_rect()
        elif self.choice == 2:
            for i in range(0,6):
                self.jump.append(pygame.image.load(f"images\\enemy3jump\\{i}.png").convert_alpha())
            for i in range(0,7):
                self.move_left.append(pygame.image.load(f"images\\enemy3\\{i}.png").convert_alpha())
                self.rect = self.move_left[i].get_rect()

        self.rect.x = self.screen_rect.right - self.rect.height
        self.rect.y = self.screen_rect.bottom - (2 * (self.mc.rect.height ))
    
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blit(self) -> None:
        if self.choice == 0 or self.choice == 1:
            if self.run_enemy:
                if self.image_counter >= 24:
                    self.image_counter = 0
                self.screen.blit(self.move_left[self.image_counter// 6], self.rect)
                self.image_counter += 1
        elif self.choice == 2:
            if self.run_enemy:
                if self.image_counter >= 49:
                    self.image_counter = 0
                self.screen.blit(self.move_left[self.image_counter// 7], self.rect)
                self.image_counter += 1


    def update(self) -> None:
        self.x -= self.settings.speed_char *1.8
        if self.obstacle:
            if self.choice == 0:
                self.make_jump(24,6)
            if self.choice == 1:
                self.make_jump(45,7)
            if self.choice == 2:
                self.make_jump(30,5)
        self.rect.x = self.x
        self.rect.y = self.y
    
    def make_jump(self,counter: int, divider: int,) -> None:
        self.run_enemy = False
        if self.image_counter >= counter:
            self.image_counter = 0
        self.screen.blit(self.jump[self.image_counter // divider], self.rect)
        self.image_counter += 1

        if self.settings.enemy_jump_count >= -10:
            if self.settings.enemy_jump_count > 0:
                self.y -=(self.settings.enemy_jump_count ** 2) // 2
            else:
                self.y +=(self.settings.enemy_jump_count ** 2) // 2
            self.settings.enemy_jump_count -= 1
        else:
            self.settings.enemy_jump_count = 10
            self.run_enemy = True
            self.obstacle = False




