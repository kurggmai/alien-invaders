import pygame
import sys
from pygame.sprite import Group
from pygame.sprite import Sprite
from random import randint
from random import uniform
from random import random
from random import choice

pygame.init()

WIDTH = 700
HEIGHT = 700
bg_color = "#000000"

screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Stats():
    def __init__(self):
        self.lives = 3
        self.count = 0
        self.running = True

    def restart(self, screen, ship):
        aliens.empty()
        bullets.empty()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ship = ship

        ship.rect.centerx = self.screen_rect.centerx
        ship.rect.centery = self.screen_rect.bottom - 100
        
        pygame.time.wait(500)

    def died(self, screen):
        font = pygame.font.Font('Sonic Press Start Button [NolivantNT Edit]/SonicPressStartButton[NolivantNTEdit]-Regular.ttf', 36)
        text_image = font.render('Game Over', False, "#645F91")
        screen.blit(text_image, (150, 300))

    def reload(self, screen, ship):
        self.restart(screen, ship)

        self.lives = 3
        self.count = 0
        self.running = True

class Star(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.width = self.height = 3
        self.x = randint(0, self.screen_rect.right)
        self.y = randint(0, self.screen_rect.bottom)
        self.speed_factor = 200
        r, g, b = 150, 150, 200
        self.k = uniform(0.3, 1.2)
        self.color = (int(r * self.k), int(g * self.k), int(b * self.k))
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.fy = float(self.y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, dt):
        self.fy += (self.speed_factor * dt) * self.k
        if self.rect.y >= self.screen_rect.bottom:
            self.fy = 0


        self.rect.y = int(self.fy)

class Ship(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.speed_factor = 500

        self.image = pygame.image.load('images/ship.png')
        self.image = pygame.transform.scale_by(self.image, 2)

        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.bottom - 100

        self.mov_left = False
        self.mov_right = False
        self.mov_up = False
        self.mov_down = False


    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, dt):
        if self.mov_left and self.rect.left > 0:
            self.rect.centerx -= self.speed_factor * dt

        if self.mov_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.speed_factor * dt

        if self.mov_up and self.rect.top > 0:
            self.rect.centery -= self.speed_factor * dt

        if self.mov_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.centery += self.speed_factor * dt


class Bullet(Sprite):
    def __init__(self, screen, ship):
        super().__init__()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ship = ship
        self.width = 5
        self.height = 20
        self.color = "#E5F5FF"
        self.speed_factor = 400
        
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.top = self.ship.rect.top
        self.rect.centerx = self.ship.rect.centerx
        self.y = float(self.rect.centery)

    def update(self, dt):
        self.y -= self.speed_factor * dt
        self.rect.centery = int(self.y)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 0, 3)


class Alien(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        
        self.image = pygame.image.load('images/alien.png')
        self.image = pygame.transform.scale_by(self.image, 4)
        self.rect = self.image.get_rect()

        self.rect.x = randint(0, self.screen_rect.right - self.rect.width)
        self.x = float(self.rect.centerx)

        self.rect.y = -self.rect.height
        self.y = float(self.rect.y)

        self.speed_factor_x = 150
        self.speed_factor_y = 50
        self.vector = 1
        
        self.timer = uniform(1, 3)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, dt):

        self.timer -= dt
        if self.timer <= 0:
            self.vector *= -1
            self.timer = uniform(1, 3)
        
        self.x += self.speed_factor_x * dt * self.vector
        self.y += self.speed_factor_y * dt


        if self.x < 0:
            self.x = 0
            self.vector = 1
            self.timer = uniform(1, 3)
        elif self.x > self.screen_rect.right - self.rect.width:
            self.x = self.screen_rect.right - self.rect.width
            self.vector = -1
            self.timer = uniform(1, 3)


        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


class Button():
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('images/button.png')
        self.image = pygame.transform.scale_by(self.image, 0.3)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery + 55

    def blitme(self):
        self.screen.blit(self.image, self.rect)


def update_bullets(dt):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    for bullet in bullets.sprites():
        bullet.update(dt)
        bullet.draw()
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def update_aliens(dt, spawn_timer, screen, ship):
        collisions = pygame.sprite.spritecollide(ship, aliens, True)
        if collisions:
            stats.lives -= 1
            stats.restart(screen, ship)

        for alien in aliens.sprites():
            if alien.rect.top > HEIGHT:
                aliens.remove(alien)
            else:
                alien.update(dt)
                alien.blitme()

        spawn_timer -= dt
        if spawn_timer <= 0:
            new_alien = Alien(screen)
            aliens.add(new_alien)
            spawn_timer = uniform(1, 3)

        return spawn_timer

def check_button_pressed(event, button, screen, ship):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mousex, mousey = pygame.mouse.get_pos()
        if (
            mousex > button.rect.left and mousex < button.rect.right 
            and mousey > button.rect.top and mousey < button.rect.bottom
            ):
            stats.reload(screen, ship)



ship = Ship(screen)
button = Button(screen)
stats = Stats()
stars = Group()
bullets = Group()

alien = Alien(screen)
aliens = Group()
aliens.add(alien)

global_spawn_timer = uniform(1, 3)

for _ in range(500):
    star = Star(screen)
    stars.add(star)

clock = pygame.time.Clock()

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

            if stats.running:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    ship.mov_left = True

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    ship.mov_right = True

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    ship.mov_up = True

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    ship.mov_down = True

                if event.key == pygame.K_SPACE:
                    bullet = Bullet(screen, ship)
                    bullets.add(bullet)

        elif event.type == pygame.KEYUP:
            if stats.running:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    ship.mov_left = False

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    ship.mov_right = False

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    ship.mov_up = False

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    ship.mov_down = False

    if stats.lives == 0:
        stats.running = False
        stats.died(screen)

    if stats.lives:
        screen.fill(bg_color)
        stars.update(dt)
        ship.update(dt)
        update_bullets(dt)
        global_spawn_timer = update_aliens(dt, global_spawn_timer, screen, ship)
        stars.draw(screen)
        aliens.draw(screen)
        ship.blitme()
    else:
        screen.fill(bg_color)
        stats.died(screen)
        button.blitme()
        check_button_pressed(event, button, screen, ship)
        

    pygame.display.flip()