import pygame
import os.path
from mixins import ImageBatch
from math import cos, sin, pi


class Ship(pygame.sprite.Sprite, ImageBatch):
    # Original Image
    IMAGE_PATH = os.path.join('Resources', 'sprites', 'ship')

    # Rotation Direction Constants
    ROT_RIGHT = -1
    ROT_LEFT = 1
    ROT_STOP = 0

    MOV_FORWARDS = 1
    MOV_BACKWARDS = -1
    MOV_STOP = 0

    @classmethod
    def load(cls):
        for out in super(Ship, cls).load():
            yield out

        yield '  Resizing ImageBatch for %s' % cls.__name__

        Ship.SCALED_IMAGES = {}
        for key, value in Ship.IMAGES.iteritems():
            yield '    %s' % key

            rect = value.get_rect()

            width = rect.width / 4
            height = rect.height / 4

            Ship.SCALED_IMAGES[key] = pygame.transform.smoothscale(
                value,
                (width, height)
            )

    def __init__(self, x, y, model='ship1', base='purple'):
        super(Ship, self).__init__()

        self.model = model
        self.base = base
        self.image = Ship.SCALED_IMAGES.get(self.model)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self._direction = 0
        self._delay = 1000 / Ship.FPS
        self._counter = pygame.time.get_ticks()
        self._rotate_direction = 0
        self._move_direction = 0

        self._speedX = 0.0
        self._speedY = 0.0
        self._speed = 0.0

    def set_direction(self, dir):
        self._direction = dir

    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.centery

    @staticmethod
    def set_fps(fps):
        Ship.FPS = fps

    def set_Speed(self, shipSpeed):
        self._speed = shipSpeed

    def move(self, dir, stop=False):
        '''
        Calls accelerate at direction and ships speed.
        Takes arguement:
            Ship.MOV_FORWARDS = accelerate in the current facing direction.
            Ship.MOV_BACKWARDS = accelerate opposite of the current facing direction.
            Ship.MOV_STOP = stop accelerating.
        '''
        if stop:
            if dir == self._move_direction:
                self._move_direction = Ship.ROT_STOP
        elif dir in (Ship.MOV_FORWARDS, Ship.MOV_BACKWARDS, Ship.MOV_STOP):
            self._move_direction = dir
        else:
            raise Exception('Invalid movement direction')

    def rotate(self, dir, stop=False):
        '''
        Sets the direction of rotation.
        Takes arguement:
            Ship.ROT_RIGHT = Rotate Right or clockwise
            Ship.ROT_LEFT = Rotate Left or counter-clockwise
            Ship.ROT_STOP = Stops Rotation
        '''
        if stop:
            if dir == self._rotate_direction:
                self._rotate_direction = Ship.ROT_STOP
        elif dir in (Ship.ROT_RIGHT, Ship.ROT_LEFT, Ship.ROT_STOP):
            self._rotate_direction = dir
        else:
            raise Exception('Invalid rotation direction')


    def accelerate(self, rads, speed, use_degrees=False):
        '''

        '''
        if speed == 0:
            return

        if use_degrees:
            rads = rads * pi / 180

        rads -= pi / 2
        self._speedX += cos(rads) * speed
        self._speedY += sin(rads) * speed

    def update(self, time):
        if time > self._counter + self._delay:
            self._counter = time

            # Base image right now
            base_image = Ship.SCALED_IMAGES.get('%s - %s' % (self.model, self.base))

            # Add the current engine level
            engine_image = Ship.SCALED_IMAGES.get('%s - off' % self.model).copy()
            engine_image.blit(base_image, base_image.get_rect())
            output_image = engine_image

            # Updates side-burn
            if self._rotate_direction != Ship.ROT_STOP:
                burn_image = 'ship1 - left' if self._rotate_direction == Ship.ROT_LEFT else 'ship1 - right'
                burn_image = Ship.SCALED_IMAGES.get(burn_image).copy()

                burn_image.blit(output_image, output_image.get_rect())
                output_image = burn_image

            # Ship Rotation
            self._direction = self._direction + (self._rotate_direction * pi / Ship.FPS)
            self.image = pygame.transform.rotate(output_image, self._direction * 180 / pi)
            self.rect = self.image.get_rect(center = self.rect.center)

            # Ship Accelerate From Engine
            self.accelerate(self._direction, self._move_direction * self._speed / Ship.FPS)

            # Ship Move
            # TODO: Make it not run off screen?
            self.rect.centerx += self._speedX
            self.rect.centery -= self._speedY


