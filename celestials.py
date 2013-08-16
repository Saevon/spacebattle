from pygame.sprite import Sprite
import pygame

import os

from math import cos, sin, atan2, degrees, pi, sqrt
from mixins import ImageBatch
from random import randrange
from random import choice as randchoice
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
        super(Celestial, self).__init__()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self._counter = 0
        self._delay = 1000 / Celestial.FPS

        self._pullable = set()

    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.centery

    def update(self, delta_time):
        self._counter += delta_time
        if self._counter > self._delay:
            self._counter = 0

            self._update()

            for obj in self._pullable:
                self._pull_obj(obj)

    def _update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def _pull_obj(self, obj):
        dx = obj.x - self.x
        dy = obj.y - self.y

        distance = (dx ** 2 + dy ** 2) ** (1.0 / 2.0)

        rads = atan2(-dy, dx)

        speed = self.pull(distance) / Celestial.FPS

        obj.accelerate(-1 * rads, -1 * speed / Celestial.MOVEMENT_CONST)

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


class Planet(Celestial, ImageBatch):
    IMAGE_PATH = os.path.join('Resources', 'sprites', 'planets')

    PLANET_MASS_CONST = 1 * 10 ** 27
    MASS_RANGE = (1, 16)

    def __init__(self, x, y, radius=None, mass=None, image=None):
        if radius is None:
            radius = 20
        self.radius = radius

        if image is None or image not in Planet.IMAGES.keys():
            image = randchoice(Planet.IMAGES.keys())

        self.image = pygame.transform.smoothscale(Planet.IMAGES[image], (self.radius * 2, self.radius * 2))

        if mass is None:
            mass = Planet.PLANET_MASS_CONST * randrange(Planet.MASS_RANGE[0], Planet.MASS_RANGE[1])
        self.mass = mass

        self.rads = randrange(0, 360) * pi / 180

        super(Planet, self).__init__(x, y)

    def _update(self):
        self.rads += pi / 2 ** self.speed
        self.rads %= 2 * pi

        self.rect.centerx = self.orbit.x + self.distance * cos(self.rads)
        self.rect.centery = self.orbit.y + self.distance * sin(self.rads)


    def orbit(self, obj, distance, speed=None):
        '''
        TODO: use GravityWell.satellite() to figure out the minimal speed needed
        TODO: elliptical orbits?
        '''
        self.orbit = obj
        self.distance = distance

        if speed is None:
            speed = randrange(10, 15)
        self.speed = speed

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













