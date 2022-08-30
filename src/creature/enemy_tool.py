import random

import setting
from engine.lib.grid import GridInt
from engine.lib.vect import Vec2i
from engine.lib.tilePos import Direction, TilePos
from engine.resource import resource

from module.map_terrain import Terrain
from creature.creature import Creature
from module.map import Map
from creature.snake import Snake
from creature.kind import Kind

MAP_SIZE_X = setting.MAP_SIZE_X
MAP_SIZE_Y = setting.MAP_SIZE_Y
TRYING_NUM = 100


def gen_enemies(m: Map) -> list[Creature]:

    genNum = 30
    eList = []
    for _ in range(TRYING_NUM):
        sx = random.randint(1, MAP_SIZE_X - 2)
        sy = random.randint(1, MAP_SIZE_Y - 2)
        t = m.terrain.get(sx, sy)
        ct = m.creatureMap.get(sx, sy)

        if (t == Terrain.PATH or t == Terrain.ROOM) and ct == Kind.Nothing:
            name = Snake.NAME + resource.unique_num()
            enemy = Snake(name, "animalsheet", m)

            enemy.move_to(TilePos(sx, sy))
            m.creatureMap.set_grid(sx, sy, enemy.kind)
            eList.append(enemy)
            genNum -= 1
            if genNum == 0:
                return eList
    return eList
