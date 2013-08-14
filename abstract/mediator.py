

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

    def __init__(self):
        self.is_frozen = True
        self.is_alive = True

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
    def load(cls):
        '''
        Loads all the data this MediatorClass needs to run.
        Load does not need to be called, as just running an instance will
        still call it. This is only useful if you need to pre-load the mediator.
            e.g. in a loading screen
        '''
        # Don't load things twice
        if getattr(cls, 'is_loaded', False):
            return

        msgs = cls._load()

        # Allow non-generator methods as well
        if msgs is None:
            return

        # Generate all the loading messages for this class
        for msg in msgs:
            yield msg

        # Mark this class as loaded
        cls.is_loaded = True

    @classmethod
    def unload(cls):
        '''
        Unloads all the data this MediatorClass needs to run.
        This is used when this MediatorClass will not be used for a long while
        '''
        if not getattr(cls, 'is_loaded', False):
            raise MediatorException("Can't unload MediatorClass, it wasn't loaded")

        msgs = cls._unload()

        # Allow non-generator methods as well
        if msgs is None:
            return

        # Generate all the loading messages for this class
        for msg in msgs:
            yield msg

        # Mark this class as unloaded
        cls.is_loaded = False

    def tick(self, screen, events, delta_ms):
        '''
        Process the given events, then update the view for this mediator
        '''
        if self.is_frozen:
            self.unfreeze()

        if self._child:
            method = self._child.tick
            exception_type = MediatorParentEvent
        else:
            method = self._tick
            exception_type = MediatorEvent

        # Run the tick code, catching any of the raised MediatorEvents
        try:
            method(screen, events, delta_ms)
        except exception_type as event:
            handler = getattr(self, event.HANDLER, False)
            if not handler:
                raise MediatorException('Mediator Event handler does not exist: %s' % event.HANDLER)
            handler(event)
        except BaseMediatorEvent as err:
            raise MediatorException("Invalid MediatorEvent, not caught by current handler: %s" % err)

    def draw(self, screen):
        '''
        Draws the view unto the given screen without doing any updates
        '''
        self._draw(screen)

    #######################################################
    # Private Helpers
    #######################################################

    def _tick(self, screen, events, delta_ms):
        '''
        Called every tick when you're the active mediator
        '''
        # Process the events
        self.event_manager.handle(events)

        # Re-draw the view
        self.update(delta_ms)
        self.draw(screen)

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

    def finish(self):
        '''
        Calls the finish handler for the current mediator

        NOT for public use
        '''
        if self.is_alive:
            raise MediatorException("Mediator already finished")

        self.is_alive = False
        self._finish()

    #######################################################
    # Sub class Methods
    #######################################################

    @classmethod
    def _load(cls):
        '''
        Called to load the classes variables for later initialization
        This method should be a generator that provides loading progress
        '''

    @classmethod
    def _unload(cls):
        '''
        Called to unload the classes variables
        This method should be a generator that provides unloading progress
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

    def _draw(self, screen):
        '''
        Called every time we need to re-draw the display
        '''

    def _update_views(self, delta_time):
        '''
        Called when we need to update the views (animate)
        '''

    def _update_models(self, delta_time):
        '''
        Called when we need to update the models
        '''




