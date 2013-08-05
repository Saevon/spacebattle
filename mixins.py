import pygame.image
import os.path


class ImageBatch(object):
    '''
    Mixin that adds a load method
    '''

    IMAGES = {}

    @classmethod
    def load(cls):
        # super(ImageBatch, cls).load()

        cls.IMAGES = {}

        for key in os.listdir(cls.IMAGE_PATH):
            if key.endswith('.png'):
                cls.IMAGES[os.path.splitext(key)[0]] = pygame.image.load(
                    os.path.join(cls.IMAGE_PATH, key)
                )
