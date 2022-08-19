import random

from pygame import Rect

import setting
from engine.lib.grid import GridInt
from engine.lib.vect import Vec2i
from engine.lib.tilePos import Direction, TilePos
from engine.resource import resource

from module.map_terrain import Terrain
from module.creature import Creature

from enemy.snake import Snake

MAP_SIZE_X = setting.MAP_SIZE_X
MAP_SIZE_Y = setting.MAP_SIZE_Y
TRYING_NUM = 100


def gen_enemies(terrain: GridInt, creatureMap: GridInt) -> list[Creature]:

    genNum = 30
    eList = []
    for _ in range(TRYING_NUM):
        sx = random.randint(1, MAP_SIZE_X - 2)
        sy = random.randint(1, MAP_SIZE_Y - 2)
        t = terrain.get(sx, sy)
        ct = creatureMap.get(sx, sy)
        if (t == Terrain.PATH or t == Terrain.ROOM) and ct == 0:
            name = Snake.NAME + resource.unique_num()
            enemy = Snake(name, "animalsheet")
            enemy.move_to(TilePos(sx, sy))
            eList.append(enemy)
            genNum -= 1
            if genNum == 0:
                return eList
