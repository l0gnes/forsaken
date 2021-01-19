import pygame
import datetime
import uuid

class AnimationWrapper(object):
    def __init__(self, id : int, func, iterations : int = None):
        self.ID = id
        self.func = func

        # For animations which consist of calling a function multiple times
        self.times_to_iterate = iterations
        self.iterations_completed = 0

    @property
    def delete_me(self):
        return self.times_to_iterate == self.iterations_completed

class AnimationHandler(object):
    def __init__(self, game, *args, **kwargs):
        self.GAME = game

        self.animated_last = {}
        self.animation_cache = {}

    def current_time(self):
        return (datetime.datetime.utcnow() - datetime.datetime(month=6, day=9, year=2020)).total_seconds()

    def add_animation(self, function, s : int, iterations : int = None):
        animid = uuid.uuid1().hex # This magical function will never generate the same string of characters :)
        self.animation_cache[AnimationWrapper(animid, function, iterations)] = s
        self.animated_last[animid] = 0 # So we don't get a terrible undefined key error anywheres

    def do_animations(self):
        for a in self.animation_cache:

            if self.current_time > self.animated_last[a.ID] + self.animation_cache[a.ID]:
                a.func() # Call the animation function
                a.iterations_completed += 1

                # Deletes the animations that aren't going to run anymore
                if a.delete_me:
                    del self.animation_cache[a]
                    del self.animated_last[a.id]
                    del a
