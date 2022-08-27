import random
from enum import Enum, auto
from typing import Dict

import setting

from engine.lib.tilePos import Direction
from engine.lib.vect import Vec2i, Vec2f
from engine.lib.tilePos import TilePos, Direction, DIR_LOC

from engine.surfaceItem import SurfaceItem
from module.map_element import MapElement
from module.map_terrain import Terrain
from module.map import Map
from creature.kind import Kind

MOVING_SPEED = 0.1
ATTACK_SPEED = 0.1


class Behavior(Enum):
    IDLE = auto()
    MOVE = auto()
    ATTACK = auto()


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
        self.mapClass.creatureMap.set_grid_v(v, self.kind)

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

    def check_around(self) -> tuple[TilePos, list[TilePos]]:
        '''Return (player tilePos if player next to, list of available move tile)'''
        nextToPlayer: TilePos = None
        availableMove: list[TilePos] = []
        dirs: list[TilePos] = [self.pos.direct(d) for d in DIR_LOC]
        for dt in dirs:
            if self.mapClass.creatureMap.get_v(dt) == Kind.Player:
                nextToPlayer = dt
            if self.mapClass.terrain.get_v(dt) == Terrain.WALL:
                continue
            if self.mapClass.creatureMap.get_v(dt) != Kind.Nothing:
                continue
            availableMove.append(dt)
        return (nextToPlayer, availableMove)

    def ai(self):
        '''For overwrite'''
        pass

    def random_move(self):
        (_, availableMove) = self.check_around()
        if len(availableMove) == 0:
            return
        des = random.choice(availableMove)
        movingVect = Vec2f(des.x - self.pos.x, des.y - self.pos.y)
        movingDes = des
        self.mapClass.creatureMap.set_grid_v(self.pos, Kind.Nothing)
        self.mapClass.creatureMap.set_grid_v(movingDes, self.kind)

        self.set_moving(movingVect, movingDes)


class CreatureGroup:
    creatures: Dict[str, Creature]

    def __init__(self):
        self.creatures = {}

    def add(self, c: Creature):
        self.creatures[c.name] = c

    def ai(self):
        for c in self.creatures.values():
            c.ai()

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
