import pygame
from pypresence import Presence
import enums

class DiscordRichPresence():
    def __init__(self, game):
        self.GAME= game
        self.CHANNEL = 0

        self.PYPRESENCE_CLIENT_ID = 0 # Change this to whatever, it doesn't really matter
        self.RPC = Presence(self.PYPRESENCE_CLIENT_ID)
        self.RPC.connect() # Connects to discord

    def register_channel(self):
        pass

    def update_presence(self):

