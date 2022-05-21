import sys, time
from random import randint, uniform
import pygame
from pygame.locals import *
from pygame import Rect as R
from pygame import Vector2 as V

pygame.init()

FPS = 120
CLOCK = pygame.time.Clock()
PDR = R(0, 0, 1080, 1080)
PDS = pygame.display.set_mode(PDR.size)
PDS.fill((255, 255, 255))

CENTER = V(PDR.center)

SQUARE_IMAGE = pygame.image.load("rect870.png").convert_alpha()
square = pygame.transform.rotate(SQUARE_IMAGE, randint(15, 345))

SQUARE_CENTER = V(square.get_rect().center)
square_degrees = 0

target_angle = 360 + randint(0, 360)
radius = randint(300, 800)

rotations = 8

exit_demo = False
while not exit_demo:
    for e in pygame.event.get():
        if e.type == KEYUP:
            if e.key == K_ESCAPE: exit_demo = True


    pos = CENTER + V(1, 0).rotate(square_degrees) * radius
    rotated_square = pygame.transform.rotate(square, 360 - square_degrees)
    square_center = V(rotated_square.get_rect().center)

    PDS.blit(rotated_square, pos - square_center)

    square_degrees += 1
    if square_degrees >= target_angle:
        radius = randint(300, 800)
        square_degrees = 0
        target_angle = 360 + randint(0, 360)
        square = pygame.transform.rotate(SQUARE_IMAGE, randint(15, 345))
        rotations -= 1
        if rotations == 0:
            pygame.image.save(PDS, "{}.png".format(time.perf_counter()))
            pygame.quit()
            sys.exit()