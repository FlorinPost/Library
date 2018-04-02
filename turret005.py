
# Turret rotation
import pygame as pg
import numpy as np
import random
from random import uniform
from os import path

vec = pg.math.Vector2
# Images and sound directors
img_dir = path.join(path.dirname(__file__), 'Imagesp')
snd_dir = path.join(path.dirname(__file__), 'Music for Ping')

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Settings
PLAYER_ACC = 0.5
PLAYER_FRICTION_GROUND = -0.12
PLAYER_FRICTION_AIR = 0.12

# Gun settings
BULLET_SPEED = 30
BULLET_LIFETIME = 750
BULLET_RATE = random.randrange(200, 300)
# KICKBACK = 2
GUN_SPREAD = 5

# Functions

# Classes
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_old = birdy_img
        self.image = pg.transform.scale( self.image_old, (50,50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 100)
        self.pos = vec(WIDTH / 2, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 2)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = - PLAYER_ACC
        elif keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        elif keys[pg.K_UP]:
            self.acc.y = -2
        elif keys[pg.K_DOWN]:
            self.acc.y = 0.1
            # self.open_parachute()
        # Apply friction for horizontal motion
        self.acc.x += self.vel.x * PLAYER_FRICTION_GROUND

        self.acc.y += -self.vel.y * PLAYER_FRICTION_AIR

        # The motion.s equations
        self.vel.x += self.acc.x
        self.vel.y += self.acc.y
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        # if self.acc.y <= 0:

        self.pos.y += self.vel.y + self.acc.y
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.y < 0:
            self.vel.y *= -1
        if self.pos.y >= HEIGHT - 100:
            self.pos.y = HEIGHT - 100
        self.rect.center = self.pos

    def open_parachute(self):
        birdy = birdy_img
        birdy_img.set_colorkey(BLACK)
        birdy.rect = birdy_img.get_rect()
        birdy.rect.bottom = vec(self.pos.x, self.pos.y + 30)


class Turret(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = pg.Surface((20, 80))
        self.image_orig.fill(YELLOW)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = vec(0,0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.rot = self.angle()
            new_image = pg.transform.rotozoom(self.image_orig, self.rot, 1)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def angle(self):
        x_change = self.rect.centerx - player.rect.centerx
        y_change = self.rect.centery - player.rect.centery
        if y_change == 0:
            ang = 90
        else:
            ang = round(np.degrees(np.arctan(x_change / y_change)))
        return ang

    def recoil(self):
        kickback = 20
        self.pos_new = self.pos
        self.vel = vec(-kickback,0 ).rotate(self.rot)
        self.pos_new += self.vel

        self.vel = vec(kickback, 0).rotate(self.rot)
        self.pos_new -= self.vel
        self.vel = vec(0, 0)

    def update(self):

        self.rotate()
        self.pos += self.vel
        # k = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:

            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                # self.recoil()
                dir = vec(1, 0).rotate(-self.rot + 90)
                # k+= 1
                # print(k)
                # print("dir is         ",dir)
                pos = self.pos
                bullet = Bullet(pos, dir)
                all_sprites.add(bullet)
                bullets = pg.sprite.Group()
                bullets.add(bullet)

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, dir):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread)*BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel
        # print("pos is     ",self.pos)
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()


pg.init()


# screen
WIDTH = 468
HEIGHT = 600
FPS = 60

size = (WIDTH, HEIGHT)
screen = pg.display.set_mode(size)
pg.display.set_caption("Rotation")

running = True
clock = pg.time.Clock()
# Load the images
bullet_img = pg.image.load(path.join(img_dir,"bullet.png")).convert()
birdy_img = pg.image.load(path.join(img_dir, "fig01.gif")).convert()


# The groups for sprites
all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)
turrets = pg.sprite.Group()
turret_list = [(WIDTH/2, 20), (40, HEIGHT/2), (WIDTH -40, HEIGHT/2)]
for item in turret_list:
    t = Turret(item[0], item[1])
    turrets.add(t)
    all_sprites.add(t)

# The main loop

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    clock.tick(FPS)

    # all sprite update

    all_sprites.update()

    # screen definition

    screen.fill(BLACK)

    # Draw

    all_sprites.draw(screen)

    pg.display.flip()

pg.quit()


