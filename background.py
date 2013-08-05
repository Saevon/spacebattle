from random import choice as randchoice

import os
import pygame


IMAGE_PATH = os.path.join('Resources', 'backgrounds')

(
    KEEP,
    STRETCH,
) = range(2)

def load(image=None, options=KEEP, resolution=None):
    images = {}
    for key in os.listdir(IMAGE_PATH):
        # ignore hidden files
        if key.startswith('.'):
            continue
        images[os.path.splitext(key)[0]] = os.path.join(IMAGE_PATH, key)


    if image is None or image not in images.keys():
        image = randchoice(images.keys())

    image = pygame.image.load(images[image])

    # scale if needed
    if options == STRETCH and resolution is not None:
        image = pygame.transform.smoothscale(image, resolution)

    return image









