

class View(object):

    def update(self, delta_time):
        '''
        Updates any animations on this view, after delta_time in milliseconds
        has passed
        '''

    def draw(self, screen):
        '''
        Draws the view unto the given screen
        '''


class ImageView(View):
    def __init__(self, image):
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect())
