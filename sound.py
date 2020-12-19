import pygame
import glob
import os

class SoundHandler(object):
    def __init__(self, game, *args, **kwargs):
        self.game = game
        self.make_sure_init()

        pygame.mixer.set_num_channels(
            4 # Number of Channels (Overlapping Audio)
        )

        self.SOUNDS = {}
        self.load_sounds()

    def make_sure_init(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

    def load_sounds(self):
        files = glob.glob(
            "./assets/wav/*.wav",
            recursive=True
        )
        for i in files:
            refname = os.path.splitext(os.path.split(i)[1])[0]
            self.SOUNDS[refname] = pygame.mixer.Sound(file=i)
            print(refname, ".wav loaded!")



    def attempt_play(self, soundref, *args, **kwargs):
        pygame.mixer.find_channel().play(self.SOUNDS[soundref], *args, **kwargs)

        


    