from mediator import Mediator, MediatorEvent, MediatorException


class BaseLoadMediator(Mediator):
    '''
    A Mediator that shows a loading screen
    '''

    def __init__(self, mediator, clock=None):
        '''
        A mediator that shows a loading screen, starting the given mediator once loaded
        or closing it if exiting
        '''
        if not isinstance(mediator, Mediator):
            raise MediatorException("Can't start without a Mediator sub-class to load")

        self._mediator = mediator
        self._loader = None

        super(BaseLoadMediator, self).__init__(clock)

    def _tick(self, screen):
        # Set up the preloader
        if self._loader is None:
            self._loader = mediator.preload(screen)

        load_event = self._load_next()
        if load_event is not None:
            self._load_msg(load_event)

        super(BaseLoadMediator, self)._run(self, screen)

    def _load_next(self):
        '''
        Does one more of the loading steps, returning its message, if None is
        returned, the loader is still working on the previous step
        '''
        try:
            return self._loader.next()
        except StopIteration:
            self._loader = None

            # When we close we also close our saved mediator,
            # We don't want that so we set it to None instead
            mediator = self._mediator_cls(self._kwargs)

            raise Mediator.SwapForEvent(mediator, pop=True)


    #######################################################
    # Sub class Methods
    #######################################################

    def _load_msg(self):
        '''
        Occurs when a load message comes in from the loading Mediator
        '''


