

'''
comments: MOUSE EVENTS
MOUSEMOTION	pos, rel, buttons
MOUSEBUTTONUP	pos, button
MOUSEBUTTONDOWN	pos, button

The Mouse Procedure
selected = None # the variable should be initialized

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            for i, r in enumerate(plat_list):
                if r.rect.collidepoint(event.pos):
                    selected = i
                    selected_offset_x = r.pos[0] - event.pos[0]
                    selected_offset_y = r.pos[1] - event.pos[1]

    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            selected = None

    elif event.type == pygame.MOUSEMOTION:
        if selected is not None:  # selected can be `0` so `is not None` is required
            # move object
            plat_list[selected].pos[0] = event.pos[0] + selected_offset_x
            plat_list[selected].pos[1] = event.pos[1] + selected_offset_y



Very difficult to " transport" objects from CrossRotMob(), and Pusher(),
preserving their sweeping interval!
The discovery of setting up the limits of sweeping after each "transport" solved the problem!
Here is the solution:

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, r in enumerate(plat_list):
                        if r.rect.collidepoint(event.pos):
                        # The commented lines are the new adagio: re-setting the sweeping limits!
                            # mx, my = pygame.mouse.get_pos()
                            # r.rect.center = ( mx, my)
                            # r.limL = mx - r.sweepx
                            # r.limR = mx + r.sweepx
                            # r.lowl = my - r.sweepy
                            # r.uppl = my + r.sweepy
                            selected = i
                            selected_offset_x = r.pos[0] - event.pos[0]
                            selected_offset_y = r.pos[1] - event.pos[1]

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selected = None


            elif event.type == pygame.MOUSEMOTION:
                if selected is not None:  # selected can be `0` so `is not None` is required
                    # move object
                    # mx, my = pygame.mouse.get_pos()
                    # r.rect.center = (mx, my)
                    # r.limL = mx - r.sweepx
                    # r.limR = mx + r.sweepx
                    # r.lowl = my - r.sweepy
                    # r.uppl = my + r.sweepy
                    plat_list[selected].pos[0] = event.pos[0] + selected_offset_x
                    plat_list[selected].pos[1] = event.pos[1] + selected_offset_y


Collision

Since of major importance in bouncing a ball from a platform is
            ball.vel = ball.vel.reflect(platform.norm)
it implies that determining the
platform.norm

it is decisive for the accuracy of motion.
Therefore, if the rectangle defined as platform has length >> width,
then the direction of the platform should be

platform.dir = vec(1,0).rotate(platform.inclination)

so,
platform.norm = platform.dir.rotate(90)

In the similar case of width >> length

platform.dir = vec(0,1).rotate(platform.inclination)


Thus, the normal vector to the collision surface is actually directed perpendicular to the
longest side of the rectangle(surface of contact).


Creating Clones

Using button 3 on the mouse ( right button) an object can be cloned
as long as the mouse position is inside the platform.
The condition is checked with
                if event.button == 3:
                    for r in crossgroup:
                        if r.rect.collidepoint(event.pos):
                            p = CrossRotMob(r.pos[0], r.pos[1], r.l, r.w, r.color,r.angle, r.step,r.speed, r.sweepx )
                            crossgroup.add(p)
                            allsprites.add(p)
                            plat_list.append(p)

Depending on the group whose representative r should be cloned, one should
select the group, and the class !
One problem occurred when the instances of a class( r representative) were not
defined with self.args , like self.x, etc...Thus, the refference to such an object generated the
error : object in class has no r.x attribute!


Note!
If the new objects are added to the plat_list , then they could be translated ( transported, shifted)as well !

self.image = pygame.Surface((100,100)) # created on the fly
self.image.set_colorkey((0,0,0)) # black transparent
pygame.draw.circle(self.image, (255,0,0), (50,50), 50, 2) # red circle
self.image = self.image.convert_alpha()


collision using the radius

#pygame.sprite.spritecollide(sprite, group, dokill, collided = None): return Sprite_list
crashgroup = pygame.sprite.spritecollide(hunter, birdgroup, False, pygame.sprite.collide_circle)
# pygame.sprite.collide_circle works only if one sprite has self.radius
# you can do without that argument collided and only the self.rects will be checked

Not successful with this!
 for ball in ball_list:
            for plat in all_plats:
                if plat == pygame.sprite.spritecollide(ball, all_plats, False, pygame.sprite.collide_circle):
                    ball.vel = ball.vel.reflect(plat.norm)
                    print("Yup!")

'''

