import pygame

class MainC():
    def __init__(self,game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.image_counter = 0
        self.run_r = True
        self.run_r_fast = False
        self.run_l = False
        self.make_jump = False
        self.run_right, self.jumping, self.run_left = [], [], []
        self.character_animation()


    def character_animation(self) -> None:
        for i in range(0,6):
            self.run_right.append(pygame.image.load(f"images\\run_right\\run{i}.png").convert_alpha())

        for i in range(0,6):
            self.run_left.append(pygame.image.load(f"images\\run_left\\run{i}.png").convert_alpha())

        for i in range(0,4):
            self.jumping.append(pygame.image.load(f"images\\jump\\jump{i}.png").convert_alpha())
            self.rect = self.run_right[i].get_rect()
        self.rect.x =self.screen_rect.left + (3 * self.rect.height)
        self.rect.y = self.screen_rect.bottom - (2 * self.rect.height)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        


    def blit_char(self) -> None:
        if self.run_r:
            self.update_anim(number=24, anim_list=self.run_right, divider=6)

        if self.make_jump:
            self.update_anim(number=20, anim_list=self.jumping, divider=5)

        if self.run_l:
            self.update_anim(number=24, anim_list=self.run_left, divider=6)


    def update(self) -> None:
        if self.make_jump:
            self.jump()

        if self.run_r_fast and self.rect.right < self.screen_rect.right:
            self.x += 3
        
        if self.run_l and self.rect.left > self.screen_rect.left:
            self.x -= 12

        self.rect.x = self.x
        self.rect.y = self.y

    def update_anim(self, number: int, anim_list: list, divider: int) -> None:
        if self.image_counter >= number:
                self.image_counter = 0
        self.screen.blit(anim_list[self.image_counter// divider], self.rect)
        self.image_counter += 1

    def position_character(self) -> None:
        self.rect.x =self.screen_rect.left + (3 * self.rect.height)
        self.rect.y = self.screen_rect.bottom - (2 * self.rect.height)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def jump(self):
        self.run_r = False
        self.run_l = False
        if self.settings.jump_count >= -10:
            self.y -= (self.settings.jump_count * abs(self.settings.jump_count)) * 0.5
            self.settings.jump_count -= 1
        else:
            if self.rect.y < self.screen_rect.bottom - (2 * self.rect.height):
                self.y = min((self.screen_rect.bottom - (2 * self.rect.height)),((self.settings.jump_count * abs(self.settings.jump_count)) * 0.5))
                self.settings.jump_count -= 1
            else:
                self.settings.jump_count = 10
                self.make_jump = False
                self.run_r = True

    def cancel_jump(self):
        self.settings.jump_count = 10
        self.make_jump = False
        self.run_r = True
        self.position_character()

    