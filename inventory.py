import pygame
import enums
import itemdefs

class ItemDefinition(object):
    def __init__(self, *args, **kwargs):
        pass

class ItemObject(object):
    def __init__(self, id : int, itemDef):
        self.id = id

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

    def add_item(self, item : ItemObject, count : int):
        if count == 0:
            return # No items are added (duh)

        if count < 0:
            # This function handles garbage, so we'll redirect it there
            return self.remove_item(item, count * -1)

        if item not in self._storage:
            self._storage[item] = count
        else:
            precount = self._storage[item]
            count = precount + count
            self._storage[item] = count
        return count

    def remove_item(self, item : ItemObject, count : int):
        raise NotImplemented
