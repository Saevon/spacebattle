from pygame import locals as const


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

        if context is None:
            context = Context()

        self.context = context

    def quit(self, handler):
        '''
        Adds a handler for the QUIT event (clicking the x button)
        '''
        self.on_quit.append(handler)
        return handler

    def shortcut(self, modifiers, key):
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

        def wrapper(handler):
            self.on_shortcut[modifiers][key].append(handler)
            return handler
        return wrapper

    def keyup(self, key):
        '''
        Adds a handler for the keyup event
        '''
        handlers = self.on_keyup.get(key, False)
        if not handlers:
            self.on_keyup[key] = []

        def wrapper(handler):
            self.on_keyup[key].append(handler)
            return handler
        return wrapper

    def keydown(self, key):
        '''
        Adds a handler for the keydown event
        '''
        handlers = self.on_keydown.get(key, False)
        if not handlers:
            self.on_keydown[key] = []

        def wrapper(handler):
            self.on_keydown[key].append(handler)
            return handler
        return wrapper

    def event(self, event):
        '''
        Adds a handler for any other event, its type is given by event
        '''
        handlers = self.on_generic.get(event, False)
        if not handlers:
            self.on_generic[event] = []

        def wrapper(handler):
            self.on_generic[event].append(handler)
            return handler
        return wrapper

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
                handlers = self.on_keydown.get(event.key, False)
                if handlers:
                    map(lambda handler: handler(context), handlers)

            # generic events
            handlers = self.on_generic.get(event.type, False)
            if handlers:
                map(lambda handler: handler(context), handlers)
