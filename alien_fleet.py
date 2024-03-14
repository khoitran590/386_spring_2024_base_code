from random import randint
import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers
from alien import Alien
# from timer import Timer


class AlienFleet:
    def __init__(self, game): 
        self.model_alien = Alien(game=game, type=1)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()

        # self.ship_lasers = game.ship.lasers.lasers    # a laser Group
        # self.aliens_lasers = Lasers(settings=game.settings)

        self.ship_lasers = game.ship_lasers.lasers    # a laser Group
        self.aliens_lasers = game.alien_lasers

        self.screen = game.screen
        self.settings = game.settings
        self.shoot_requests = 0
        self.ship = game.ship
        self.create_fleet()
    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 6 * alien_width
        number_aliens_x = int(available_space_x / (1.2 * alien_width))
        return number_aliens_x
    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (1 * alien_height))
        number_rows = 6
        return number_rows        
    def reset(self):
        self.aliens.empty()
        self.create_fleet()
        self.aliens_lasers.reset()
    def create_alien(self, alien_number, row_number):
        # if row_number > 5: raise ValueError('row number must be less than 6')
        type = row_number // 2     
        alien = Alien(game=self.game, type=type)
        alien_width = alien.rect.width

        alien.x = alien_width + 1.5 * alien_width * alien_number 
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * row_number 
        self.aliens.add(alien)     
    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width) 
        number_rows = self.get_number_rows(self.ship.rect.height, self.model_alien.rect.height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                   self.create_alien(alien_number, row_number)
    def check_fleet_edges(self):
        for alien in self.aliens.sprites(): 
            if alien.check_edges():
                self.change_fleet_direction()
                break
    def check_fleet_bottom(self):
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.hit()
                break
    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print('Aliens all gone!')
            self.game.reset()
    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def shoot_from_random_alien(self):
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return
        
        num_aliens = len(self.aliens.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.aliens.sprites():
            if i == alien_num:
                self.aliens_lasers.shoot(game=self.game, x=alien.rect.centerx + 6, y=alien.rect.bottom)
            i += 1

    # alien_lasers hitting the ship Or
    # alien_lasers hitting a barrier or
    # alien_lasers hitting a ship_lasers

    # ship_lasers hitting an alien or
    # ship_lasers hitting a barrier or
    # ship_lasers hitting an aliens_lasers


    def check_collisions(self):  
        collisions = pg.sprite.groupcollide(self.aliens, self.ship_lasers, False, True)  
        if collisions:
            for alien in collisions:
                alien.hit()

        collisions = pg.sprite.spritecollide(self.ship, self.aliens_lasers.lasers, True)
        if collisions:
            self.ship.hit()

        # aliens_lasers collide with barrier?

        # ship_lasers collide with barrier?

        # aliens_lasers collide with ship_lasers ?


    def update(self): 
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.shoot_from_random_alien()
        for alien in self.aliens.sprites():
            if alien.dead:      # set True once the explosion animation has completed
                alien.remove()
            alien.update() 
        self.aliens_lasers.update()
    def draw(self): 
        for alien in self.aliens.sprites(): 
            alien.draw() 
