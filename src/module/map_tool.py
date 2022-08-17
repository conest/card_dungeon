import random
from pygame import Rect

import setting
from engine.lib.grid import GridInt
from engine.lib.vect import Vec2i

from module.map_generator import Terrain
from module import map_algorithm as algorithm


def random_avaliable_pos(terrain: GridInt, rect: Rect = None, okTerrain: list[Terrain] = None) -> Vec2i:
    TRY_TIMES = 100

    if okTerrain is None:
        okTerrain = [
            Terrain.EMPTY,
            Terrain.PATH,
            Terrain.ROOM,
        ]

    if rect is None:
        rect = Rect(0, 0, setting.MAP_SIZE_X - 1, setting.MAP_SIZE_Y - 1)

    for _ in range(TRY_TIMES):
        rx = random.randint(rect.x, rect.x + rect.w)
        ry = random.randint(rect.y, rect.y + rect.h)
        for t in okTerrain:
            if terrain.get(rx, ry) == t:
                return Vec2i(rx, ry)

    print('[WARNING] failed gen pos at random_avaliable_pos')
    return None


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


def player_and_stairs_pos(terrain: GridInt, rooms: list[Rect]) -> tuple[Vec2i, Vec2i]:
    '''Return (start, stairs)'''
    [pRoom, sRoom] = random.choices(rooms, k=2)
    vPlayer = random_avaliable_pos(terrain, rect=pRoom)
    vStairs = random_avaliable_pos(terrain, rect=sRoom)
    terrain.set_grid_v(vPlayer, Terrain.PLAYER)
    terrain.set_grid_v(vStairs, Terrain.STAIRS)

    return (vPlayer, vStairs)
