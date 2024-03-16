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

class LaunchScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.font = pg.font.Font(None, 36)
        # Calculate the center position for the button
        button_width = 400
        button_height = 100
        screen_center_x = self.settings.screen_width // 2
        screen_center_y = self.settings.screen_height // 1.5
        button_x = screen_center_x - button_width // 2
        button_y = screen_center_y - button_height // 1.5
        self.play_button = pg.Rect(button_x, button_y, button_width, button_height)
        self.launch_image = pg.image.load('images/cover-start.jpg')  # Load the image
        self.launch_image = pg.transform.scale(self.launch_image, (self.settings.screen_width, self.settings.screen_height))
        self.launch_image_rect = self.launch_image.get_rect()

    def draw_button(self, button, text):
        pg.draw.rect(self.screen, (0, 255, 0), button)  # Draw button
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=button.center)
        self.screen.blit(text_surf, text_rect)

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.play_button.collidepoint(mouse_pos):
                        running = False

            self.screen.fill(self.settings.bg_color)
            self.screen.blit(self.launch_image, self.launch_image_rect)  # Draw the image
            self.draw_button(self.play_button, "Play Game")
            pg.display.flip()

class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music='sounds/backgroundmusic.wav')
        self.scoreboard = Scoreboard(game=self)  
                                    
        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.alien_fleet = AlienFleet(game=self)
        # self.barriers.set_ship(self.ship)
        # self.barriers.set_alien_fleet(self.alien_fleet)

        self.settings.initialize_speed_settings()
        self.high_score = self.read_high_score()

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
        

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        self.update_high_score(self.scoreboard.increment_score(0))

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
            #self.lasers.update()
            self.scoreboard.update()
            pg.display.flip()

    def read_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                line = file.readline()
                return int(line)
        except (FileNotFoundError, ValueError):
            return 0

    def update_high_score(self, current_score):
        if current_score > self.high_score:
            self.high_score = current_score
            with open("high_score.txt", "w") as file:
                file.write(str(self.high_score))

def main():
    pg.init()
    settings = Settings()
    size = settings.screen_width, settings.screen_height
    screen = pg.display.set_mode(size=size)
    pg.display.set_caption("Alien Invasion")

    game = Game()
    launch_screen = LaunchScreen(game)
    launch_screen.run()  # Show the launch screen first
    game.play()  # Then start the main game loop

if __name__ == '__main__':
    main()
