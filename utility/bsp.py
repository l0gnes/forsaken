# Attempt No. 2 at BSP.
# I accidentally deleted the first one...

# All of the measurements are done for each plot point on the map, not pixel

import random
import enum

FORCE_MIN_SPLIT_SIZE = 3

class SplitDirection(enum.Enum):
    vertical = 0
    horizontal = 1

class boopLeaf(object):
    def __init__(self, x1 : int, y1 : int, x2 : int, y2 : int, *, parent = None, node = None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.node = node
        self.parent = parent
        self.direct_children = [] # direct children of this leaf

    @property
    def string_points(self):
        return f"<LeafCords({self.node}) ({self.x1},{self.y1}) -> ({self.x2},{self.y2})>"

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    def createChildren(self, seed : random.Random):
        """
            Creates child nodes from this parent node.

            :param seed: The pseudo-random generator.
            :type seed: random.Random
        """
        direction = seed.choice(list(SplitDirection.__members__.values()))
        split_point = 0

        if direction == SplitDirection.horizontal:
            split_point = seed.randint(3, self.height)

        elif direction == SplitDirection.vertical:
            split_point = seed.randint(3, self.width)

        # We create the nodes
        NODE_A = boopLeaf(
            self.x1, 
            self.y1, 
            self.x2 if direction == SplitDirection.vertical else split_point - 1,
            self.y2 if direction == SplitDirection.horizontal else split_point - 1,
            parent = self,
            node = "A"
            )

        NODE_B = boopLeaf(
            self.x1 if direction == SplitDirection.horizontal else (self.width - split_point - 1),
            self.y1 if direction == SplitDirection.vertical else (self.height - split_point - 1),
            self.x2,
            self.y2,
            parent = self,
            node = "B"   
        )

        self.direct_children.extend((NODE_A, NODE_B))
        return NODE_A, NODE_B

            


class boopTree(boopLeaf):
    def __init__(self, width : int, height : int, *, seed : int = None):
        
        super().__init__(
            0, 0, width, height
        )

        self.__random_seed = seed if seed is not None else random.randint(0, 65535)
        self.seed = random.Random(self.__random_seed)

        #self.width = width
        #self.height = height

    def fetchAllLeafsCount(self): # I don't care that it's an improper plural.
        nodes_to_iterate = [self,]
        children = 0
        
        while len(nodes_to_iterate) > 0:
            node = nodes_to_iterate[0]
            
            if len(node.direct_children) > 0: # If the node has direct children
                children += len(node.direct_children)
                nodes_to_iterate.extend(node.direct_children)
            
            nodes_to_iterate.pop(0)
        
        return children

    def fetchAllLeafs(self): # I don't care that it's an improper plural.
        nodes_to_iterate = [self,]
        rooms = []
        
        while len(nodes_to_iterate) > 0:
            node = nodes_to_iterate[0]
            
            rooms.append(node)
            if len(node.direct_children) > 0: # If the node has direct children
                nodes_to_iterate.extend(node.direct_children)
            
            nodes_to_iterate.pop(0)
        
        return rooms

    def createChildrenIteration(self, iterations : int):
        #node_a, node_b self.createChildren(seed)
        nodes_to_iterate = [self,]

        for i in range(iterations):
            #print(f"DOING ITERATION {i+1} ({2 ** i} ROOMS)")
            for x in range(len(nodes_to_iterate)):
                node = nodes_to_iterate.pop(0)
                new_nodes = node.createChildren(self.seed)
                nodes_to_iterate.extend(new_nodes)


if __name__ == "__main__":
    failures = 0
    for i in range(1000):
        #try:
        t = boopTree(256, 256, seed=i)
        t.createChildrenIteration(2)
        print(len(t.fetchAllLeafs()))
        #except:
        #    failures += 1
    print(f"Failures: {failures} ({(failures/1000) * 100}%)")
    input()
    

    


