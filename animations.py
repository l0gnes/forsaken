import pygame
import datetime

class AnimationWrapper(object):
    def __init__(self, func, run_once : bool = False):
        self.func = func
        self.run_once = run_once

class AnimationHandler(object):
    def __init__(self, game, *args, **kwargs):
        self.GAME = game

        self.animation_cache = []

    def add_animation(self, function, run_once : bool = False):
        self.animation_cache.append(
            AnimationWrapper(
                function, run_once
            )
        )

    def do_animations(self):
        for i in self.animation_cache:
            i.func()

            if i.run_once:
                self.animation_cache.remove(i)
        