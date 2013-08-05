from pygame.sprite import Sprite
import pygame

import os.path

from math import cos, sin, atan2, degrees, pi, sqrt
from random import randrange
import well


def vector_add(rads1, speed1, rads2, speed2):
        x = speed1 * cos(rads1) + speed2 * cos(rads2)
        y = speed1 * sin(rads1) + speed2 * sin(rads2)

        rads = atan2(y, x)
        speed = sqrt(x ** 2 + y ** 2)

        return (rads, speed)




class Celestial(Sprite, well.GravityWell):
    '''
    requires that self.mass and Class.Image be defined
    '''

    MOVEMENT_CONST = 10 ** 20

    @staticmethod
    def set_fps(fps):
        Celestial.FPS = fps

    def __init__(self, x, y):
        self.x = x
        self.y = y

        super(Celestial, self).__init__()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self._counter = pygame.time.get_ticks()
        self._delay = 1000 / Celestial.FPS

        self._pullable = set()

    def update(self, time):
        if time > self._counter + self._delay:
            self._counter = time

            self._update()

            for obj in self._pullable:
                self._pull_obj(obj)

    def _update(self):
        pass


    def _pull_obj(self, obj):
        distance = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** (1.0 / 2.0)

        dx = obj.x - self.x
        dy = obj.y - self.y
        rads = atan2(-dy, dx)

        speed = self.pull(distance) / Celestial.FPS

        obj.accelerate(rads, speed)

    def pull_on(self, obj):
        self._pullable.add(obj)

    def pull_off(self, obj):
        self._pullable.remove(obj)



class Sun(Celestial):
    IMAGE = pygame.image.load(os.path.join('Resources', 'sprites', 'sun', 'Sun.png'))

    # This is half the our Solar Mass
    STAR_MASS_CONST = 1 * 10 ** 33
    MASS_RANGE = (1, 51)

    def __init__(self, x, y, radius=None, mass=None):
        if radius is None:
            radius = 50
        self.radius = radius

        self.image = pygame.transform.smoothscale(Sun.IMAGE, (self.radius * 2, self.radius * 2))

        if mass is None:
            mass = Sun.STAR_MASS_CONST * randrange(Sun.MASS_RANGE[0], Sun.MASS_RANGE[1])
        self.mass = mass

        super(Sun, self).__init__(x, y)


class Planet(Celestial):
    IMAGE = pygame.image.load(os.path.join('Resources', 'sprites', 'planets', 'Planet.png'))

    PLANET_MASS_CONST = 1 * 10 ** 27
    MASS_RANGE = (1, 16)

    def __init__(self, x, y, radius=None, mass=None):
        if radius is None:
            radius = 20
        self.radius = radius

        self.image = pygame.transform.smoothscale(Planet.IMAGE, (self.radius * 2, self.radius * 2))

        if mass is None:
            mass = Planet.PLANET_MASS_CONST * randrange(Planet.MASS_RANGE[0], Planet.MASS_RANGE[1])
        self.mass = mass

        self.rads = randrange(0, 360) * pi / 180

        super(Planet, self).__init__(x, y)

    def _update(self):
        self.rads += pi / 2 ** self.speed
        self.rads %= 2 * pi

        self.x = self.orbit.x + self.distance * cos(self.rads)
        self.y = self.orbit.y + self.distance * sin(self.rads)

        self.rect.centerx = self.x
        self.rect.centery = self.y


    def orbit(self, obj, distance):
        '''
        TODO: use GravityWell.satellite() to figure out the minimal speed needed
        TODO: elliptical orbits?
        '''
        self.orbit = obj
        self.distance = distance

        self.speed = randrange(10, 15)

#     def orbit(self, obj, distance):
#         obj.pull_on(self)

#         self.x = obj.x
#         self.y = obj.y - distance
#         self.rect.centerx = self.x
#         self.rect.centery = self.y

#         self.rads = pi / 2
#         self.speed = obj.satellite(distance)

#     def accelerate(self, rads, speed):
#         self.rads, self.speed = vector_add(
#             self.rads, self.speed,
#             rads, speed
#         )

#     def _update(self):
#         x = self.speed * cos(self.rads)
#         y = self.speed * sin(self.rads)

#         self.x = self.x + (x / Celestial.MOVEMENT_CONST)
#         self.y = self.y + (y / Celestial.MOVEMENT_CONST)

#         self.rect.centerx = self.x
#         self.rect.centery = self.y













