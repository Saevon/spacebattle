from pygame import locals as const
import pygame
import os.path

from celestials import Sun, Planet
from event_handler import Context
from ship import Ship

import events


# KeyDown Booleans
aDown = False
dDown = False

# Pygame startup MUST HAPPEN FIRST
pygame.init()
Planet.load()

clock = pygame.time.Clock()

resolution = (640, 480)
window = pygame.display.set_mode(resolution)
pygame.display.set_caption('Space Battle')

background = pygame.image.load(os.path.join('Resources', 'stars.jpg'))

count = 0

WHITE = pygame.Color(255, 255, 255)
FPS = 30

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
sprites.add(ship)
# for celestial in celestials:
#     celestial.pull_on(ship)

# Global object that an event can manipulate
events.handler.context = Context({
    'ship': ship,
})


while True:
    window.fill(WHITE)

    window.blit(background, background.get_rect())
    sprites.draw(window)

    # Events!
    events.handler(pygame.event.get())

    # Draw the screen ever FPS frames
    pygame.display.update()
    clock.tick(FPS)

    # updates
    sprites.update(pygame.time.get_ticks())

