import random
from pygame import Rect

import setting
from engine.lib.grid import GridInt
from engine.lib.vect import Vec2i

from module.map_generator import Terrain
from module import map_algorithm as algorithm


def random_avaliable_pos(terrain: GridInt, rect: Rect = None) -> Vec2i:
    TRY_TIMES = 100
    nopeTerrain = [
        Terrain.WALL,
        Terrain.DOOR,
        Terrain.FOYER,
    ]

    if rect is None:
        rect = Rect(0, 0, setting.MAP_SIZE_X - 1, setting.MAP_SIZE_Y - 1)

    count = TRY_TIMES
    while(count > 0):
        count -= 1
        rx = random.randint(rect.x, rect.x + rect.w)
        ry = random.randint(rect.y, rect.y + rect.h)

        nope = False
        for t in nopeTerrain:
            if terrain.get(rx, ry) == t:
                nope = True
                break
        if not nope:
            return Vec2i(rx, ry)
    print('[WARNING] failed gen pos at random_avaliable_pos')
    return None


def gen_start_and_stairs(terrain: GridInt, rooms: list[Rect]) -> tuple[Vec2i, Vec2i]:
    '''Return (start, stairs)'''
    pass


def classify_rooms(terrain: GridInt, rooms: list[Rect]) -> tuple[list, list]:
    '''Return (Bigest room chain, isolated rooms)'''
    checkMap: GridInt = GridInt.from_vect(terrain.size())
    groupedRooms: list[list] = []

    while (len(rooms) > 0):
        startPos = Vec2i.from_tuple(rooms[0].center)
        vList = algorithm.bfsArea(terrain, Terrain.WALL, startPos)
        for loc in vList:
            checkMap.set_grid_v(loc, 1)

        newGroup: list[Rect] = []

        for r in reversed(rooms):
            center = Vec2i.from_tuple(r.center)
            if checkMap.get_v(center) == 1:
                newGroup.append(r)
                rooms.remove(r)

        groupedRooms.append(newGroup)

    if len(groupedRooms) == 1:
        return (groupedRooms[0], [])

    groupedRooms.sort(key=lambda s: len(s), reverse=True)

    isolatedRoom: list[Rect] = []
    for i in range(1, len(groupedRooms)):
        for ii in range(len(groupedRooms[i])):
            isolatedRoom.append(groupedRooms[i][ii])
    return (groupedRooms[0], isolatedRoom)
