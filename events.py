from event_handler import EventHandler, Mods
from pygame import locals as const
from ship import Ship

import pygame
import sys


handler = EventHandler()

@handler.quit
@handler.shortcut(Mods.META, const.K_q)
@handler.shortcut(Mods.ALT, const.K_q)
def quit(context):
    pygame.quit()
    sys.exit()

@handler.keydown(const.K_d)
def rotate_left(context):
    context.ship.rotate(Ship.ROT_RIGHT)

@handler.keyup(const.K_d)
def rotate_right_stop(context):
    context.ship.rotate(Ship.ROT_RIGHT, stop=True)

@handler.keydown(const.K_a)
def rotate_left(context):
    context.ship.rotate(Ship.ROT_LEFT)

@handler.keyup(const.K_a)
def rotate_left_stop(context):
    context.ship.rotate(Ship.ROT_LEFT, stop=True)

DEBUG = False
if DEBUG:
    def locate_key(val):
        for key, value in const.__dict__.iteritems():
            if value == val and (key.startswith('K_') or key.startswith('KMOD')):
                print key

    @handler.event(const.KEYDOWN)
    def debug_keys(context):
        print '-' * 15
        print '-- Key'
        locate_key(context.event.key)
        print '-- Mod'
        locate_key(context.event.mod)
        print '-' * 15
