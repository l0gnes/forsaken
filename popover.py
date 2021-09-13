from pygame import Surface


class PopoverWindow(object):
    """
        Pop-overs are displayed on top of the game surface.

        This can include things like a persistent in-game gui, a pause screen,
        or an inventory menu.
    """

    identifier = None
    active = False # Whether or not the popover should be able to be interacted with

    def __init__(self, game, width : int, height : int, *args, **kwargs):
        self.game = game
        self.SURFACE = Surface((width, height))

    def create_default_popover(self):
        """
            Basically just ensures the popover's surface has something in it.
        """
        self.SURFACE.fill('purple')

    def draw_popover(self):
        """
        This is to be written over, this is what is called to draw the popover onto the screen.
        """
        raise NotImplementedError("No popover could be drawn.")

    def _event_hook_runner(self, event):
        """
            This is what the event handler will check to ensure that only active popovers
            run their event handlers. So that you dont click a button in a closed popover.
        """
        if self.active:
            return self.event_hook(event)

    def event_hook(self, event):
        """this window's event listener, this is also meant to be written over."""
        return

class PopoverHandler(object):
    """
        Handles pop-over storing, enabling, disabling and everything in between.
    """

    def __init__(self, game, *args, **kwargs):
        self.game = game

        self.popovers = {}

    def fetch_active_popovers(self):
        return list(
            filter(
                lambda popover: popover.active, self.popovers.values()
            )
        )

    def register_popover(self, popoverName : str, popover : PopoverWindow) -> None:
        """
            Registers a popover
        """
        
        if not hasattr(popover, "SURFACE"): # If the popover window has no surface (which shouldn't ever happen)
            raise TypeError("PopoverWindow has no attribute `SURFACE`.")

        elif popover.identifier: # If popover has a non-null identifier already
            raise TypeError("Popover is already identified")

        else:
            
            self.popovers[popoverName] = popover 
            popover.identifier = popoverName

        