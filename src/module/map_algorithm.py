from engine.lib.grid import GridInt
from engine.lib.vect import Vec2i
from engine.lib.tilePos import TilePos, DIR_LOC


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


def aStar(terrain: GridInt, wall: int, start: TilePos, target: TilePos) -> list[TilePos]:
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

            if terrain.get(ds.x, ds.y) != wall and nodeGrid.get(ds).opened:
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


def bfsArea(terrain: GridInt, wall: int, pos: TilePos, limit: int = -1) -> list[TilePos]:
    '''Faster algorithm for check connection and size'''
    if terrain.get_v(pos) == wall:
        return []

    limited = True
    if limit == -1:
        limited = False

    checkGrid = GridInt(terrain.size().x, terrain.size().y)
    checkList: list[TilePos] = []
    vlist: list[TilePos] = []

    checkGrid.set_grid_v(pos, 1)
    checkList.append(pos)

    while len(checkList) > 0:
        q = checkList.pop(0)
        vlist.append(q)

        for d in DIR_LOC.values():
            ds = TilePos(q.x + d[0], q.y + d[1])
            if ds.x < 0 or ds.y < 0 or ds.x >= terrain.size().x or ds.y >= terrain.size().y:
                continue
            if checkGrid.get_v(ds) == 1:
                continue
            if limited and pos.distence(ds) > limit:
                continue
            if terrain.get_v(ds) == wall:
                continue
            checkList.append(ds)
            checkGrid.set_grid_v(ds, 1)

    return vlist


def bfsPath(terrain: GridInt, wall: int, pos: TilePos, limit: int = -1) -> list[TilePos]:
    '''for generate a list of location that in a given distance from a position'''
    if terrain.get_v(pos) == wall:
        return []

    limited = True
    if limit == -1:
        limited = False

    checkGrid = GridInt(terrain.size().x, terrain.size().y)
    checkList: list[Node] = []
    vlist: list[TilePos] = []

    startNode = Node()
    startNode.setLocs(pos, pos)
    startNode.setGH(0, 0)
    checkGrid.set_grid_v(pos, 1)
    checkList.append(startNode)

    while len(checkList) > 0:
        q = checkList.pop(0)
        vlist.append(q.loc.duplicate())
        g = q.g + 1

        for d in DIR_LOC.values():
            ds = TilePos(q.loc.x + d[0], q.loc.y + d[1])
            if ds.x < 0 or ds.y < 0 or ds.x >= terrain.size().x or ds.y >= terrain.size().y:
                continue
            if checkGrid.get_v(ds) == 1:
                continue
            if limited and g > limit:
                continue
            if terrain.get_v(ds) == wall:
                continue

            newNode = Node()
            newNode.setLocs(ds, q.loc.duplicate())
            newNode.setGH(g, 0)
            checkList.append(newNode)
            checkGrid.set_grid_v(ds, 1)

    return vlist
