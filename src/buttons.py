import pygame


class Button():
    def __init__(self, game, width: int, height:int):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.sounds = game.sounds
        self.stats = game.stats
        self.text_color = (255, 255, 255)
        self.width, self.height = width, height
        self.inactive_color = (6,57,112)
        self.active_color = (30,129,176)

    def prep_msg(self, msg: str, x: int, y: int, font_size:int=30, font_type: str='fonts\\beer-money12.ttf' ):
        self.font = pygame.font.Font(font_type, font_size)
        self.image = self.font.render(msg, True, self.text_color)
        self.screen.blit(self.image, (x,y))

    def draw_button(self,msg: str, x: int, y: int, font_size: int=30):
        self.mouse_pos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        if x < self.mouse_pos[0] < x + self.width and y < self.mouse_pos[1] < y + self.height:
            pygame.draw.rect(self.screen, self.active_color, (x, y, self.width, self.height))
            
            if self.click[0] == 1 :
                self.sounds.press_button()
                pygame.time.delay(300)
        else: 
            pygame.draw.rect(self.screen, self.inactive_color, (x, y, self.width, self.height))
        

        self.prep_msg(msg, x=x+5, y=y+5, font_size=font_size )
