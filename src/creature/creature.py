import random
from typing import Dict

import setting

from engine.lib.tilePos import Direction
from engine.lib.vect import Vec2i, Vec2f
from engine.lib.tilePos import TilePos, Direction, DIR_LOC

from engine.sufaceItem import SurfaceItem
from module.map_element import MapElement
from module.map_terrain import Terrain
from module.map import Map
from creature.kind import Kind

MOVING_SPEED = 0.1


class Creature(MapElement):
    NAME = "Creature"
    kind: Kind
    mapClass: Map

    maxHP: int
    hp: int
    atk: int
    defence: int

    isMoving: bool
    movingVect: Vec2f
    movingDes: TilePos
    movingCount: float

    def __init__(self, name: str, sprite: SurfaceItem, mapClass: Map):
        super().__init__(name, sprite)
        self.mapClass = mapClass
        self.kind = Kind.Unknow

        self.isMoving = False
        self.movingVect = Vec2f()
        self.movingDes = TilePos()
        self.movingCount = 0

    def __str__(self) -> str:
        return f'[Creature] {self.name}'

    def set_hp(self, hp: int):
        self.maxHP = hp
        self.hp = hp

    def attacked(self, atk: int):
        # TODO Atteacked
        pass

    def move_to(self, v: TilePos):
        self.pos = v
        self.set_absolute_position()
        self.sprite.position = Vec2f(self.pos.x, self.pos.y) \
            * setting.TILE_PIXEL * setting.ZOOM

    def move(self, d: Direction):
        self.move_to(self.pos.direct(d))

    def set_moving(self, movingVect: Vec2f, des: TilePos):
        self.movingVect = movingVect * MOVING_SPEED
        self.movingDes = des
        self.isMoving = True

    def moving(self, delta: int):
        if not self.isMoving:
            return
        mv = self.movingVect * delta
        self.aPos += mv
        self.sprite.position += mv

    def reached(self):
        if not self.isMoving:
            return
        self.isMoving = False
        self.move_to(self.movingDes)

    def check_move(self, d: Direction) -> bool:
        newLoc = self.pos.direct(d)
        if self.mapClass.terrain.get_v(newLoc) == Terrain.WALL:
            return False
        if self.mapClass.creatureMap.get_v(newLoc) != Kind.Nothing:
            return False
        return True

    def random_move(self):
        d = random.randint(0, 3)
        if not self.check_move(d):
            return
        movingVect = Vec2f.from_tuple(DIR_LOC[d])
        movingDes = self.pos.direct(d)
        self.mapClass.creatureMap.set_grid_v(self.pos, 0)
        self.mapClass.creatureMap.set_grid_v(movingDes, self.kind)

        self.set_moving(movingVect, movingDes)


class CreatureGroup:
    creatures: Dict[str, Creature]

    def __init__(self):
        self.creatures = {}

    def add(self, c: Creature):
        self.creatures[c.name] = c

    def random_move(self):
        for c in self.creatures.values():
            c.random_move()

    def moving(self, delta: int):
        for c in self.creatures.values():
            c.moving(delta)

    def reached(self):
        for c in self.creatures.values():
            c.reached()

    def get_by_pos(self, pos: TilePos) -> Creature:
        for e in self.creatures.values():
            if e.pos == pos:
                return e
        return None
