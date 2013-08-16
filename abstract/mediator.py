from time import time


class BaseMediatorEvent(Exception):
    '''
    A wrapper for an event that tells the mediators to do something at the end
    of the current tick
    '''

class MediatorParentEvent(BaseMediatorEvent):
    '''
    A MediatorEvent that can only be processed by the parent of the mediator
    '''

class MediatorEvent(BaseMediatorEvent):
    '''
    A MediatorEvent that can only be processed by the currently active mediator
    (The one that raises this exception)
    '''



class MediatorException(Exception):
    '''
    A base exception raised by mediator objects if they break in their main interface
    '''

class Clock(object):
    '''
    A simple clock that finds out how much time passed since its last call
    '''

    def __init__(self, fps=None):
        self.fps = fps

        self.reset()

    def delta(self):
        '''
        Returns the time in milliseconds since the last call of this method
        '''
        now = time()

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
        # TODO

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

class BaseController(object):
    def __call__(self, events):
        '''
        Proccesses the given events
        '''


class Mediator(object):
    '''
    A MVC facade, it allows you to group Models, Views and Controllers into differing tasks
        e.g. 'Main Menu' vs 'Game'
    Each mediator should either initialize some MVC objects or should accept them as args
    from the parent that creates it

    Note: each of the Model, View and Controller classes are mapped to the ones below
        Model: ? TODO ?
        View: ? TODO ?
        Controller: EventManager
    '''

    def __init__(self, clock=None):
        '''
        This should set defaults for required instance variables, _preload should
        do any other start-up code
        '''
        self.is_frozen = True
        self.is_alive = True
        self.has_started = False

        self._child = None

        if clock is None:
            clock = Clock()
        self.clock = clock

        self.views = []
        self.models = []
        self.controller = BaseController()

    #######################################################
    # Mediator Events
    #######################################################

    class PutEvent(MediatorEvent):
        '''
        Adds a child mediator
        '''
        HANDLER = '_put'

        def __init__(self, mediator):
            if not isinstance(mediator, Mediator):
                raise MediatorException("We can't Put a non Mediator sub-class")

            self.mediator = mediator

    def _put(self, event):
        '''
        Mediator Event Handler for the PutEvent.
        '''
        self._child = event.mediator

    class PopEvent(MediatorParentEvent):
        '''
        Closes the current mediator, effectively deleting it
        '''
        HANDLER = '_pop'

    def _pop(self, event):
        '''
        Mediator Event Handler for the PopEvent
        '''
        # Ensure this is a valid event
        if not self._child:
            raise MediatorException("No mediator to pop")

        value = self._child.finish()
        self._child = None
        self._on_return(value)


    class SwapForEvent(MediatorParentEvent):
        '''
        Swaps the current mediator for the given mediator, either freezing or poppingthe current mediator
        '''
        HANDLER = '_swap_for'

        def __init__(self, mediator, pop=True):
            if not isinstance(mediator, Mediator):
                raise MediatorException("We can't SwapFor a non Mediator sub-class")

            self.mediator = mediator
            self.pop = pop

    def _swap_for(self, event):
        '''
        Mediator Event Handler for the SwapForEvent
        '''
        # Ensure this is a valid event
        if not self._child:
            raise MediatorException("Can't swap from non-existent mediator")

        # Close the old mediator
        if event.pop:
            self._child.finish()
        else:
            self._child.freeze()

        # Start up the new mediator
        self._child = event.new
        self._child.unfreeze()


    #######################################################
    # Public usage Methods
    #######################################################

    @classmethod
    def load_class(cls):
        '''
        Loads all the data this MediatorClass needs to run.
        Load does not need to be called, as just running an instance will
        still call it. This is only useful if you need to pre-load the mediator.
            e.g. in a loading screen
        '''
        # Don't load things twice
        if getattr(cls, 'is_loaded', False):
            return

        msgs = cls._load_class()

        # Allow non-generator methods as well
        if msgs is None:
            return

        # Generate all the loading messages for this class
        for msg in msgs:
            yield msg

        # Mark this class as loaded
        cls.is_loaded = True

    @classmethod
    def unload_class(cls):
        '''
        Unloads all the data this MediatorClass needs to run.
        This is used when this MediatorClass will not be used for a long while
        '''
        if not getattr(cls, 'is_loaded', False):
            raise MediatorException("Can't unload MediatorClass, it wasn't loaded")

        msgs = cls._unload_class()

        # Allow non-generator methods as well
        if msgs is None:
            return

        # Generate all the loading messages for this class
        for msg in msgs:
            yield msg

        # Mark this class as unloaded
        cls.is_loaded = False

    def run(self, screen):
        '''
        Run the current Mediator until it quits
        '''
        try:
            while True:
                self._run(screen)
        except BaseMediatorEvent:
            pass

    def draw(self, screen):
        '''
        Draws the view unto the given screen without doing any updates
        '''
        for view in self.views:
            view.draw(screen)

    def update(self, delta_time):
        '''
        Updates the models, then the views with the new time delta
        '''
        for model in self.models:
            model.update(delta_time)

        for view in self.views:
            view.update(delta_time)

    def handle_events(self, events):
        '''
        Gets the controller to proccess the passed in events
        '''
        self.controller(events)

    def get_events(self):
        '''
        Returns a list of events that got generated since the last call of this method
        '''
        return []

    #######################################################
    # Private Helpers
    #######################################################

    def _run(self, screen):
        '''
        Starts up either you or your child
        '''
        # Remember to run your child code instead if you have a child
        if self._child:
            method = self._child._run
            exception_type = MediatorParentEvent
        else:
            method = self._loop
            exception_type = MediatorEvent

        # Run the tick code, catching any of the raised MediatorEvents
        try:
            method(screen)
        except BaseMediatorEvent as event:
            # Any events not of the valid type get sent to the parent
            if not isinstance(event, exception_type):
                raise event

            handler = getattr(self, event.HANDLER, False)
            if not handler:
                raise MediatorException(
                    'Mediator Event handler does not exist: %s' % event.HANDLER
                )
            handler(event)

    def _loop(self, screen):
        '''
        Called to begin the main loop for this Mediator
        '''
        # Start up, throwing out the loading messages
        if not self.has_started:
            [msg for msg in self.preload(screen)]

        if self.is_frozen:
            self.unfreeze()

        while True:
            self._tick(screen)

    def _tick(self, screen):
        '''
        Runs throught one iteration of the main loop for this Mediator
        '''
        # Calculate how long its been since the last call
        delta_time = self.clock.delta()

        # Process the events
        self.handle_events(self.get_events())

        # Re-draw the view
        self._clear_screen(screen)
        self.update(delta_time)
        self.draw(screen)
        self._draw_screen(screen)

        # ensure we run with a proper FPS
        self.clock.fps_sleep()

    #######################################################
    # Events (Not for Public use)
    #######################################################
    def unfreeze(self):
        '''
        Calls the unfreeze handler for the current mediator

        NOT for public use
        '''
        if not self.is_frozen:
            raise MediatorException("Mediator already unfrozen")

        # Restart the timer to now
        self.clock.reset()

        self.is_frozen = False
        self._unfreeze()

    def freeze(self):
        '''
        Calls the freeze handler for the current mediator

        NOT for public use
        '''
        if self.is_frozen:
            raise MediatorException("Mediator already frozen")

        self.is_frozen = True
        self._freeze()

    def preload(self, screen):
        '''
        Loads up the class right before it starts for the first time
        This method will not change the screen

        This is a generator
        '''
        if self.has_started:
            return
        self.has_started = True

        msgs = self._preload(screen)

        # We might not have a generator
        if msgs is None:
            return

        for msg in msgs:
            yield msg

    def finish(self):
        '''
        Calls the finish handler for the current mediator

        NOT for public use
        '''
        if not self.is_alive:
            raise MediatorException("Mediator already finished")

        self.is_alive = False
        self._finish()

    #######################################################
    # Sub class Methods
    #######################################################

    @classmethod
    def _load_class(cls):
        '''
        Called to load the classes variables for later initialization
        This method should be a generator that provides loading progress
        '''

    @classmethod
    def _unload_class(cls):
        '''
        Called to unload the classes variables
        This method should be a generator that provides unloading progress
        '''

    def _clear_screen(self, screen):
        '''
        Used to ensure the screen buffer is ready to be drawn to
        '''

    def _draw_screen(self, screen):
        '''
        Ensures the screen is drawn unto the monitor
        '''

    def _preload(self, screen):
        '''
        Called when the class is started (unfreezed) for the first time
        This method should be a generator that provides unloading progress
        This should not change the screen
        '''

    def _freeze(self):
        '''
        Called when this mediator has stopped running, but has not been popped
        This means the mediator *might* be reused, do not assume it will unfreeze
        '''

    def _unfreeze(self):
        '''
        Called when a mediator is unfrozen, aka about to become the running mediator.
        New mediators that have not been run should start as frozen, thus this method
        will be called when they begin
        '''

    def _finish(self):
        '''
        Called when the current mediator is popped, meaning it will never be re-started
        '''

    def _on_return(self, value):
        '''
        Gets called when a child pops, returning a value
        '''





