import functools
import inspect

def FUNC_EVENT_CALLER(func):
    # This registers the event notifier
    def wrapper(f):
        @functools.wraps(f)
        def predicate(self, *args, **kwargs):
            self.game.EVENT_NOTIFIERS[f.__name__] = f

            if f.__name__ not in self.game.EVENT_LISTENERS:
                self.game.EVENT_LISTENERS[f.__name__] = ()

            for listener_function in self.game.EVENT_LISTENERS[f.__name__]:
                listener_function(self, *args, **kwargs)

            return f(self, *args, **kwargs)
        return predicate
    return wrapper

def FUNC_EVENT_LISTENER(listener_type : str):

    def wrapper(f):
        print(f.__class__)
        @functools.wraps(f)
        def event_listener_deco(self, *args, **kwargs):

            if listener_type not in self.game.EVENT_LISTENERS.keys():
                self.game.EVENT_LISTENERS[listener_type] = (f,) # We add this in there just incase the event hasnt happened yet
                return f(self, *args, **kwargs)

            self.game.EVENT_LISTENERS[listener_type].append(f) # Add func to the list of funcs to be called when the event occurs
            return f(self, *args, **kwargs)
        return event_listener_deco
    return wrapper