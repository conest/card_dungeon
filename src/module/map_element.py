from typing import Dict

import pygame
import setting
from engine.lib.tilePos import TilePos, Direction

from engine.lib.vect import Vec2i, Vec2f
from engine.sufaceItem import SurfaceItem
from engine.camera import Camera


MAP_SIZE_X = setting.MAP_SIZE_X
MAP_SIZE_Y = setting.MAP_SIZE_Y
TILE_PIXEL = setting.TILE_PIXEL

MOVING_SPEED = 0.1


class MapElement:
    name: str
    pos: TilePos
    aPos: Vec2f
    sprite: SurfaceItem
    inMist: bool

    movingVect: Vec2f
    movingDes: TilePos
    movingCount: float

    def __init__(self, name: str, sprite: SurfaceItem):
        self.name = name
        self.pos = TilePos()
        self.aPos = Vec2f()
        self.sprite = sprite
        self.sprite.name = name
        self.inMist = True

        self.movingVect = Vec2f()
        self.movingDes = TilePos()
        self.movingCount = 0

    def __str__(self) -> str:
        return f'[MapElement] {self.name}, loc: {self.loc}'

    def set_absolute_position(self):
        self.aPos = self.pos.to_Vec2f() * setting.TILE_PIXEL

    def centerAPos(self) -> Vec2f:
        halfTile = setting.TILE_PIXEL / 2
        return self.aPos + Vec2f(halfTile, halfTile)

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

    def moving(self, delta: int):
        mv = self.movingVect * delta
        self.aPos += mv
        self.sprite.position += mv

    def reached(self):
        self.move_to(self.movingDes)


class MapElementManage():
    NAME = "MapElementManage"
    size: Vec2i
    eDict: Dict[str, MapElement]
    camera: Camera

    def __init__(self, camera: Camera):
        super().__init__()
        self.name = MapElementManage.NAME
        self.size = Vec2i(MAP_SIZE_X, MAP_SIZE_Y)
        self.eDict = {}
        self.camera = camera

    def add(self, me: MapElement):
        self._check_name_unique(me.name)
        self.eDict[me.name] = me

    def delete(self, name: str) -> bool:
        '''Return False if nothing find in the list with the given name'''
        if name in self.eDict:
            del self.eDict[name]
            return True
        return False

    def _check_name_unique(self, name: str):
        assert(name not in self.eDict), \
            f'[ERROR] Find MapElement name duplicated: {name} in {self.name}'

    def checkCamera(self, name: str):
        element = self.eDict[name]
        element.sprite.position = (element.aPos - self.camera.cPositon) * setting.ZOOM
        spriteSize = (setting.TILE_PIXEL, setting.TILE_PIXEL)
        elementRect = pygame.Rect(element.aPos.to_tuple_int(), spriteSize)
        if self.camera.in_camera(elementRect):
            element.sprite.visible = True
        else:
            element.sprite.visible = False

    def checkAllCamera(self) -> bool:
        for name in self.eDict:
            self.checkCamera(name)
