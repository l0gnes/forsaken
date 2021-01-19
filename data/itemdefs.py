#from inventory import ItemDefinition
from enums import itemType
from data import itemFuncs

class ItemDefinition(object):
    def __init__(self, *args, **kwargs):
        self.weight = kwargs.get("weight", 0)
        self.name = kwargs.get("name", "An unknown item")
        self.description = kwargs.get('description', "Its use is indiscribable")
        self.type = itemType.unknown
        self.FUNCTION = None
        self.subclass = None

        if self.subclass is not None:
            self.subclass.__init__()

itemlist = [
    ItemDefinition(
        name = "Minor Health Potion",
        weight = 0.5,
        description = "Heals a small amount of HP",
        type = itemType.consumable,
        subclass = itemFuncs.HealingConsumable(10)
    ),
    ItemDefinition(
        name = "Health Potion",
        weight = 0.75,
        description = "Heals a moderate amount of HP",
        type = itemType.consumable,
        subclass = itemFuncs.HealingConsumable(20)
    ),
    ItemDefinition(
        name = "Major Health Potion",
        weight = 1,
        description = "Heals a huge amount of HP",
        type = itemType.consumable,
        subclass = itemFuncs.HealingConsumable(40)
    )
]
