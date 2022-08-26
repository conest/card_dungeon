from typing import Dict

import pygame
import setting
from engine.lib.tilePos import TilePos
from engine.lib.vect import Vec2i, Vec2f
from engine.object import Object
from engine.surfaceItem import SurfaceItem
from engine.camera import Camera


MAP_SIZE_X = setting.MAP_SIZE_X
MAP_SIZE_Y = setting.MAP_SIZE_Y
TILE_PIXEL = setting.TILE_PIXEL


class MapElement(Object):
    pos: TilePos
    aPos: Vec2f
    sprite: SurfaceItem
    inMist: bool

    def __init__(self, name: str, sprite: SurfaceItem):
        super().__init__()
        self.name = name
        self.pos = TilePos()
        self.aPos = Vec2f()
        self.sprite = sprite
        self.sprite.name = name
        self.inMist = True

    def __str__(self) -> str:
        return f'[MapElement] {self.name}, loc: {self.loc}'

    def set_absolute_position(self):
        self.aPos = self.pos.to_Vec2f() * setting.TILE_PIXEL

    def centerAPos(self) -> Vec2f:
        halfTile = setting.TILE_PIXEL / 2
        return self.aPos + Vec2f(halfTile, halfTile)


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