import pygame
import random
import time
import numpy as np

vec = pygame.math.Vector2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
HOVERING = (255, 51, 255)
ORANGE = (255, 128, 0)
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

size = [SCREEN_WIDTH, SCREEN_HEIGHT]


class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, l, w, color):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.l = l
        self.w = w
        self.color = color
        self.image_orig = pygame.Surface((l, w))
        self.image_orig.fill(color)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rot = 0
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.sweepx = 0
        self.sweepy = 0
        self.limL = self.rect.centerx - self.sweepx
        self.limR = self.rect.centerx + self.sweepx
        self.lowl = self.pos[1] - self.sweepy
        self.uppl = self.pos[1] + self.sweepy

        if x >= y:
            self.dir = vec(1, 0).rotate(self.rot)
        else:
            self.dir = vec(0, 1).rotate(self.rot)
        self.norm = self.dir.rotate(90 - self.rot)

    def update(self):
        self.norm = self.dir.rotate(90 - self.rot)
        self.vel += self.acc
        self.pos += self.vel
        self.rect.center = (self.pos[0], self.pos[1])


class Platrot(Platform):

    def __init__(self, x, y, l, w, color, angle, step, speed):
        super().__init__(x, y, l, w, color)

        self.angle = angle
        self.step = step  # degrees should rotate at once
        self.speed = speed
        self.rect.center = (x, y)
        self.rot = 0
        self.rot_speed = self.step
        self.last_update = pygame.time.get_ticks()
        self.k = 0
        self.sweepx = 0
        self.sweepy = 0
        self.limL = self.rect.centerx - self.sweepx
        self.limR = self.rect.centerx + self.sweepx
        self.lowl = self.pos[1] - self.sweepy
        self.uppl = self.pos[1] + self.sweepy

    def rotate(self):

        now = pygame.time.get_ticks()

        if now - self.last_update > self.speed:

            self.last_update = now
            self.k += 1
            if self.k >= self.angle:
                self.k = self.k - 2 * self.angle

            if self.k < 0:
                self.rot = (self.rot + self.rot_speed) % 360
            else:
                self.rot = (self.rot - self.rot_speed) % 360
            new_image = pygame.transform.rotozoom(self.image_orig, self.rot, 1)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.dir = vec(1, 0).rotate(self.rot)
        self.norm = vec(1, 0).rotate(90 - self.rot)
        self.rect.center = (self.pos[0], self.pos[1])


class Platmob(Platform):

    def __init__(self, x, y, l, w, color):
        super().__init__(x, y, l, w, color)

        self.sweepx = 0
        self.sweepy = 0
        self.limL = self.rect.centerx - self.sweepx
        self.limR = self.rect.centerx + self.sweepx
        self.lowl = self.pos[1] - self.sweepy
        self.uppl = self.pos[1] + self.sweepy

    def slide(self):
        # sliding procedure
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc = vec(-0.02, 0)
        if keys[pygame.K_RIGHT]:
            self.acc = vec(0.02, 0)

        self.vel += self.acc
        self.pos += self.vel
        self.rect.center = (self.pos[0], self.pos[1])
        self.acc = vec(0, 0)
        if self.pos[0] <= 0 or self.pos[0] >= SCREEN_WIDTH:
            self.acc = vec(0, 0)
            self.vel *= - 1

    def update(self):
        self.slide()


