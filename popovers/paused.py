from popovers import PopoverWindow

class PausedPopover(PopoverWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        