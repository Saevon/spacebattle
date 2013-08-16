from pygame import locals as const
import pygame
import os.path

from celestials import Sun, Planet
from event_handler import Context
from ship import Ship
from time import time

from math import pi

import background
import events


# Constants
FPS = 30

# Pygame startup MUST HAPPEN FIRST
pygame.init()



# Global object that an event can manipulate
events.handler.context = Context({
    # 'players': {
    #     1: player1,
    #     2: player2,
    #     3: player3,
    #     4: player4,
    # },
})

from menu.mediators import MainMediator

resolution = (640, 480)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('Space Battle')

game = MainMediator()
game.run(screen)

pygame.quit()

