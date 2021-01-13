import pygame
import game
import deco

class MainMenuSurface(object):
    def __init__(self, game, *args, **kwargs):
        self.game = game # reference to game object
        
        self.surface = pygame.Surface(
            size = self.game.screen.get_size()
        )

        self.POINTER_INDEX = 0 # We're going to use this for our menu control
        self.LIST_MENU_OPTIONS = {
            "New Game" : self.game.start_new_game,
            'Load Game' : self.load_game_screen,
            "Settings" : self.load_settings_manager,
            "Exit" : pygame.quit
        }
        self.LIST_MENU_POINT_POSITIONS = {
            # ID : Height
        }

        self.SECRET_PHRASE = []

        self.logo = pygame.image.load(
            './assets/logo.png'
        ).convert()

        self.game.SoundHandle.play_music('bouncy boi', loop=True)

    def event_hook(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.POINTER_INDEX += 1 if self.POINTER_INDEX+1 < len(self.LIST_MENU_OPTIONS) else 0
                self.game.SoundHandle.attempt_play('menuswitch')
            elif event.key == pygame.K_UP:
                self.POINTER_INDEX -= 1 if self.POINTER_INDEX > 0 else 0
                self.game.SoundHandle.attempt_play('menuswitch')
            elif event.key == pygame.K_RETURN:
                # TODO: Make the text in the menu flash or something i don't know
                self.game.SoundHandle.attempt_play('menuselectdrastic')
                
                self.game.WindowHandle.do_with_fade(
                    list(self.LIST_MENU_OPTIONS.values())[self.POINTER_INDEX]
                )

            self.SECRET_PHRASE.append(pygame.key.name(event.key))

            if len(self.SECRET_PHRASE) > 3:
                self.SECRET_PHRASE.pop(0)

            if self.SECRET_PHRASE == list('pog'):
                self.logo = pygame.image.load(
                    './assets/pog.jpg'
                ).convert()
                self.logo = pygame.transform.scale(
                    self.logo, (100, 100)
                )


    @deco.FUNC_EVENT_LISTENER('music_play')
    def music_was_played_wow(self):
        print('WOWIE')

    def load_game_screen(self):
        print("not implemented yet again")

    def load_settings_manager(self):
        print("no implemented settings")

    def get_surface_menu_list(self):
        text_labels = []
        for index, o in enumerate(self.LIST_MENU_OPTIONS.keys()):
            sur = self.game.LARGE_FONT.render(
                o, # Text,
                True, # Antialias
                "black", # Color of text
                'white' if self.POINTER_INDEX != index else 'grey'
            )
            text_labels.append(sur)

        longest_width = 0
        tallest_height = 0
        for label in text_labels:
            if label.get_width() > longest_width:
                longest_width = label.get_width()

            if label.get_height() > tallest_height:
                tallest_height = label.get_height()

        total_height = tallest_height * len(text_labels) + (8 * len(text_labels))
        total_width = longest_width + 8

        menu_surface = pygame.Surface(
            (
                total_width,
                total_height
            )
        )

        menu_surface.fill('white')
        for index, o in enumerate(text_labels, start=0):
            h = index * tallest_height + 8
            self.LIST_MENU_POINT_POSITIONS[index] = h
            menu_surface.blit(
                o,
                (4, h)
            )

        return menu_surface

    def draw_surface(self):
        self.surface.fill(
            'white'
        )
        self.surface.blit(
            self.logo,
            (
                (self.surface.get_width() - self.logo.get_width()) / 2,
                (self.surface.get_height() - self.logo.get_height()) / 10
            )
        )

        sml = self.get_surface_menu_list()
        self.surface.blit(
            sml,
            (
                (self.surface.get_width() - sml.get_width()) / 2,
                (self.surface.get_height() - sml.get_height()) / 2
            )
        )

        self.game.screen.blit(self.surface, (0, 0))

