from inventory import ItemDefinition
from enums import itemType
from data import itemFuncs

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
