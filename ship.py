import pygame
import os.path
from mixins import ImageBatch


class Ship(pygame.sprite.Sprite, ImageBatch):
    # Original Image
    IMAGE_PATH = os.path.join('Resources', 'sprites', 'ship')

    # Rotation Direction Constants
    ROT_RIGHT = -1
    ROT_LEFT = 1
    ROT_STOP = 0

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

    def __init__(self):
        super(Ship, self).__init__()

        self.image = Ship.SCALED_IMAGES.get('ship1')

        self.rect = self.image.get_rect()
        self.rect.centerx = 50
        self.rect.centery = 50

        self._direction = 0
        self._delay = 1000 / Ship.FPS
        self._counter = pygame.time.get_ticks()
        self._rotate_direction = 0
        self._speed = 10

    @staticmethod
    def set_fps(fps):
        Ship.FPS = fps

    def move():
        '''
        Calls accelerate at direction and ships speed.
        '''
        self.accelerate(self._direction, self._speed)

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


    def accelerate(self, rads, speed):
        '''

        '''

    def update(self, time):
        if time > self._counter + self._delay:
            self._counter = time

            # Base image right now
            base_image = Ship.SCALED_IMAGES.get('ship1')

            # Add the current engine level
            engine_image = Ship.SCALED_IMAGES.get('ship1 - off').copy()
            engine_image.blit(base_image, base_image.get_rect())
            output_image = engine_image

            # Updates side-burn
            if self._rotate_direction != Ship.ROT_STOP:
                burn_image = 'ship1 - left' if self._rotate_direction == Ship.ROT_LEFT else 'ship1 - right'
                burn_image = Ship.SCALED_IMAGES.get(burn_image).copy()

                burn_image.blit(output_image, output_image.get_rect())
                output_image = burn_image

            # Ship Rotation
            self._direction = self._direction + (self._rotate_direction * 180 / Ship.FPS)
            self.image = pygame.transform.rotate(output_image, self._direction)
            self.rect = self.image.get_rect(center = self.rect.center)




