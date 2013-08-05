import pygame
import os.path

class Ship(pygame.sprite.Sprite):
    IMAGE = pygame.image.load(os.path.join('Resources', 'sprites', 'ship', 'Ship - off.png'))
    ROT_RIGHT = 1
    ROT_LEFT = 2

    def __init__(self):
        super(Ship, self).__init__()

        self.rect = Ship.IMAGE.get_rect()

        self.image = pygame.transform.smoothscale(Ship.IMAGE, (self.rect.width / 4, self.rect.height / 4))

        self.rect = self.image.get_rect()
        self.rect.centerx = 50
        self.rect.centery = 50

        self._direction = 0

    def move():
        '''

        '''

    def rotate(self, d, angle):
        '''

        '''
        if d == ROT_RIGHT:
            IMAGE = pygame.transform.rotate(IMAGE, - angle)
        elif d == ROT_LEFT:
            IMAGE = self._ship = pygame.transform.rotate(IMAGE, angle)

    def accelerate(self, rads, speed):
        '''

        '''
