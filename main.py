from pygame import locals as const
import pygame
import sys
import os.path

from celestials import Sun, Planet
from ship import Ship


# Missing Mouse button constants
MOUSEKEY_LEFT = 1
MOUSEKEY_MIDDLE = 2
MOUSEKEY_RIGHT = 3

MOUSEKEY_SCROLLUP = 4
MOUSEKEY_SCROLLDOWN = 5


# Pygame startup MUST HAPPEN FIRST
pygame.init()

clock = pygame.time.Clock()

resolution = (640, 480)
window = pygame.display.set_mode(resolution)
pygame.display.set_caption('Space Battle')

background = pygame.image.load(os.path.join('Resources', 'stars.jpg'))

count = 0

WHITE = pygame.Color(255, 255, 255)
FPS = 30

sprites = pygame.sprite.Group()

# Create Sun
Sun.set_fps(FPS)
sun = Sun(resolution[0] / 2, resolution[1] / 2, 50)
sprites.add(sun)

planet = Planet(0, 0, 8)
planet.orbit(sun, 140)
sprites.add(planet)

planet = Planet(0, 0, 10)
planet.orbit(sun, 60)
sprites.add(planet)

planet = Planet(0, 0, 30)
planet.orbit(sun, 200)
sprites.add(planet)

# Create Ship
Ship.set_fps(FPS)
ship = Ship()
sprites.add(ship)

running = True
while running:
    window.fill(WHITE)

    window.blit(background, background.get_rect())
    sprites.draw(window)

    # Event handling
    for event in pygame.event.get():
        if event.type == const.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == const.MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == const.MOUSEBUTTONUP:
            mousex, mousey = event.pos

            event.button == MOUSEKEY_RIGHT

        elif event.type == const.KEYDOWN:
            if event.key == const.K_q and ((event.mod & const.KMOD_META) or (event.mod & const.KMOD_ALT)):
                pygame.quit()
                sys.exit()

            if event.key == const.K_a:
                ship.rotate(Ship.ROT_LEFT)

            if event.key == const.K_d:
                ship.rotate(Ship.ROT_RIGHT)


    sprites.update(pygame.time.get_ticks())

    # Draw the screen ever FPS frames
    pygame.display.update()
    clock.tick(FPS)


