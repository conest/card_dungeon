from enum import IntEnum


class Terrain(IntEnum):
    EMPTY = 0
    PATH = 1
    ROOM = 2
    DOOR = 11
    FOYER = 12

    WALL = 21
    STAIRS = 30
    BORDER = 99

    PLAYER = 100
    ENEMY = 101
