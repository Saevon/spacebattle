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

            width = rect.width / 5
            height = rect.height / 5

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

        self._engine_counter = 0
        self._burn_counter = 0

        self._speedX = float(0)
        self._speedY = float(0)

        self._movespeed = float(0)
        self._turnspeed = float(0)

        self._x = float(x)
        self._y = float(y)

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

    def set_MoveSpeed(self, speed):
        self._movespeed = speed

    def set_TurnSpeed(self, speed):
        self._turnspeed = speed

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


    def accelerate(self, rads, speed):
        '''

        '''
        if speed == 0:
            return

        rads -= pi / 2
        self._speedX += cos(rads) * speed
        self._speedY += sin(rads) * speed

    def engine_on_image(self, counter):
        '''

        '''
        return {
            0: 'on - start',
            1: 'on - 1',
            2: 'on - 2',
            3: 'on - 3'
        }[counter]

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
                if self._burn_counter == 0:
                    burn_image = ('%s - left - 1' % (self.model)) if self._rotate_direction == Ship.ROT_LEFT else ('%s - right - 1' % (self.model))
                    self._burn_counter = 1
                elif self._burn_counter == 1:
                    burn_image = ('%s - left - 2' % (self.model)) if self._rotate_direction == Ship.ROT_LEFT else ('%s - right - 2' % (self.model))
                    self._burn_counter = 0

                burn_image = Ship.SCALED_IMAGES.get(burn_image).copy()
                burn_image.blit(output_image, output_image.get_rect())
                output_image = burn_image

            # Updates engine
            if self._move_direction != Ship.MOV_STOP:
                if self._move_direction == Ship.MOV_FORWARDS:
                    engine_image = ('%s - %s' % (self.model, self.engine_on_image(self._engine_counter)))
                    if self._engine_counter < 3:
                        self._engine_counter += 1
                    else:
                        self._engine_counter = 1
                elif self._move_direction == Ship.MOV_BACKWARDS:
                    self._engine_counter = 0
                    engine_image = ('%s - off' % (self.model))

                engine_image = Ship.SCALED_IMAGES.get(engine_image).copy()
                engine_image.blit(output_image, output_image.get_rect())
                output_image = engine_image
            else:
                self._engine_counter = 0

            # Ship Rotation
            self._direction = self._direction + (self._rotate_direction * self._turnspeed / Ship.FPS)
            self.image = pygame.transform.rotate(output_image, self._direction * 180 / pi)
            self.rect = self.image.get_rect(center = self.rect.center)

            # Ship Accelerate From Engine
            self.accelerate(self._direction, float(self._movespeed) * self._move_direction / Ship.FPS)

            # Ship Move
            # TODO: Make it not run off screen?
            self._x += self._speedX
            self._y -= self._speedY
            
            self.rect.centerx = self._x
            self.rect.centery = self._y


