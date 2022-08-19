# import setting
from engine.lib.tilePos import Direction
# from engine.lib.vect import Vec2i, Vec2f
from engine.sufaceItem import SurfaceItem
from module.map_element import MapElement
from module.map_terrain import Terrain
from module.map import Map


class Creature(MapElement):
    NAME = "Creature"

    mapClass: Map

    maxHP: int
    hp: int
    atk: int
    defence: int

    def __init__(self, name: str, sprite: SurfaceItem):
        super().__init__(name, sprite)

    def __str__(self) -> str:
        return f'[Creature] {self.name}'

    def check_move(self, d: Direction) -> bool:
        newLoc = self.pos.direct(d)
        if self.mapClass.terrain.get_v(newLoc) == Terrain.WALL:
            return False
        return True

    def set_hp(self, hp: int):
        self.maxHP = hp
        self.hp = hp

    def attacked(self, atk: int):
        # TODO
        pass
