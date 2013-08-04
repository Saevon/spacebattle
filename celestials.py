from pygame.sprite import Sprite
import pygame

import os.path

from math import atan2, degrees, pi
import well

class Sun(Sprite, well.GravityWell):

    IMAGE = pygame.image.load(os.path.join('Resources', 'sprites', 'sun', 'Sun.png'))

    @staticmethod
    def set_fps(fps):
        Sun.FPS = fps

    def __init__(self, x, y, radius):
        self.image = pygame.transform.smoothscale(Sun.IMAGE, (radius * 2, radius * 2))

        self._x = x
        self._y = y

        super(Sun, self).__init__()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self._counter = pygame.time.get_ticks()
        self._delay = 1000 / Sun.FPS

    def update(self, time):
        if time > self._counter + self._delay:
            self._counter = time

            for obj in self._pullable:
                self.pull_obj(obj)

    def set_pullable(self, objects):
        self._pullable = objects

    def pull_obj(self, obj):
        distance = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** (1.0 / 2.0)

        dx = obj.x - self.x
        dy = obj.y - self.y
        rads = atan2(-dy, dx)

        speed = self.pull(distance) / Sun.FPS

        obj.accelerate(rads, speed)
