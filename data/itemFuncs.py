from inventory import ItemDefinition
from enums import itemType

class ItemFunction(object):
    pass

class HealingConsumable(ItemFunction):
    def __init__(self, health : int):
        self.health_to_heal = health

        self.FUNCTION = self.heal_player

    def heal_player(self, player, *args, **kwargs):
        return self.player.heal(self.health_to_heal)
