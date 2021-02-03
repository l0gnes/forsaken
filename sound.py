import pygame
import glob
import os
import deco

from enums import GameState

class SoundHandler(object):

    def __init__(self, sgame, *args, **kwargs):
        self.game = sgame
        game = sgame
        self.make_sure_init()

        pygame.mixer.set_num_channels(
            6 # Number of Channels (Overlapping Audio)
        )
        self.MUSIC_CHANNEL = pygame.mixer.find_channel() # Reserved music channel
        self.MUSIC_SOSS = False # Stop on Scene Switch setting

        self.SOUNDS = {}
        self.load_sounds()
        self.load_music()

        # These will obviously need a menu in the future.
        self.MUSIC_MUTED = False
        self.SOUNDS_MUTED = False
        self.BASE_SOUNDS_VOLUME = 100
        self.BASE_MUSIC_VOLUME = 100
        self.MASTER_VOLUME = 25 # The volume of the whole game

        self.game.addEventListener("setGamestate", self.play_menu_stuff)

    @property
    def MUSIC_VOLUME(self):
        return float(self.BASE_MUSIC_VOLUME / 100) * self.MASTER_VOLUME_INFLUENCE

    @property
    def SOUNDS_VOLUME(self):
        return float(self.BASE_SOUNDS_VOLUME / 100) * self.MASTER_VOLUME_INFLUENCE

    @property
    def MASTER_VOLUME_INFLUENCE(self):
        return self.MASTER_VOLUME / 100

    def refresh_channel_volumes(self):
        print('SETTING MUSIC VOLUME TO `%s`' % self.MUSIC_VOLUME)
        self.MUSIC_CHANNEL.set_volume(self.MUSIC_VOLUME)

    def make_sure_init(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

    def load_sounds(self):
        self.game.LOGGING.info("Loading Sounds...")

        files = glob.glob(
            "./assets/wav/*.wav",
            recursive=True
        )
        for i in files:
            refname = os.path.splitext(os.path.split(i)[1])[0]
            self.SOUNDS[refname] = pygame.mixer.Sound(file=i)

            self.game.LOGGING.debug("Sound %s Loaded!" % refname)

    def load_music(self):
        self.game.LOGGING.info("Loading Music...")

        files = glob.glob(
            "./assets/wav/music/*.wav",
            recursive=True
        )

        for i in files:
            refname = os.path.splitext(os.path.split(i)[1])[0]
            self.SOUNDS[refname] = pygame.mixer.Sound(file=i)
            self.game.LOGGING.debug("Music File %s Loaded!" % refname)

    @deco.FUNC_EVENT_CALLER('play_music')
    def play_music(self, soundref, loop : bool = True, stop_on_scene_switch : bool = True, *args, **kwargs):
        self.refresh_channel_volumes()
        self.game.LOGGING.debug("Attempting to play the song: %s" % soundref)
        self.MUSIC_SOSS = stop_on_scene_switch
        self.MUSIC_CHANNEL.play(
            self.SOUNDS[soundref],
            loops = -1 if loop else 0
        )

    @deco.FUNC_EVENT_LISTENER('setGamestate')
    def play_menu_stuff(self, gamestate, *args, **kwargs):
        if gamestate == GameState.menu_screen:
            if hasattr(self, "RUNNING"):
                self.SoundHandle.play_music('bouncy boi')
            else:
                self.play_music('bouncy boi')
        elif gamestate == GameState.playing:
            if hasattr(self, 'RUNNING'):
                self.SoundHandle.play_music('damp')
            else:
                self.play_music('damp')
    

    @deco.FUNC_EVENT_CALLER('attempt_play')
    def attempt_play(self, soundref, *args, **kwargs):
        self.game.LOGGING.debug("Attempting to play a sound \"%s\"" % soundref)
        c = pygame.mixer.find_channel()
        c.set_volume(self.SOUNDS_VOLUME)
        c.play(self.SOUNDS[soundref], *args, **kwargs)


        


    