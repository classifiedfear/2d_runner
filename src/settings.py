import pygame
class Settings():
    def __init__(self):
        self.size = self.screen_width, self.screen_height = 1280, 720
        self.points = 10
        self.chracter_setting()
    def chracter_setting(self) -> None:
        self.speed_char = 8.5
        self.jump_count = 10
        self.enemy_jump_count = 10
        self.direction = 0
        self.hp = 3

