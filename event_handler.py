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

class EventHandler(object):


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
        return EventHandler._append_wrapper_with_const(loc, key, const)

    def keyup(self, key, const=None):
        '''
        Adds a handler for the keyup event
        '''
        handlers = self.on_keyup.get(key, False)
        if not handlers:
            self.on_keyup[key] = []

        loc = self.on_keyup
        return EventHandler._append_wrapper_with_const(loc, key, const)

    def keydown(self, key, const=None):
        '''
        Adds a handler for the keydown event
        '''
        handlers = self.on_keydown.get(key, False)
        if not handlers:
            self.on_keydown[key] = []

        loc = self.on_keydown
        return EventHandler._append_wrapper_with_const(loc, key, const)

    def mouseclick(self, key, const=None):
        handlers = self.on_mouseclick.get(key, False)
        if not handlers:
            self.on_mouseclick[key] = []

        loc = self.on_mouseclick
        return EventHandler._append_wrapper_with_const(loc, key, const)

    def event(self, key, const=None):
        '''
        Adds a handler for any other event, its type is given by key
        '''
        handlers = self.on_generic.get(key, False)
        if not handlers:
            self.on_generic[key] = []

        loc = self.on_generic
        return EventHandler._append_wrapper_with_const(loc, key, const)



    def __call__(self, events):
        self.handle(events, self.context)

    def _get_modifiers(self, flag):
        '''
        Transforms the pygame modifiers into EventHandler modifiers
        '''
        modifiers = 0

        for key, value in Mods.MAP.iteritems():
            if flag & key:
                modifiers |= value

        return modifiers

    def handle(self, events, context):
        '''
        Handles each of the given events with the given context
        '''
        context.handler = self

        for event in events:
            context.event = event

            if event.type == const.QUIT:
                map(lambda handler: handler(event), self.on_quit)
            elif event.type == const.KEYDOWN:
                mod = self._get_modifiers(event.mod)
                handlers = self.on_shortcut.get(mod, False)
                if handlers:
                    handlers = handlers.get(event.key, False)
                    if handlers:
                        map(lambda handler: handler(context), handlers)

                handlers = self.on_keydown.get(event.key, False)
                if handlers:
                    map(lambda handler: handler(context), handlers)
            elif event.type == const.KEYUP:
                handlers = self.on_keyup.get(event.key, False)
                if handlers:
                    map(lambda handler: handler(context), handlers)
            elif event.type == const.MOUSEBUTTONDOWN:
                handlers = self.on_mouseclick.get(event.button, False)
                if handlers:
                    map(lambda handler: handler(context), handlers)


            # generic events
            handlers = self.on_generic.get(event.type, False)
            if handlers:
                map(lambda handler: handler(context), handlers)
