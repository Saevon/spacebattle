import pygame
import os.path

class Ship(pygame.sprite.Sprite):
    # Original Image
    IMAGE = pygame.image.load(os.path.join('Resources', 'sprites', 'ship', 'Ship - off.png'))

    # Rotation Direction Constants
    ROT_RIGHT = 1
    ROT_LEFT = 2
    ROT_STOP = 3

    def __init__(self):
        super(Ship, self).__init__()

        self.rect = Ship.IMAGE.get_rect()

        self.width = self.rect.width / 4
        self.height = self.rect.height / 4
    
        self.image_original = pygame.transform.smoothscale(Ship.IMAGE, (self.width, self.height))
        self.image = self.image_original

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

    def rotate(self, d):
        '''
        Sets the direction of rotation.
        Takes arguement:
            Ship.ROT_RIGHT = Rotate Right or clockwise
            Ship.ROT_LEFT = Rotate Left or counter-clockwise
            Ship.ROT_STOP = Stops Rotation
        '''
        if d == Ship.ROT_RIGHT:
            self._rotate_direction = -1
        elif d == Ship.ROT_LEFT:
            self._rotate_direction = 1
        elif d == Ship.ROT_STOP:
            self._rotate_direction = 0
        else:
            return

    def accelerate(self, rads, speed):
        '''
        
        '''
        
    def update(self, time):
        if time > self._counter + self._delay:
            self._counter = time

            # Ship Rotation
            self._direction = self._direction + (self._rotate_direction * 180 / Ship.FPS)
            self.image = pygame.transform.rotate(self.image_original, self._direction)
            self.rect = self.image.get_rect(center = self.rect.center)
