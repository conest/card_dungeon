from engine.lib.grid import GridInt
from engine.lib.vect import Vec2i
from engine.lib.tilePos import TilePos, DIR_LOC
from .map_generator import Terrain


class Node:
    opened: bool
    loc: TilePos
    parent: TilePos
    g: int
    h: int
    f: int

    def __init__(self):
        self.opened = True
        self.loc = TilePos()
        self.parent = TilePos()
        self.setGH(0, 0)

    def setLocs(self, loc: TilePos, parent: TilePos):
        self.loc = loc
        self.parent = parent
        self.opened = False

    def setGH(self, g: int, h: int):
        self.g = g
        self.h = h
        self.f = g + h


class NodeGrid:
    grid: list[Node]
    _size: Vec2i

    def __init__(self, size: Vec2i):
        self._size = size
        self.grid = []
        for _ in range(size.volume()):
            self.grid.append(Node())

    def _idx(self, v: Vec2i) -> int:
        return self._size.x * v.y + v.x

    def get(self, v: Vec2i) -> Node:
        return self.grid[self._idx(v)]

    def set_grid(self, v: Vec2i, n: Node):
        self.grid[self._idx(v)] = n


def _find_least_f_node(nodeList: list[Node]) -> Node:
    isf = 0
    for i, o in enumerate(nodeList):
        if o.f < nodeList[isf].f:
            isf = i
    return nodeList.pop(isf)


def _gen_path(nodeList: list[Node], nodeGrid: NodeGrid) -> list[TilePos]:
    path: list[TilePos] = []
    lastNode = nodeList[-1]
    path.append(lastNode.loc.duplicate())
    while lastNode.loc != lastNode.parent:
        lastPos = lastNode.parent
        lastNode = nodeGrid.get(lastPos)
        path.append(lastNode.loc.duplicate())
    return path


def aStar(terrain: GridInt, start: TilePos, target: TilePos) -> list[TilePos]:
    if start == target:
        return []

    nodeGrid = NodeGrid(terrain.size())
    nodeList: list[Node] = []

    startNode = Node()
    startNode.setLocs(start, start)
    startNode.setGH(0, start.distence(target))
    nodeGrid.set_grid(start, startNode)
    nodeList.append(startNode)

    while len(nodeList) > 0:
        q = _find_least_f_node(nodeList)

        # gen successors
        successors: list[Node] = []
        for d in DIR_LOC.values():
            ds = TilePos(q.loc.x + d[0], q.loc.y + d[1])

            if terrain.get(ds.x, ds.y) != Terrain.WALL and nodeGrid.get(ds).opened:
                newNode = Node()
                newNode.setLocs(ds, q.loc.duplicate())
                newNode.setGH(q.g + 1, ds.distence(target))
                successors.append(newNode)
                nodeGrid.set_grid(ds, newNode)

        if len(successors) == 0:
            continue
        # check if reach the target
        for s in successors:
            nodeList.append(s)
            if s.loc == target:
                return _gen_path(nodeList, nodeGrid)

    return []
