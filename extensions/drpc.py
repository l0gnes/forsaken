import pygame
from pypresence import Presence
import enums
import datetime

__author__ = "Alexander Lohnes"
__verison__ = "*" # Setting this value to '*' makes the extension compatible with all versions

class DiscordRichPresence():
    def __init__(self, game):
        self.GAME= game
        self.__CHANNEL = 0

        # Set a date in the past
        self.LAST_CHANGED = 0

        self.UPDATE_EVERY = datetime.timedelta(
            seconds = 120 # Every 2 Minutes
        ).total_seconds() * 500 # Grabs the milliseconds

        self.PYGAME_EVENT = pygame.event.Event(
            pygame.USEREVENT, Channel=self.CHANNEL
        )

        self.PYPRESENCE_CLIENT_ID = 790056166684229692 # Change this to whatever, it doesn't really matter
        self.RPC = Presence(self.PYPRESENCE_CLIENT_ID)
        self.RPC.connect() # Connects to discord

    @property
    def CHANNEL(self):
        return self.__CHANNEL

    @CHANNEL.setter
    def CHANNEL(self, value):
        self.__CHANNEL = value

    def register_channel(self, eventno : int):
        print("Registering Channels...")
        pygame.time.set_timer(eventno, 500)
        self.CHANNEL = eventno
        print("Channel is set to `%s`" % self.CHANNEL)
        return eventno, self

    def get_state_text(self):
        if self.GAME.GAMESTATE == enums.GameState.playing:
            return "Currently Playing"
        elif self.GAME.GAMESTATE == enums.GameState.paused:
            return "Paused"
        elif self.GAME.GAMESTATE == enums.GameState.menu_screen:
            return "In Menus"

    def event_hook(self, event):
        self.update_presence()


    def update_presence(self):
        current_time = self.GAME.Ticker._clock.get_time()
            
        if self.LAST_CHANGED + self.UPDATE_EVERY < pygame.time.get_ticks() or self.LAST_CHANGED == 0:
            print(f'updating {self.LAST_CHANGED + self.UPDATE_EVERY} < {pygame.time.get_ticks()}')
            # Since the game currently only supports gamestates, i'm going off of that.
            self.RPC.update(
                large_image = "logo-holo",
                #details = __verison__,
                state = self.get_state_text()
            )
            self.LAST_CHANGED = current_time

def enable_extension(game):
    return game.load_extension(
        DiscordRichPresence(
            game
        )
    )