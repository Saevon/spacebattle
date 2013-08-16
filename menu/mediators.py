from abstract import mediator
from abstract import event_manager

from pygame import locals as const
import pygame

class PygameClock(object):
    '''
    A clock using the pygame clock
    '''

    def __init__(self, fps=None):
        self.fps = fps
        self._clock = pygame.time.Clock()

        self.reset()

    def delta(self):
        '''
        Returns the time in milliseconds since the last call of this method
        '''
        now = pygame.time.get_ticks()

        # If we have no time, then the first time we call delta is the starting time
        # aka delta == 0 as no time passed
        if self._time is None:
            delta = 0
        else:
            delta = now - self._time

        # Make sure to update the current time
        self._time = now

        # TODO: update the FPS average

        return delta

    def fps_sleep(self):
        '''
        Sleeps until the clock is running N Frames per Second
        This just ensures you run no faster than the fps, though you can
        run slower
        '''
        if self.fps is None:
            return

        self._clock.tick(self.fps)

    def get_average_fps(self):
        '''
        Returns the current FPS average
        '''
        # TODO

    def reset(self):
        '''
        Resets the clock, using the next delta() call to syncronize it
        '''
        self._time = None


WHITE = pygame.Color(255, 255, 255)

class PygameMediatorMixin(object):
    '''
    A Mixin making the Mediator use pygame methods
    '''

    def __init__(self, clock=None):
        # Pygame uses the pygame clock
        if clock is None:
            clock = PygameClock()

        super(PygameMediatorMixin, self).__init__(clock)

    def get_events(self):
        return pygame.event.get()

    def _clear_screen(self, screen):
        screen.fill(WHITE)

    def _draw_screen(self, screen):
        pygame.display.update()


from menu.controllers import game_handler, pause_handler
import background
from celestials import Sun, Planet
from ship import Ship

from abstract.view import ImageView
from abstract import pause
from math import pi

class MainMediator(mediator.Mediator):

    def _preload(self, screen):
        game = GameMediator()

        raise mediator.Mediator.PutEvent(game)

    def _on_return(self, value):
        raise mediator.Mediator.PopEvent()


class PauseMediator(PygameMediatorMixin, pause.BasePauseMediator):
    def _preload(self, screen):
        yield 'Setting Screenshot'
        screenshot = screen.copy()
        yield
        self._mediator.draw(screenshot)
        yield

        self.views.append(ImageView(screenshot))

        self.controller = pause_handler
        self.controller.context.mediator = self

class GameMediator(PygameMediatorMixin, mediator.Mediator):

    FPS = 30

    def pause(self):
        pause = PauseMediator(self)
        raise mediator.Mediator.SwapForEvent(pause, pop=False)

    def _preload(self, screen):
        rect = screen.get_rect()
        resolution = (rect.width, rect.height)

        yield 'Loading Events'
        self.controller = game_handler
        self.controller.context.mediator = self

        yield 'Loading Background'
        self.bg = ImageView(
            background.load(options=background.STRETCH, resolution=resolution)
        )
        self.views.append(self.bg)

        yield 'Loading Planets'
        for msg in Planet.load():
            yield msg

        yield 'Loading Stars'
        Sun.set_fps(GameMediator.FPS)

        yield 'Loading Sector'
        self.celestials = []

        sun = Sun(resolution[0] / 2, resolution[1] / 2, 50)
        self.celestials.append(sun)
        self.views.append(sun)
        yield

        planet = Planet(0, 0, 8)
        planet.orbit(sun, 140)
        self.celestials.append(planet)
        self.views.append(planet)
        yield

        planet = Planet(0, 0, 10)
        planet.orbit(sun, 60)
        self.celestials.append(planet)
        self.views.append(planet)
        yield

        planet = Planet(0, 0, 30)
        planet.orbit(sun, 200)
        self.celestials.append(planet)
        self.views.append(planet)
        yield

        yield 'Building Ships'
        for msg in Ship.load():
            yield msg

        Ship.set_fps(GameMediator.FPS)

        yield 'Spawning Players'
        self.players = {}

        player1 = Ship(50, 50, base='purple')
        player1.set_MoveSpeed(10)
        player1.set_TurnSpeed(pi)
        player1.set_direction(0)
        self.views.append(player1)
        self.players[1] = player1
        yield

        player2 = Ship(600, 50, base='red')
        player2.set_MoveSpeed(10)
        player2.set_TurnSpeed(pi)
        player2.set_direction(-pi/4)
        self.views.append(player2)
        self.players[2] = player2
        yield

        player3 = Ship(50, 400, base='green')
        player3.set_MoveSpeed(10)
        player3.set_TurnSpeed(pi)
        player3.set_direction(pi/2)
        self.views.append(player3)
        self.players[3] = player3
        yield

        player4 = Ship(600, 400, base='blue')
        player4.set_MoveSpeed(10)
        player4.set_TurnSpeed(pi)
        player4.set_direction(-pi/2)
        self.views.append(player4)
        self.players[4] = player4
        yield

        yield 'Applying Gravity'
        for celestial in self.celestials:
            celestial.pull_on(player1)
            celestial.pull_on(player2)
            celestial.pull_on(player3)
            celestial.pull_on(player4)