class CrossRotMob(Platrot):
    def __init__(self, x, y, l, w, color, angle, step, speed, sweepx):
        super().__init__(x, y, l, w, color, angle, step, speed)

        self.angle = angle
        self.step = step  # How many degrees should rotate at once
        self.speed = speed
        self.sweepx = sweepx
        self.sweepy = 0
        self.rect.center = (x, y)
        self.rot = 0
        self.acc = vec(0.03, 0)
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.fric = vec(0.05, 0)
        self.sweep = 0
        self.limL = self.rect.centerx - self.sweepx
        self.limR = self.rect.centerx + self.sweepx
        self.lowl = self.pos[1] - self.sweepy
        self.uppl = self.pos[1] + self.sweepy

    def slide(self):
        # self.rect.center = (self.pos[0], self.pos[1])
        if self.pos[0] > self.limR:
            self.acc = vec(- 0.01, 0)
            self.vel *= -1
            self.fric = vec(-0.01, 0)
        if self.pos[0] < self.limL:
            self.acc = vec(0.01, 0)
            self.vel *= -1
            self.fric = vec(0.01, 0)
        self.vel += self.acc - self.fric
        self.pos += self.vel

    def update(self):

        self.slide()
        self.rotate()
        self.rect.center = (self.pos[0], self.pos[1])


class Platoblique(Platform):

    def __init__(self, x, y, l, w, color, incline):
        super().__init__(x, y, l, w, color)

        self.incline = incline
        self.image = pygame.transform.rotozoom(self.image, incline, 1)
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.sweepx = 0
        self.sweepy = 0
        self.limL = self.rect.centerx - self.sweepx
        self.limR = self.rect.centerx + self.sweepx
        self.lowl = self.pos[1] - self.sweepy
        self.uppl = self.pos[1] + self.sweepy

    def update(self):
        self.dir = vec(0, -1).rotate(self.incline)
        self.norm = self.dir.rotate(90)
        # print( self.dir, "    norm", self.norm)
        self.pos += self.vel
        self.rect.center = (self.pos[0], self.pos[1])


class Pusher(Platoblique):
    def __init__(self, x, y, l, w, color, incline, force, sweepy):
        super().__init__(x, y, l, w, color, incline)

        self.incline = incline
        self.force = force
        self.fric = vec(0, 0)
        self.acc = vec(0, -0.03)
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.sweepy = sweepy
        self.sweepx = 0
        self.limL = self.rect.centerx - self.sweepx
        self.limR = self.rect.centerx + self.sweepx
        self.lowl = self.pos[1] - self.sweepy
        self.uppl = self.pos[1] + self.sweepy
        self.rot = 0
        self.dir = vec(1, 0).rotate(self.incline)
        self.norm = self.dir.rotate(-90)

    def slide(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.acc = vec(0, -0.01)
        if keys[pygame.K_DOWN]:
            self.acc = vec(0, 0.01)
        if self.pos[1] >= self.uppl:
            self.acc = vec(0, -0.01)
            self.vel *= -1
            self.fric = vec(0, -0.01)
        if self.pos[1] <= self.lowl:
            self.acc = vec(0, 0.01)
            self.vel *= -1
            self.fric = vec(0, 0.01)
        self.vel += self.acc - self.fric
        self.pos += self.vel
        self.rect.center = (self.pos[0], self.pos[1])

    def update(self):
        self.slide()
        self.rect.center = (self.pos[0], self.pos[1])


# Balls class


class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.BALL_SIZE = random.randrange(30, 40)
        self.x = 25
        self.y = 25
        ball_img = pygame.image.load("Imagesp\\ball_image1.png").convert()
        self.image_orig = pygame.transform.scale(ball_img, (self.BALL_SIZE, self.BALL_SIZE))

        # self.image = pygame.Surface((50, 50))
        self.image_orig.set_colorkey(BLACK)  # black transparent
        # pygame.draw.circle(self.image, RED, (25, 25), int(self.BALL_SIZE/2), 2)  # red circle
        # self.image_orig = self.image.convert_alpha()
        self.rect = self.image_orig.get_rect()

        self.radius = self.BALL_SIZE / 2  # for collide check
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.pos = vec(self.x, self.y)
        self.acc = vec(0, 0.5)
        self.vel = vec(0, 0)
        self.mass = 3.14 * self.BALL_SIZE * self.BALL_SIZE
        self.rot = 0
        self.rot_speed = -random.randrange(2, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):

        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotozoom(self.image_orig, self.rot, 1)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):

        self.vel += self.acc
        self.pos += self.vel
        if self.rect.bottom > SCREEN_HEIGHT + self.BALL_SIZE / 2:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel = vec(10, 0)
            self.acc = (0, -0.2)
        if self.pos[0] > SCREEN_WIDTH + 2 * self.BALL_SIZE:
            self.kill()
        if self.pos[1] >= SCREEN_HEIGHT - self.BALL_SIZE:
            self.vel = self.vel.reflect(vec(0, 1))
        if self.pos[0] < self.BALL_SIZE or self.pos[0] > SCREEN_WIDTH - self.BALL_SIZE:
            self.vel = self.vel.reflect(vec(1, 0))
        if self.pos[0] < -10:
            self.vel = self.vel.reflect(vec(0, 1))
        if self.pos[1] < -self.BALL_SIZE / 2:
            self.acc = vec(0, 2)
        self.rect.center = (self.pos[0], self.pos[1])


