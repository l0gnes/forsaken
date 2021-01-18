import pygame
import enums
import itemdefs

class playerEncumbered(Exception):
    pass

# Weight is measured in "lb"

class ItemDefinition(object):
    def __init__(self, *args, **kwargs):
        self.weight = kwargs.get("weight", 0)
        self.name = kwargs.get("name", "An unknown item")
        self.description = kwargs.get('description', "Its use is indiscribable")
        self.type = enum.itemType.unknown
        self.FUNCTION = None
        self.subclass = None

        if self.subclass is not None:
            self.subclass.__init__()

class ItemObject(object):
    def __init__(self, id : int, itemDef : ItemDefinition):
        self.id = id
        self.meta = itemDef
        #self.FUNCTION = self.meta.FUNCTION

    def use(self, player, *args, **kwargs):
        return self.meta.FUNCTION(player, *args, **kwargs)

class ItemFactory(object):
    def __init__(self, itemdefs):
        self.itemdefs = itemdefs
        self.item_object_cache = []
        #self._id_cache = 0

    def construct(self):

        for idef in self.itemdefs:
            self.item_object_cache.append(
                ItemObject.__init__(len(self.item_object_cache), idef)
            )

        return self.item_object_cache

class InventoryHandler(object):
    def __init__(self, player, *args, **kwargs):
        self.player = player
        self.item_factory = ItemFactory(itemdefs.itemlist).construct()

        self._storage = {}

    def fetch_storage_weight(self):
        tW = 0 # The total weight
        for item, count in self._storage.items():
            tW += item.weight * count
        return tW

    def add_item(self, item : ItemObject, count : int, *, pickup_until_encumbered : bool = False, pardon_weight : bool = False):
        remainder = 0 # The items leftover if pickup_until_encumbered = True
        if count == 0:
            return # No items are added (duh)

        if count < 0:
            # This function handles garbage, so we'll redirect it there
            return self.remove_item(item, count * -1)

        if not pickup_until_encumbered:
            if item.meta.weight * count > self.player.free_carry_weight:
                raise playerEncumbered()
        else:
            newCount = 0
            tmpWeight = 0
            while newCount * item.meta.weight < self.player.free_carry_weight:
                newCount += 1
            remainder = count - newCount
            count = newCount * item.meta.weight # Gives us the new item count

        if item not in self._storage:
            self._storage[item] = count
        else:
            precount = self._storage[item]
            count = precount + count
            self._storage[item] = count
        return count, remainder

    def remove_item(self, item : ItemObject, count : int):
        raise NotImplemented
