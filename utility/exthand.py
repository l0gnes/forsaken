# All new and improved extension handler
# Hopefully making modding easier user-end.

import pygame
import glob
import importlib
import os

class ExtensionNotLoaded(Exception):
    pass

class ExtensionHandler(object):
    def __init__(self, game, *args, **kwargs):
        self.GAME = game

        self.unloaded_extensions = self.GAME.SETTINGS.fetch('disabled-extensions')
        self.EXTENSIONS = {}

    def ensure_not_disabled(self, extension_name : str):
        return not extension_name in self.unloaded_extensions

    def fetch_extensions(self):
        for ext_path in glob.glob('./extensions/*.*', recursive=False):
            extname = os.path.splitext(os.path.split(ext_path)[1])[0]
            print("attempting to load extension: `extensions.%s`" % extname)
            ext_mod = importlib.import_module("extensions.%s" % extname, package='.')
            print(ext_mod)

            if not hasattr(ext_mod, 'enable_extension'):
                raise EnvironmentError('Mod %s has no `enable_extension` function' % ext_mod.__name__)

            if self.ensure_not_disabled(ext_mod.__name__.split('.')[1]):
                print("LOADING %s" % ext_mod.__name__)
                c, e = ext_mod.enable_extension(self)
            else:
                print("%s IS DISABLED!!" % ext_mod.__name__)
                break

            if c:
                self.EXTENSIONS[e.__class__.__name__] = e
                print(f"Extension: {ext_mod.__name__} (Author={ext_mod.__author__}) loaded successfully!")
            else:
                print("Failed to load extension: %s" % str(c))

    # Called if an extension actually sets up successfully
    def load_extension(self, extension):
        if hasattr(extension, 'register_channel'):
            channel = extension.register_channel(
                eventno = pygame.USEREVENT + len(self.EXTENSIONS) + 1
            )
        else:
            raise EnvironmentError('Mod %s has no `register_channel` function' % extension)
        return channel, extension

    def unload_extension(self, extension):

        if extension not in self.EXTENSIONS:
            raise ExtensionNotLoaded()

        eventid = self.EXTENSIONS[extension]
        pygame.time.set_timer(eventid, 0) # Removes the event id and stuff
        del self.EXTENSIONS[extension]

        


    def init(self):
        return self.fetch_extensions()