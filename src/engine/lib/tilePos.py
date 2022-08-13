from __future__ import annotations

from enum import IntEnum
from .vect import Vec2i


class Direction(IntEnum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Direction8(IntEnum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    UP_RIGHT = 5
    DOWN_RIGHT = 6
    UP_LEFT = 7
    DOWN_LEFT = 8


DIR_LOC = {
    Direction.UP: (0, -1),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
}


LOC_DIR = {
    (0, -1): Direction.UP,
    (0, 1): Direction.DOWN,
    (-1, 0): Direction.LEFT,
    (1, 0): Direction.RIGHT,
}


def opposite_direction(d: Direction) -> Direction:
    match d:
        case Direction.UP:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.UP
        case Direction.LEFT:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.LEFT


class TilePos(Vec2i):

    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__(x, y)

    def __str__(self) -> str:
        return f'[TilePos] (x: {self.x}, y: {self.y})'

    def direct(self, d: Direction) -> TilePos:
        loc = DIR_LOC[d]
        return TilePos(self.x + loc[0], self.y + loc[1])

    def direction_from(self, toTile: TilePos) -> Direction:
        x = toTile.x - self.x
        y = toTile.y - self.y
        if (x, y) in LOC_DIR:
            return LOC_DIR[(x, y)]
        return None

    def toVect(self) -> Vec2i:
        return Vec2i(self.x, self.y)

    def fromVect(self, v: Vec2i):
        self.x = v.x
        self.y = v.y

    def duplicate(self) -> TilePos:
        return TilePos(self.x, self.y)
