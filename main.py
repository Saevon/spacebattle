from pygame import locals as const
import pygame
import os.path

from celestials import Sun, Planet
from event_handler import Context
from ship import Ship
from time import time

import background
import events


# Constants
WHITE = pygame.Color(255, 255, 255)
FPS = 30

# Pygame startup MUST HAPPEN FIRST
print "Loading Pygame: ",
start = time()
pygame.init()
print '%.4fs' % (time() - start)

for msg in Planet.load():
    print msg
for msg in Ship.load():
    print msg


clock = pygame.time.Clock()

resolution = (640, 480)
window = pygame.display.set_mode(resolution)
pygame.display.set_caption('Space Battle')

bg = background.load(options=background.STRETCH, resolution=resolution)


sprites = pygame.sprite.Group()
celestials = set()

# Create Sector
Sun.set_fps(FPS)
sun = Sun(resolution[0] / 2, resolution[1] / 2, 50)
sprites.add(sun)
celestials.add(sun)

planet = Planet(0, 0, 8)
planet.orbit(sun, 140)
sprites.add(planet)
celestials.add(planet)

planet = Planet(0, 0, 10)
planet.orbit(sun, 60)
sprites.add(planet)
celestials.add(planet)

planet = Planet(0, 0, 30)
planet.orbit(sun, 200)
sprites.add(planet)
celestials.add(planet)

# Create Ship
Ship.set_fps(FPS)
ship = Ship()
ship.set_Speed(30)
sprites.add(ship)
# for celestial in celestials:
#     celestial.pull_on(ship)

# Global object that an event can manipulate
events.handler.context = Context({
    'ship': ship,
})


while True:
    window.fill(WHITE)

    window.blit(bg, bg.get_rect())
    sprites.draw(window)

    # Events!
    events.handler(pygame.event.get())

    # Draw the screen ever FPS frames
    pygame.display.update()
    clock.tick(FPS)

    # updates
    sprites.update(pygame.time.get_ticks())

