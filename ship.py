import pygame
import os.path

class Ship(pygame.sprite.Sprite):
    IMAGE = pygame.image.load(os.path.join('Resources', 'sprites', 'ship', 'Ship - off.png'))
    ROT_RIGHT = 1
    ROT_LEFT = 2

    def __init__(self):
        self.rect = Ship.IMAGE.get_rect()

        self.width = self.rect.width / 4
        self.height = self.rect.height / 4
    
        self.image = pygame.transform.smoothscale(Ship.IMAGE, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.centerx = 50
        self.rect.centery = 50
        
        self._direction = 0
        self._delay = 1000 / Ship.FPS

    @staticmethod
    def set_fps(fps):
        Ship.FPS = fps
        
    def move():
        '''

        '''
        
    def rotate(self, d):
        '''
        
        '''
        if d == Ship.ROT_RIGHT:
            self.rotate = -1
        elif d == Ship.ROT_LEFT:
            self.rotate = 1
        else:
            self.rotate = 0

   #     self._direction += angle
   #     self.image = pygame.transform.smoothscale(Ship.IMAGE, (self.width, self.height))
   #     self.image = pygame.transform.rotate(self.image, self._direction)
   #     self.rect = self.image.get_rect(center = self.rect.center)

    def update(self, time):
        if time > self._counter + self._delay:
            self._counter = time

            self.rotate_speed = self.rotate * 90 / Ship.FPS
            self.image = pygame.transform.rotate(self.image, self.rotate_speed)
            self.rect = self.image.get_rect(center = self.rect.center)
            
    def accelerate(self, rads, speed):
        '''

        '''
