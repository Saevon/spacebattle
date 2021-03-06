from pygame import locals as const
from functools import wraps


class Context(dict):
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

class Mods:
    (
        SHIFT,
        META,
        ALT,
        CTRL,
    ) = [2 ** k for k in range(1, 5)]

    MAP = {
        const.KMOD_SHIFT: SHIFT,
        const.KMOD_META: META,
        const.KMOD_ALT: ALT,
        const.KMOD_CTRL: CTRL,
    }

class EventManager(object):


    def __init__(self, context=None):
        self.on_quit = []
        self.on_generic = {}
        self.on_shortcut = {}
        self.on_keydown = {}
        self.on_keyup = {}
        self.on_mouseclick = {}

        if context is None:
            context = Context()

        self.context = context

    #######################################################
    # EVENT REGISTRATIONS
    #######################################################
    @staticmethod
    def _append_wrapper_with_const(loc, key, const=None):
        '''
        HELPER: returns a wrapper that will append a func to the given loc
            with the given key. Also adds an extra const wrapper if that is provided
        '''
        def wrapper(func):
            # If we have constants, we call the function with a closure
            if const is not None:
                @wraps(func)
                def closure(*args, **kwargs):
                    # we use the const values first, but they get overwritten by keyword args
                    input_kwargs = dict(**const)
                    input_kwargs.update(**kwargs)

                    return func(*args, **input_kwargs)

                handler = closure
            else:
                handler = func

            # Add it to the callbacks
            loc[key].append(handler)

            # Always return the original
            # That lets us chain different events with differing constants in one line
            return func
        return wrapper


    def quit(self, handler):
        '''
        Adds a handler for the QUIT event (clicking the x button)
        '''
        self.on_quit.append(handler)
        return handler

    def shortcut(self, modifiers, key, const=None):
        '''
        Adds a handler for a shortcut (a key combination)
        '''
        if modifiers is None:
            modifiers = 0

        handlers = self.on_shortcut.get(modifiers, False)
        if not handlers:
            self.on_shortcut[modifiers] = {}

        handlers = self.on_shortcut[modifiers].get(key, False)
        if not handlers:
            self.on_shortcut[modifiers][key] = []

        loc = self.on_shortcut[modifiers]
        return EventManager._append_wrapper_with_const(loc, key, const)

    def keyup(self, key, const=None):
        '''
        Adds a handler for the keyup event
        '''
        handlers = self.on_keyup.get(key, False)
        if not handlers:
            self.on_keyup[key] = []

        loc = self.on_keyup
        return EventManager._append_wrapper_with_const(loc, key, const)

    def keydown(self, key, const=None):
        '''
        Adds a handler for the keydown event
        '''
        handlers = self.on_keydown.get(key, False)
        if not handlers:
            self.on_keydown[key] = []

        loc = self.on_keydown
        return EventManager._append_wrapper_with_const(loc, key, const)

    def mouseclick(self, key, const=None):
        handlers = self.on_mouseclick.get(key, False)
        if not handlers:
            self.on_mouseclick[key] = []

        loc = self.on_mouseclick
        return EventManager._append_wrapper_with_const(loc, key, const)

    def event(self, key, const=None):
        '''
        Adds a handler for any other event, its type is given by key
        '''
        handlers = self.on_generic.get(key, False)
        if not handlers:
            self.on_generic[key] = []

        loc = self.on_generic
        return EventManager._append_wrapper_with_const(loc, key, const)

    def tick(self, time=1000):
        '''
        Adds a handler that gets called every time milliseconds

        callback(context, time):
            time `int`
                how long since the last call in ticks

        Warning: this will never go faster then the FPS clock
            so use the given time variable in case some time was skipped
        Warning: something needs to be triggering the tick event
        '''
        # TODO


    #######################################################
    # Main Functions
    #######################################################

    def _get_modifiers(self, flag):
        '''
        HELPER: Transforms the pygame modifiers into EventManager modifiers
        '''
        modifiers = 0

        for key, value in Mods.MAP.iteritems():
            if flag & key:
                modifiers |= value

        return modifiers

    def _call_handlers(self, handlers):
        '''
        HELPER: calls a list of handlers
        '''
        if not handlers:
            return

        for handler in handlers:
            handler(self.context)

    def __call__(self, events):
        '''
        Handles the given events
        '''
        self._handle(events)

    def _handle(self, events):
        '''
        Handles each of the given events
        '''
        self.context.handler = self
        context = self.context

        for event in events:
            context.event = event

            if event.type == const.QUIT:
                self._call_handlers(self.on_quit)
            elif event.type == const.KEYDOWN:
                mod = self._get_modifiers(event.mod)
                handlers = self.on_shortcut.get(mod, False)
                if handlers:
                    handlers = handlers.get(event.key, False)
                    self._call_handlers(handlers)

                handlers = self.on_keydown.get(event.key, False)
                self._call_handlers(handlers)
            elif event.type == const.KEYUP:
                handlers = self.on_keyup.get(event.key, False)
                self._call_handlers(handlers)
            elif event.type == const.MOUSEBUTTONDOWN:
                handlers = self.on_mouseclick.get(event.button, False)
                self._call_handlers(handlers)

            # generic events
            handlers = self.on_generic.get(event.type, False)
            self._call_handlers(handlers)


