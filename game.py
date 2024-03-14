import pygame as pg
from settings import Settings
import game_functions as gf
from laser import Lasers, LaserType
from alien_fleet import AlienFleet
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from vector import Vector
from barrier import Barriers
import sys


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self)  
                                    
        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.alien_fleet = AlienFleet(game=self)
        # self.barriers.set_ship(self.ship)
        # self.barriers.set_alien_fleet(self.alien_fleet)

        self.settings.initialize_speed_settings()

    def handle_events(self):
        keys_dir = {pg.K_w: Vector(0, -1), pg.K_UP: Vector(0, -1), 
                    pg.K_s: Vector(0, 1), pg.K_DOWN: Vector(0, 1),
                    pg.K_a: Vector(-1, 0), pg.K_LEFT: Vector(-1, 0),
                    pg.K_d: Vector(1, 0), pg.K_RIGHT: Vector(1, 0)}
        
        for event in pg.event.get():
            if event.type == pg.QUIT: self.game_over()
            elif event.type == pg.KEYDOWN:
                key = event.key
                if key in keys_dir:
                    self.ship.v += self.settings.ship_speed * keys_dir[key]
                elif key == pg.K_SPACE:
                    self.ship.open_fire()
            elif event.type == pg.KEYUP:
                key = event.key
                if key in keys_dir:
                    self.ship.v = Vector()
                elif key == pg.K_SPACE:
                    self.ship.cease_fire()

    def reset(self):
        print('Resetting game...')
        # self.lasers.reset()
        self.barriers.reset()
        self.ship.reset()
        self.alien_fleet.reset()
        self.scoreboard.reset()

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        pg.quit()
        sys.exit()

    def play(self):
        self.sound.play_bg()
        while True:     # at the moment, only exits in gf.check_events if Ctrl/Cmd-Q pressed
            # gf.check_events(settings=self.settings, ship=self.ship)
            self.handle_events() 
            self.screen.fill(self.settings.bg_color)
            self.ship.update()
            self.alien_fleet.update()
            self.barriers.update()
            # self.lasers.update()
            self.scoreboard.update()
            pg.display.flip()


def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()
