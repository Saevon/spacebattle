from pygame.sprite import Sprite
import pygame

import os.path

from math import atan2, degrees, pi
import well

class Sun(Sprite, well.GravityWell):

    IMAGE = pygame.image.load(os.path.join('Resources', 'sprites', 'sun', 'Sun.png'))

    def __init__(self, x, y):
        self.image = Sun.IMAGE

        self._x = x
        self._y = y

        super(self, Sun).__init__()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def pull_obj(self, obj):
        distance = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** (1.0 / 2.0)

        dx = obj.x - self.x
        dy = obj.y - self.y
        rads = atan2(-dy, dx)

        speed = self.pull(distance)

        obj.accelerate(rads, speed)
