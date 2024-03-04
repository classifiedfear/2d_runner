import pygame
class Sound:
    def __init__(self):
        self.main_theme = 'sounds\\a new beginning.wav'
        self.music = 'sounds\\battleThemeA.wav'
        self.game_over = 'sounds\\game_over.wav'
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        self.play_music(self.main_theme, -1, 1)

    def press_button(self) -> None:
        pygame.mixer.Sound('sounds/interface-124464.wav').play()

    def hit(self) -> None:
        pygame.mixer.Sound('sounds/zvuk-urona-v-majnkraft.wav').play()

    def get_point(self) -> None:
        pygame.mixer.Sound('sounds/zvuk-vyibivaniya-monetyi-iz-igryi-super-mario-30119.wav').play()

    def check_button(self) -> None:
        pygame.mixer.Sound('sounds/button-124476.wav').play()

    def get_hp(self) -> None:
        pygame.mixer.Sound('sounds/potion-3.wav').play()

    def play_music(self, music: str, loop: int, volume: int) -> None:
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(loop)
        pygame.mixer.music.set_volume(volume)
 
    def change_track(self,check: int) -> None:
        pygame.mixer.music.pause()
        pygame.mixer.music.stop()
        if check == 1:
            self.play_music(self.music, -1, 0.3)
        if check == 2:
            self.play_music(self.game_over,-1, 1)
        if check == 3:
            self.play_music(self.main_theme,-1, 1)