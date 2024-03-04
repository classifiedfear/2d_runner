import sys

import pygame
from time import sleep
from random import randint, choice


from settings import Settings
from character import MainC
from sounds import Sound
from src.backgrounds import Backgrounds
from enemy import Enemy
from obstacle import Obstacle
from gamestats import GameStats
from buttons import Button
from points import Points
from scoreboard import ScoreBoard
from hp_point import Hp_Point


class Game():
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats(self)
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.BG = Backgrounds(self)
        self.clock = pygame.time.Clock()
        self.MC = MainC(self)
        self.sounds = Sound()
        self.button = Button(self, width=140, height=45)
        self.obstacles = pygame.sprite.Group()
        self.enemylist = list()
        self.points = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.sb = ScoreBoard(self)
        pygame.display.set_caption('XZ')
        self.count_enemy = 0
        self.count_obstacle = 0
        self.bg_count = 0


    def run_game(self) -> None:
        while True:
            self.BG.menu_background()
            self._check_events()
            self.show_buttons()
            if self.stats.game_active:
                self._blit_items()
                self._update_items()
                self.plus_points()
                self.hp_up()
            pygame.display.update()
            self.clock.tick(60)

            
    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos, x = self.screen.get_rect().centerx-50, y= self.screen.get_rect().centery)
                self._check_exit_button(mouse_pos, x = self.screen.get_rect().centerx-50, y= self.screen.get_rect().centery + 100)


    def _check_keydown_events(self,event) -> None:
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.key == pygame.K_p:
            self.pause(msg='Paused! Press "E" to continue',x=self.settings.screen_width/2 - 100,y=self.settings.screen_height/2)
        if event.key == pygame.K_d:
            self.MC.run_r_fast = True
            self.MC.run_l = False
            self.MC.run_r = True
        if event.key == pygame.K_a:
            self.MC.run_l = True
            self.MC.run_r = False
        if event.key == pygame.K_SPACE:
            self.MC.make_jump = True
            if 0 < self.settings.jump_count < 9:
                self.settings.jump_count = 10
                


    def _check_keyup_events(self,event) -> None:
        if event.key == pygame.K_d:
            self.MC.run_r_fast = False
        if event.key == pygame.K_a:
            self.MC.run_l = False
            self.MC.run_r = True

            
    def create_obstacles(self) -> None:
        obstacle = Obstacle(self)
        width = obstacle.rect.width
        current_x = self.settings.screen_width + width
        while current_x < (2* self.settings.screen_width):
            self.create_obstacle(current_x)
            current_x += randint(10, 20) * width
        
            
    def down(self) -> None:
        for obstacle in self.obstacles.sprites().copy():
            if obstacle.rect.colliderect(self.MC.rect):
                self.count_obstacle += 1
            if obstacle.rect.right < self.MC.rect.left:
                self.count_obstacle = 0
        if self.count_obstacle == 5:
            self.stats.hp_left -= 1
            self.sounds.hit()
            self.sb.prep_hp()
            self.count_obstacle = 0
        self.hit()
    

    def create_enemy(self) -> None:
        new_enemy = Enemy(self)        
        self.enemylist.append(new_enemy)


    def _blit_items(self) -> None:
        self.BG.blit_background()
        self.MC.blit_char()
        self.obstacles.draw(self.screen)
        self.points.draw(self.screen)
        self.hearts.draw(self.screen)
        self._update_list_enemy()
        self.sb.show_score()
        self.remove_items()

    def remove_items(self) -> None:
        for obstacle in self.obstacles.sprites().copy():
            if obstacle.rect.right < 0:
                self.obstacles.remove(obstacle)
                self.bg_count += 1
        if not self.obstacles:
            self.create_obstacles()
        for point in self.points.sprites().copy():
            if point.rect.right < 0:
                self.points.remove(point)
        if not self.points:
            self.create_points()
        for heart in self.hearts.sprites().copy():
            if heart.rect.right < 0:
                self.hearts.remove(heart)
        if not self.hearts:
            self.hp()

    def _update_items(self) -> None:
        self.MC.update()
        self.BG.update()
        self.obstacles.update()
        self.points.update()
        self.hearts.update()
        self.change_bg()
        self.down()


    def _update_list_enemy(self) -> None:
        for enemy in self.enemylist.copy():
            enemy.blit()
            enemy.update()
            if enemy.rect.x <= choice([-5000, - 2500]):
                self.enemylist.remove(enemy)
                self.create_enemy()
        self.enemy_obstacle()


    def enemy_obstacle(self) -> None:
        collide = pygame.sprite.groupcollide(self.enemylist, self.obstacles, False, False)
        if collide:
            for enemy in self.enemylist.copy():
                enemy.obstacle = True


    def hit(self) -> None:
        for enemy in self.enemylist:
            if pygame.sprite.collide_rect(self.MC, enemy):
                self.count_enemy += 1
            if enemy.rect.left < self.MC.rect.left:
                self.count_enemy = 0
        if self.count_enemy == 5:
            self.stats.hp_left -= 1
            self.sb.prep_hp()
            self.sounds.hit()
            sleep(0.1)
        if self.stats.hp_left == 0:
            self.lose(game=True)
            

    def _check_play_button(self, mouse_pos: tuple, x: int, y: int) -> None:
        click = pygame.mouse.get_pressed()
        if x < mouse_pos[0] < x + self.button.width and  y < mouse_pos[1] < y + self.button.height and not self.stats.game_active:
            if click[0] == 1 and not self.stats.game_active:
                self.start_game(game=True )
                

    def _check_exit_button(self, mouse_pos: tuple, x: int,y: int) -> None:
        click = pygame.mouse.get_pressed()
        if x < mouse_pos[0] < x + self.button.width and  y < mouse_pos[1] < y + self.button.height and not self.stats.game_active:
            if click[0] == 1 and not self.stats.game_active:
                sys.exit()

    def create_points(self) -> None:
        point = Points(self)
        width = point.rect.width
        current_x = self.settings.screen_width + width
        while current_x < (self.settings.screen_width * 2) :
            self.create_point(current_x)
            current_x += randint(10, 13) * width


    def plus_points(self) -> None:
        for point in self.points.sprites().copy():   
            if point.rect.colliderect(self.MC):
                self.stats.score += self.settings.points
                self.sb.prep_score()
                self.sounds.get_point()
                self.points.remove(point)


    def create_point(self,x_pos: int) -> None:
        new_point = Points(self)
        new_point.x = x_pos
        new_point.y = choice([self.settings.screen_height- 100, self.settings.screen_height -200])
        new_point.rect.x = x_pos
        new_point.rect.y = choice([
            self.settings.screen_height - 240,
            self.settings.screen_height - 180,
            self.settings.screen_height - 300])
        self.points.add(new_point)


    def create_obstacle(self, x_pos: int) -> None:
        new_obstacle = Obstacle(self)
        new_obstacle.x = x_pos
        new_obstacle.rect.x = x_pos
        self.obstacles.add(new_obstacle)


    def lose(self, game: bool = True) -> None:
        self.obstacles.empty()
        self.enemylist.clear()
        self.points.empty()
        self.hearts.empty
        self.sounds.change_track(check=3)
        if game:
            self.stats.reset_stats()
            self.BG.index = 0
        self.bg_count = 0
        self.count_enemy = 0
        self.count_obstacle = 0
        self.stats.game_active= False
        pygame.mouse.set_visible(True)


    def change_bg(self) -> None:
        if self.bg_count == 35 and self.BG.index >= 3:
            self.game_over()
        elif self.bg_count == 35 :
            self.pause(f'Level {self.stats.lvl + 1}! Press "E" to continue!',x=self.settings.screen_width / 2.5 , y=self.settings.screen_height / 2)
            self.lose(game= False)
            self.start_game(game=False)
            self.bg_count = 0
            self.BG.index += 1
            self.stats.lvl += 1
            self.sb.prep_lvl()
            pygame.time.delay(200)


    def pause(self, msg: str, x: int, y: int) -> None:
        paused = True
        while paused:
            self.BG.pause()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

            self.button.prep_msg(msg, x, y)
        
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                paused = False

            pygame.display.update()
            self.clock.tick(60)

    def start_game(self, game: bool = True) -> None:
        self.create_points()
        self.create_obstacles()
        self.create_enemy()
        self.hp()
        self.sb.prep_image()
        self.sounds.change_track(check=1)
        self.MC.cancel_jump()
        if game: 
            self.BG.index = 0
        self.stats.game_active = True
        pygame.mouse.set_visible(False)

    def show_buttons(self) -> None:
        self.button.draw_button(msg='Start game',x=self.screen.get_rect().centerx-50, y=self.screen.get_rect().centery,)
        self.button.draw_button(msg='Exit game',x=self.screen.get_rect().centerx-50, y=self.screen.get_rect().centery + 100)

    def hp(self) -> None:
        hp = Hp_Point(self)
        hp_width = hp.rect.width
        current_x = (self.settings.screen_width + hp_width)
        while current_x < (2 * self.settings.screen_width):
            self.create_hp(x_pos=current_x)
            current_x += choice([50, 100]) * hp_width

    def create_hp(self, x_pos: int) -> None:
        new_hp = Hp_Point(self)
        new_hp.x = x_pos
        new_hp.y = choice([
            self.settings.screen_height - 100, 
            self.settings.screen_height - 200,
        ])
        new_hp.rect.x = x_pos
        new_hp.rect.y = choice([
            self.settings.screen_height - 240,
            self.settings.screen_height - 180,
            self.settings.screen_height - 300,
        ])
        self.hearts.add(new_hp)

    def hp_up(self) -> None:
        for heart in self.hearts.sprites().copy():
            if heart.rect.colliderect(self.MC):
                if self.stats.hp_left < 3:
                    self.stats.hp_left += 1
                    self.sb.prep_hp()
                    self.sounds.get_hp()
                    self.hearts.remove(heart)
                else:
                    self.sounds.get_hp()
                    self.hearts.remove(heart)

    def game_over(self) -> None:
        self.sounds.change_track(check= 2)
        self.pause(msg='Congratulations! You complete the game! Press "Escape" to quit or "E" to start another game!', 
        x=self.settings.screen_width / 4 , y= self.settings.screen_height / 2)
        self.lose(game=True)
        pygame.mouse.set_visible(True)


if __name__ == "__main__":
    xz = Game()
    xz.run_game()