def main():
    pygame.init()
    # Set the height and width of the screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Platforms")
    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    allsprites = pygame.sprite.Group()
    all_plats = pygame.sprite.Group()
    # Group for objects in Platform class
    platgroup = pygame.sprite.Group()
    Platform.groups = platgroup, allsprites, all_plats
    plat1 = Platform(300, 300, 100, 10, GREEN)
    plat6 = Platform(600, 300, 100, 10, GREEN)

    allsprites.add(plat1)
    platgroup.add(plat1)
    allsprites.add(plat6)
    platgroup.add(plat6)

    # Group for Platrot
    platrotgroup = pygame.sprite.Group()
    Platrot.groups = platrotgroup, allsprites, all_plats
    plat2 = Platrot(120, 100, 200, 10, YELLOW, 45, 1, 100)
    plat9 = Platrot(600, 150, 100, 10, YELLOW, 360, 5, 25)
    platrotgroup.add(plat2, plat9)
    allsprites.add(plat2, plat9)
    # Group for Platmob
    platmobgroup = pygame.sprite.Group()
    Platmob.groups = platmobgroup, allsprites, all_plats
    plat3 = Platmob(600, 400, 50, 10, RED)
    platmobgroup.add(plat3)
    allsprites.add(plat3)
    # Group for CrossRotMob
    crossgroup = pygame.sprite.Group()
    CrossRotMob.groups = crossgroup, allsprites, all_plats
    plat4 = CrossRotMob(400, 200, 40, 5, BLUE, 360, 10, 30, 50)
    crossgroup.add(plat4)
    allsprites.add(plat4)
    # Group for Platoblique
    obliquegroup = pygame.sprite.Group()
    Platoblique.groups = allsprites, obliquegroup, all_plats
    plat10 = Platoblique(100, 250, 60, 10, WHITE, 45)
    plat7 = Platoblique(550, 250, 10, 100, WHITE, 180)
    plat8 = Platoblique(650, 250, 10, 100, WHITE, 180)

    obliquegroup.add(plat10, plat7, plat8)
    allsprites.add(plat10, plat7, plat8)

    # Group for Pusher
    pushgroup = pygame.sprite.Group()
    Pusher.groups = allsprites, pushgroup, all_plats
    plat5 = Pusher(710, 450, 40, 5, ORANGE, 45, 0.9, 40)
    pushgroup.add(plat5)
    allsprites.add(plat5)

    # Group for balls
    ballgroup = pygame.sprite.Group()
    # List of all platforms for collision purposes
    plat_list = []
    plat_list.append(plat1)
    plat_list.append(plat2)
    plat_list.append(plat3)
    plat_list.append(plat4)
    plat_list.append(plat5)
    plat_list.append(plat6)
    plat_list.append(plat7)
    plat_list.append(plat8)
    plat_list.append(plat9)
    plat_list.append(plat10)

    ball_list = []
    selected = None

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball = Ball()
                    ballgroup.add(ball)
                    allsprites.add(ball)
                    ball_list.append(ball)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, r in enumerate(plat_list):
                        if r.rect.collidepoint(event.pos):
                            mx, my = pygame.mouse.get_pos()
                            r.rect.center = (mx, my)
                            r.limL = mx - r.sweepx
                            r.limR = mx + r.sweepx
                            r.lowl = my - r.sweepy
                            r.uppl = my + r.sweepy
                            selected = i
                            selected_offset_x = r.pos[0] - event.pos[0]
                            selected_offset_y = r.pos[1] - event.pos[1]
                #             Here is the place where the copies are created
                if event.button == 3:
                    for r in crossgroup:
                        generic_def = r.x - 4, r.y + 6, r.l, r.w, r.color
                        if r.rect.collidepoint(event.pos):
                            p = CrossRotMob(r.x - 4, r.y + 6, r.l, r.w, r.color, r.angle, r.step, r.speed, r.sweepx)
                            crossgroup.add(p)
                            allsprites.add(p)
                            plat_list.append(p)
                    for r in pushgroup:
                        if r.rect.collidepoint(event.pos):
                            p = Pusher(r.x - 4, r.y + 6, r.l, r.w, r.color, r.incline, r.force, r.sweepy)
                            pushgroup.add(p)
                            allsprites.add(p)
                            plat_list.append(p)
                    for r in obliquegroup:
                        if r.rect.collidepoint(event.pos):
                            p = Platoblique(r.x - 4, r.y + 6, r.l, r.w, r.color, r.incline)
                            obliquegroup.add(p)
                            allsprites.add(p)
                            plat_list.append(p)
                    for r in platrotgroup:
                        if r.rect.collidepoint(event.pos):
                            p = Platrot(r.x - 4, r.y + 6, r.l, r.w, r.color, r.angle, r.step, r.speed)
                            platrotgroup.add(p)
                            allsprites.add(p)
                            plat_list.append(p)
                    for r in platgroup:
                        if r.rect.collidepoint(event.pos):
                            p = Platform(r.x - 4, r.y + 6, r.l, r.w, r.color)
                            platgroup.add(p)
                            allsprites.add(p)
                            plat_list.append(p)
                    for r in platmobgroup:
                        if r.rect.collidepoint(event.pos):
                            p = Platmob(r.x - 4, r.y + 6, r.l, r.w, r.color)
                            platmobgroup.add(p)
                            allsprites.add(p)
                            plat_list.append(p)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selected = None


            elif event.type == pygame.MOUSEMOTION:
                if selected is not None:  # selected can be `0` so `is not None` is required
                    # move object
                    mx, my = pygame.mouse.get_pos()
                    r.rect.center = (mx, my)
                    r.limL = mx - r.sweepx
                    r.limR = mx + r.sweepx
                    r.lowl = my - r.sweepy
                    r.uppl = my + r.sweepy
                    plat_list[selected].pos[0] = event.pos[0] + selected_offset_x
                    plat_list[selected].pos[1] = event.pos[1] + selected_offset_y

        for p in plat_list:
            for bally in ball_list:

                if bally == pygame.sprite.spritecollideany(p, ball_list, collided=None):
                    bally.vel = bally.vel.reflect(p.norm)

        for ball1 in ball_list:
            if pygame.sprite.spritecollide(ball1, pushgroup, False, collided=None):
                ball1.vel = plat5.force * ball1.vel.reflect(plat5.norm)
            for ball2 in ball_list:
                if ball2 == pygame.sprite.spritecollideany(ball1, ball_list, collided=None):
                    if ball2 == ball1:
                        continue
                    else:
                        # The new spin after collision
                        rot_speed = ball1.rot_speed + ball2.rot_speed
                        ball1.rot_speed += rot_speed
                        ball2.rot_speed += rot_speed
                        # Elastic collision using conservation of momentum and energy
                        v1i = ball1.vel
                        v2i = ball2.vel
                        m1 = 3.14 * ball1.BALL_SIZE ** 2
                        m2 = 3.14 * ball2.BALL_SIZE ** 2
                        ball1.vel = (m1 - m2) / (m1 + m2) * v1i + 2 * m2 / (m1 + m2) * v2i
                        ball2.vel = 2 * m1 / (m1 + m2) * v1i + (m2 - m1) / (m1 + m2) * v2i

        allsprites.update()
        screen.fill(BLACK)
        clock.tick(60)
        pygame.event.pump()
        # Go ahead and update the screen with what we've drawn.
        allsprites.draw(screen)
        pygame.display.flip()
    # Close everything down
    pygame.quit()


if __name__ == "__main__":
    main()

