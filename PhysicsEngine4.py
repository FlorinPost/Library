'''
This is an attempt to a physics engine;
the collision of two objects is treated using both, the
conservation of momentum, and the conservation of kinetic energy

The only difference between version 2 and this new one is in
the checking whether two balls collide procedure;
rather than eliminating big_ball from the list_balls, and after
the check, adding it back, I have introduce a new if condition:
if ball1 == ball 2 : continue
That's really a neat trick to avoid undesired effects without
modifying the list! (Clay's idea!!!)
 There is also a computation of velocities of rotation
 of two objects, after their collision:

  rot_speed = ball1.rot_speed + ball2.rot_speed

  ball1.rot_speed += rot_speed
  ball2.rot_speed += rot_speed

Or, for reflecting the vector to a given normal:
 reflect()
    returns a vector reflected of a given normal.
    reflect(Vector2) -> Vector2

Returns a new vector that points in the direction as if self would bounce of a
surface characterized by the given surface normal.
The length of the new vector is the same as self's.
See lines 104 and 107

The collision of two objects is treated as an elastic collision,
where the mass of each object is given by 3.14*radius^2 (area of the circle),
the initial velocities are v1i and v2i (ball1.vel, ball2. vel).
 The formulas were derived from the two equations provided for
 the conservation of momentum,
 the conservation of the kinetic energy

v1i = ball1.vel
v2i = ball2.vel
m1 = 3.14*ball1.BALL_SIZE**2
m2 = 3.14*ball2.BALL_SIZE**2
ball1.vel =( m1-m2)/(m1+m2)*v1i + 2*m2/(m1+m2)*v2i
ball2.vel = 2*m1/(m1+m2)*v1i + (m2-m1)/(m1+m2)*v2i


'''


import pygame
import random
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
vec = pygame.math.Vector2
size = [SCREEN_WIDTH, SCREEN_HEIGHT]





class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.change_x = random.randrange(-5, 5)
        self.change_y = random.randrange(-5, 5)
        self.acc = vec (0, 0.01)
        self.vel = vec(self.change_x, self.change_y)
        self.BALL_SIZE = random.randrange(10, 40)
        self.x = random.randrange(self.BALL_SIZE, SCREEN_WIDTH - self.BALL_SIZE)
        self.y = random.randrange(self.BALL_SIZE, SCREEN_HEIGHT - self.BALL_SIZE)
        ball_img = pygame.image.load("Imagesp\\ball_image1.png").convert()
        self.image_orig = pygame.transform.scale(ball_img, (self.BALL_SIZE, self.BALL_SIZE))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.pos = vec(self.x, self.y)
        self.rot = 0
        self.rot_speed = 0
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        # Move the ball's center
        # self.vel += self.acc
        self.pos += self.vel
        if self.pos[1] > SCREEN_HEIGHT - self.BALL_SIZE or self.pos[1] < self.BALL_SIZE:
            # using the reflect()
            self.rot *= -1
            self.acc *= -1
            self.vel = self.vel.reflect(vec(0,1))
        if self.pos[0] > SCREEN_WIDTH - self.BALL_SIZE or self.pos[0] < self.BALL_SIZE:
            # using the reflect()
            self.rot *= -1
            self.vel = self.vel.reflect(vec(1,0))
        self.rect.center = (self.pos[0], self.pos[1])


def main():
    pygame.init()
    # Set the height and width of the screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Bouncing Balls")
    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    allsprites = pygame.sprite.Group()
    ballgroup = pygame.sprite.Group()
    Ball.groups = ballgroup, allsprites
    ball_list = []
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
        for ball1 in ball_list:

            for ball2 in ball_list:
                if ball2 == pygame.sprite.spritecollideany(ball1, ball_list, collided=None):
                    if ball2 == ball1:
                        continue
                    else :
                        # The new spin after collision
                        now_is_collide_time = pygame.time.get_ticks()


                        Res = ball1.vel + ball2.vel
                        o1_o2 = ball1.pos - ball2.pos
                        betha = Res.angle_to(o1_o2)

                        ball1.rot_speed += ball1.BALL_SIZE*np.sin(betha)
                        ball2.rot_speed += -ball2.BALL_SIZE*np.sin(betha)
                        # Elastic collision using conservation of momentum and energy
                        v1i = ball1.vel
                        v2i = ball2.vel
                        m1 = 3.14*ball1.BALL_SIZE**2
                        m2 = 3.14*ball2.BALL_SIZE**2
                        ball1.vel = (m1-m2)/(m1+m2)*v1i + 2*m2/(m1+m2)*v2i
                        ball2.vel = 2*m1/(m1+m2)*v1i + (m2-m1)/(m1+m2)*v2i
                        update_collision_time = pygame.time.get_ticks()
                        if now_is_collide_time - update_collision_time > 50:

                            new_ball = Ball()
                            ballgroup.add(new_ball)
                            allsprites.add(new_ball)
                            ball_list.append(new_ball)
                            ball1.kill()
                            ball2.kill()


        allsprites.update()
        screen.fill(BLACK)
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        allsprites.draw(screen)
        pygame.display.flip()
    # Close everything down
    pygame.quit()
if __name__ == "__main__":
    main()