class GameStats():
    def __init__(self,game):
        self.settings = game.settings
        self.game_active = False
        self.reset_stats()
        
    def reset_stats(self):
        self.score = 0
        self.hp_left = self.settings.hp
        self.lvl = 1