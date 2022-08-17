from enum import IntEnum

import pygame
import setting
from engine.lib.grid import GridInt
from engine.lib.vect import Vec2i
from engine.tilemap import TileMap
from engine.sufaceItem import SurfaceItem
from module import map_generator as mg
from module import map_tool as tool


class Sheet(IntEnum):
    WALL = 241


MAP_SIZE_X = setting.MAP_SIZE_X
MAP_SIZE_Y = setting.MAP_SIZE_Y
TILE_PIXEL = setting.TILE_PIXEL


class Map:
    NAME = "map"
    size: Vec2i
    tilemap: TileMap
    terrain: GridInt
    rooms: list[pygame.Rect]
    mainRooms: list[pygame.Rect]
    isolatedRooms: list[pygame.Rect]

    debug_surface: SurfaceItem

    def __init__(self):
        self.size = Vec2i(MAP_SIZE_X, MAP_SIZE_Y)
        self.tilemap = TileMap(MAP_SIZE_X, MAP_SIZE_Y, TILE_PIXEL)
        self.terrain = GridInt(MAP_SIZE_X, MAP_SIZE_Y)
        self.rooms = []

        self.debug_surface = SurfaceItem()
        self.debug_surface.new(MAP_SIZE_X * TILE_PIXEL, MAP_SIZE_Y * TILE_PIXEL)

    def si(self) -> SurfaceItem:
        return self.tilemap

    def tilemap_load_resource(self, s: pygame.Surface, h: int, v: int):
        self.tilemap.load_sheet(s)
        self.tilemap.set_sheetHV(h, v)

    def sync_map(self):
        for i, t in enumerate(self.terrain.arr):
            if t == mg.Terrain.WALL:
                self.tilemap.set_map_direct(i, Sheet.WALL)

    def draw_map(self):
        self.sync_map()
        self.tilemap.update_surface()

    def map_generate(self):
        (self.terrain, self.rooms) = mg.generator(self.debug_surface.surface)
        self._classify_rooms()

    def _classify_rooms(self):
        (self.mainRooms, self.isolatedRooms) = tool.classify_rooms(self.terrain, self.rooms)
