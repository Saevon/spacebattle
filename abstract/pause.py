from mediator import Mediator, MediatorEvent, MediatorException


class PauseMediator(Mediator):
    '''
    A Mediator that shows a pause menu
    '''

    def __init__(self, mediator):
        '''
        A mediator that shows a pause menu, restoring the given mediator once resumed
        or closing it if exiting
        '''
        if not isinstance(mediator, Mediator):
            raise MediatorException("Can't pause without a Mediator sub-class to pause/resume")

        self._mediator = mediator

    #######################################################
    # Mediator Events
    #######################################################

    class ResumeEvent(MediatorEvent):
        '''
        States that the pause screen is to be closed, resuming the frozen mediator
        '''
        HANDLER = '_resume'

    def _resume(self, event):
        '''
        Mediator Event Handler for the ResumeEvent
        '''
        # When we close we also close our saved mediator, so we remove it instead
        mediator = self._mediator
        self._mediator = None

        raise Mediator.SwapForEvent(mediator, pop=True)



    def finish(self):
        # Note: as an abstract Mediator, we don't touch the _finish method, that is only for
        # a concrete Mediator

        # We need to ensure when we close, we also close the saved mediator
        # unless we don't have one (as we're resuming it)
        if self._mediator is not None:
            self._mediator.finish()
            self._mediator = None

        super(PauseMediator, self).finish()


