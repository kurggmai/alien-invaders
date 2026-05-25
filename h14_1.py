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
        self.score = 0
        self.max_score = 0
        self.running = True
        self.local_record = 0


    def restart(self, screen, ship):
        aliens.empty()
        bullets.empty()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ship = ship
        if self.score > self.max_score:
            self.max_score = self.score
        self.score = 0

        ship.rect.centerx = self.screen_rect.centerx
        ship.rect.centery = self.screen_rect.bottom - 100
        
        pygame.time.wait(500)

    def died(self, screen):
        self.local_record = update_local_record(stats)

        font = pygame.font.Font('fonts/Sonic Press Start Button [NolivantNT Edit]/SonicPressStartButton[NolivantNTEdit]-Regular.ttf', 36)
        text_image = font.render('Game Over', False, "#645F91")
        screen.blit(text_image, (150, 300))

        font = pygame.font.Font('fonts/uvKits/uvKits.ttf', 35)
        text_image = font.render(f'Your best score: {self.max_score}', False, "#9FADB2")
        screen.blit(text_image, (150, 500))

        text_image = font.render(f'Your local record: {self.local_record}', False, "#9FADB2")
        screen.blit(text_image, (120, 100))


    def reload(self, screen, ship):
        self.restart(screen, ship)

        self.lives = 3
        self.local_record = update_local_record(stats)
        self.score = 0
        self.max_score = 0
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
        self.speed_left = 0
        self.speed_right = 0
        self.speed_up = 0
        self.speed_down = 0

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
            if self.speed_left < self.speed_factor:
                self.speed_left += 30
            self.rect.centerx -= self.speed_left * dt

        if self.mov_right and self.rect.right < self.screen_rect.right:
            if self.speed_right < self.speed_factor:
                self.speed_right += 30
            self.rect.centerx += self.speed_right * dt

        if self.mov_up and self.rect.top > 0:
            if self.speed_up < self.speed_factor:
                self.speed_up += 30
            self.rect.centery -= self.speed_up * dt

        if self.mov_down and self.rect.bottom < self.screen_rect.bottom:
            if self.speed_down < self.speed_factor:
                self.speed_down += 30
            self.rect.centery += self.speed_down * dt


        if self.mov_left == False and self.speed_left > 0:
            if self.rect.left > 0:
                self.speed_left -= 30
                self.rect.centerx -= self.speed_left * dt
            else:
                self.speed_left = 0

        if self.mov_right == False and self.speed_right > 0:
            if self.rect.right < self.screen_rect.right:
                self.speed_right -= 30
                self.rect.centerx += self.speed_right * dt
            else:
                self.speed_right = 0

        if self.mov_up == False and self.speed_up > 0:
            if self.rect.top > 0:
                self.speed_up -= 30
                self.rect.centery -= self.speed_up * dt
            else:
                self.speed_up = 0

        if self.mov_down == False and self.speed_down > 0:
            if self.rect.bottom < self.screen_rect.bottom:
                self.speed_down -= 30
                self.rect.centery += self.speed_down * dt
            else:
                self.speed_down = 0

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


class Hearts():
    def __init__(self, screen, lives):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('images/heart.png')
        self.image = pygame.transform.scale_by(self.image, 0.15)
        self.rect = self.image.get_rect()
    
    def update(self, lives):
        for n in range(lives):
            self.rect.x = self.rect.width // 2 + (self.rect.width + 10) * n
            self.rect.y = self.screen_rect.top + self.rect.height
            self.screen.blit(self.image, self.rect)


class Explosion(Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.center_x = x
        self.center_y = y

        self.min_small_rad = 1
        self.max_small_rad = 10
        self.small_speed_factor = 40
        self.factor = 3

        self.color = "#D4FF3A"

        self.rad = self.min_small_rad

        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def update(self, dt):
        self.rad += self.small_speed_factor * dt
        if self.rad >= self.max_small_rad:
            self.kill()
            return
        if self.rad > self.max_small_rad * 0.6:
            self.color = '#FF613A'
        
        self.size = int(self.max_small_rad * 4)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size // 2, self.size // 2), int(self.rad))
        self.image = pygame.transform.scale_by(self.image, 4.0)
        self.rect = self.image.get_rect(center = (self.center_x, self.center_y))

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Meteor(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load('images/meteor.png')
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, self.screen_rect.right - self.rect.width)
        self.rect.y = -self.rect.height

        self.speed_factor = 500
        self.fy = float(self.rect.y)
        
        self.timer = uniform(3, 6)

    def update(self, dt):
        self.fy += self.speed_factor * dt
        self.rect.y = int(self.fy)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
    

def update_bullets(dt, stats, screen):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)


    if collisions:
        stats.score += 1
        for bullets_list, aliens_list in collisions.items():
            for alien in aliens_list:
                explosion = Explosion(screen, alien.rect.centerx, alien.rect.centery)
                explosions.add(explosion)

    for bullet in bullets.sprites():
        bullet.update(dt)
        bullet.draw()
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def update_explosions(explosions, screen, dt):
    for explosion in explosions:
        explosion.update(dt)
        explosion.blitme()
    

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

def print_score(score, screen):
    screen_rect = screen.get_rect()
    font = pygame.font.SysFont(None, 30)
    text_image = font.render(str(score), True, "#9FADB2")
    screen.blit(text_image, (screen_rect.centerx, screen_rect.top + 30))

def update_local_record(stats):
    with open('global_record.txt', 'r+', encoding = 'utf-8') as file:
        local_record = file.read()

        if stats.max_score > int(local_record):
            file.seek(0)
            file.write(str(stats.max_score))
            file.truncate()
            return local_record
        return local_record
    
def update_meteors(meteors, spawn_timer, dt, screen, stats, ship, aliens):
    collisions = pygame.sprite.spritecollide(ship, meteors, True)
    alien_collisions = pygame.sprite.groupcollide(aliens, meteors, True, False)
    if collisions:
        stats.lives -= 1
        stats.restart(screen, ship)

    spawn_timer -= dt
    if spawn_timer <= 0:
        meteor = Meteor(screen)
        meteors.add(meteor)
        spawn_timer = uniform(1, 5)

    if meteors:
        for meteor in meteors.sprites():
            if meteor.rect.top > HEIGHT:
                meteors.remove(meteor)
            else:
                meteor.update(dt)
                meteor.blitme()

    return spawn_timer


stats = Stats()
ship = Ship(screen)
button = Button(screen)
hearts = Hearts(screen, stats.lives)
stars = Group()
bullets = Group()
explosions = Group()
meteors = Group()

alien = Alien(screen)
aliens = Group()
aliens.add(alien)

global_spawn_timer = uniform(1, 3)
meteors_spawn_timer = uniform(1, 5)

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
        stars.draw(screen)
        update_bullets(dt, stats, screen)
        global_spawn_timer = update_aliens(dt, global_spawn_timer, screen, ship)
        meteors_spawn_timer = update_meteors(meteors, meteors_spawn_timer, dt, screen, stats, ship, aliens)
        update_explosions(explosions, screen, dt)
        aliens.draw(screen)
        ship.blitme()
        hearts.update(stats.lives)
        print_score(stats.score, screen)
    else:
        screen.fill(bg_color)
        stats.died(screen)
        button.blitme()
        check_button_pressed(event, button, screen, ship)
        

    pygame.display.flip()