from pygame import locals as const
import pygame
import sys


# Missing Mouse button constants
MOUSEKEY_LEFT = 1
MOUSEKEY_MIDDLE = 2
MOUSEKEY_RIGHT = 3

MOUSEKEY_SCROLLUP = 4
MOUSEKEY_SCROLLDOWN = 5


# Pygame startup MUST HAPPEN FIRST
pygame.init()

clock = pygame.time.Clock()

resolution = (640, 480)
window = pygame.display.set_mode(resolution)
pygame.display.set_caption('Space Battle')

background = pygame.image.load('stars.jpg')

count = 0

WHITE = pygame.Color(255, 255, 255)
FPS = 30

running = True
while running:
    window.fill(WHITE)

    window.blit(background, background.get_rect())

    # Event handling
    for event in pygame.event.get():
        if event.type == const.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == const.MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == const.MOUSEBUTTONUP:
            mousex, mousey = event.pos

            event.button == MOUSEKEY_RIGHT

        elif event.type == const.KEYDOWN:
            if event.key == const.K_q and event.mod & const.KMOD_META:
                pygame.quit()
                sys.exit()

            if event.key == const.K_a and event.mod & (const.KMOD_META | const.KMOD_SHIFT):
                print '!!'





    # Draw the screen ever FPS frames
    pygame.display.update()
    clock.tick(FPS)


