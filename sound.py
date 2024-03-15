import pygame as pg
from laser import LaserType
import time


class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.001)
        alienlaser_sound = pg.mixer.Sound('sounds/alienlaser.wav')
        photontorpedo_sound = pg.mixer.Sound('sounds/photon_torpedo.wav')
        gameover_sound = pg.mixer.Sound('sounds/gameover.wav')

        explosion_sound = pg.mixer.Sound('sounds/explosion.wav')  
        powerup_sound = pg.mixer.Sound('sounds/powerup.wav')
        bg_music = pg.mixer.Sound('sounds/backgroundmusic.wav')
        nextlevel_sound = pg.mixer.Sound('sounds/nextlevel.wav')
        self.sounds = {'alienlaser': alienlaser_sound, 'photontorpedo': photontorpedo_sound,
                       'gameover': gameover_sound,'explosion': explosion_sound, 'powerup': powerup_sound, 'backgroundmusic': bg_music, 'nextlevel': nextlevel_sound}



    def play_explosion(self):
        pg.mixer.Sound.play(self.sounds['explosion'])

    def play_powerup(self):
        pg.mixer.Sound.play(self.sounds['powerup'])

    def play_bg(self):
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        pg.mixer.music.stop()

    def shoot_laser(self, type):
        pg.mixer.Sound.play(self.sounds['alienlaser' if type == LaserType.ALIEN else 'photontorpedo'])

    def gameover(self): 
        self.stop_bg() 
        gameover_sound = pg.mixer.Sound('sounds/gameover.wav')
        gameover_sound.play()
        time.sleep(2.8)
