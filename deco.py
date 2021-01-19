import functools
import inspect

def FUNC_EVENT_CALLER(func):
    # This registers the event notifier
    def wrapper(f):
        @functools.wraps(f)
        def predicate(self, *args, **kwargs):
            print(f'maybe {f.__name__}')

            if hasattr(self, 'game'):

                if f.__name__ not in self.game.EVENT_LISTENERS:
                    self.game.EVENT_LISTENERS[f.__name__] = ()

                for listener_function in self.game.EVENT_LISTENERS[f.__name__]:
                    print('trying to do functin..')
                    listener_function(self, *args, **kwargs)

            elif hasattr(self, 'GAMESTATE') and hasattr(self, "RUNNING"):

                if f.__name__ not in self.EVENT_LISTENERS:
                    self.EVENT_LISTENERS[f.__name__] = ()

                for listener_function in self.EVENT_LISTENERS[f.__name__]:
                    listener_function(self, *args, **kwargs) 

            return f(self, *args, **kwargs)
        return predicate
    return wrapper

def FUNC_EVENT_LISTENER(listener_type : str):

    def wrapper(f):
        print(f, listener_type, sep='\t')
        
        @functools.wraps(f)
        def event_listener_deco(self, *args, **kwargs):
            print(f)

            if listener_type not in self.game.EVENT_LISTENERS.keys():
                print(f"Adding {listener_type} listener_type")
                self.game.EVENT_LISTENERS[listener_type] = (f,) # We add this in there just incase the event hasnt happened yet
                return f(self, *args, **kwargs)

            self.game.EVENT_LISTENERS[listener_type].append(f) # Add func to the list of funcs to be called when the event occurs
            return f(self, *args, **kwargs)
        return event_listener_deco
    return wrapper