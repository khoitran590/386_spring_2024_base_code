from random import randint
import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers
from alien import Alien
from timer import Timer


class AlienFleet:
    def __init__(self, game): 
        self.model_alien = Alien(game=game, type=1)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()
        self.ufo = Group()
        self.has_ufo = False
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
    def create_ufo(self):
        self.game.sound.play_powerup()
        ufo = UFO(self.game, self)
        ufo.x = ufo.rect.width
        ufo.rect.x = ufo.x
        ufo.rect.y = ufo.rect.height
        self.ufo.add(ufo)
        self.has_ufo = True

    def create_alien(self, alien_number, row_number):
        # if row_number > 5: raise ValueError('row number must be less than 6')
        type = row_number // 2     
        alien = Alien(game=self.game, type=type)
        alien_width = alien.rect.width

        alien.x = alien_width + 1.5 * alien_width * alien_number 
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height * 2 + 1.1 * alien.rect.height * row_number 
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
        collisions = pg.sprite.groupcollide(self.ufo, self.ship_lasers, True, True)
        if collisions:
            for ufo in collisions:
                ufo.hit()
                self.has_ufo = False
        # ship_lasers collide with barrier?

        # aliens_lasers collide with ship_lasers ?
        collisions = pg.sprite.groupcollide(self.ship_lasers, self.aliens_lasers.lasers, False, True)
        if collisions:
            for laser in collisions:
                laser.hit()


    def update(self): 
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.shoot_from_random_alien()
        self.aliens_lasers.update()
        if not self.has_ufo and len(self.aliens.sprites())%5 == 0:
            self.create_ufo()
        for alien in self.aliens.sprites():
            if alien.dead:      # set True once the explosion animation has completed
                alien.remove()
            alien.update()
        for ufo in self.ufo.sprites():
            if ufo.dead:      # set True once the explosion animation has completed
                ufo.remove()
            ufo.update() 
    def draw(self): 
        for alien in self.aliens.sprites(): 
            alien.draw() 
        for ufo in self.ufo.sprites(): 
            ufo.draw() 


class UFO(Alien):
    ufo_images = [pg.transform.rotozoom(pg.image.load(f'images/alien{n}.bmp'), 0, 1) for n in range(2)]
    ufo_explosion_images = [pg.transform.rotozoom(pg.image.load(f'images/explode_500_0{n}.png'), 0, 3) for n in range(5)]
    ufo_value = 500

    def __init__(self, game, fleet):
        super().__init__(game, 3)
        self.timer_norm = Timer(image_list=UFO.ufo_images)
        #self.timer_explosion = Timer(image_list=UFO.ufo_explosion_images, is_loop=False)
        self.timer = self.timer_norm
        self.game = game
        self.fleet = fleet
    def hit(self):
        if not self.dying:
            self.dying = True 
            self.timer = self.timer_explosion
            self.sb.increment_score(UFO.ufo_value)
    def update(self): 
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
            self.fleet.has_ufo = False
        settings = self.settings
        self.x += settings.alien_speed * 1.5
        self.rect.x = self.x
        if self.rect.x > self.game.settings.screen_width:
            self.kill()
            self.fleet.has_ufo = False
        self.draw()
    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
