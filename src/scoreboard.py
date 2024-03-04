import pygame

class ScoreBoard():
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = game.stats
        self.settings = game.settings

        self.font = pygame.font.Font('fonts/beer-money12.ttf', 48)
        self.text_color = (255,255,255)

        self.prep_image()

    def prep_image(self):
        self.prep_score()
        self.prep_hp()
        self.prep_lvl()


    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = f'{rounded_score:,}'
        self.score_image = self.font.render(score_str,True, self.text_color)

    def prep_hp(self):
        self.hp = pygame.sprite.Group()
        for num_hp in range(self.stats.hp_left):
            hp = HP(self.game)
            hp.rect.x = 10 + num_hp * hp.rect.width
            hp.rect.y = 20
            self.hp.add(hp)
    
    def show_score(self):
        self.screen.blit(self.score_image, (self.screen_rect.centerx, self.screen_rect.top))
        self.screen.blit(self.lvl_image, (self.screen_rect.width - 50, self.screen_rect.top))
        self.hp.draw(self.screen)

    def prep_lvl(self):
        lvl_str= str(self.stats.lvl)
        self.lvl_image = self.font.render(lvl_str,True, self.text_color)

class HP(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('images/aw.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.screen_rect.x
        self.screen_rect.y = self.screen_rect.y
        self.screen.blit(self.image, self.rect)