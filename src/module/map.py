from enum import IntEnum

import pygame
from engine.lib.grid import GridInt
from engine.lib.vect import Vec2i
from engine.tilemap import TileMap
from engine.sufaceItem import SurfaceItem
from module import map_generator as mg


class Sheet(IntEnum):
    WALL = 241


MAP_SIZE_X = mg.MAP_SIZE_X
MAP_SIZE_Y = mg.MAP_SIZE_Y
TILE_PIXEL = mg.TILE_PIXEL


class Map:
    size: Vec2i
    tilemap: TileMap
    terrain: GridInt

    debug_surface: SurfaceItem

    def __init__(self):
        self.size = Vec2i(MAP_SIZE_X, MAP_SIZE_Y)
        self.tilemap = TileMap(MAP_SIZE_X, MAP_SIZE_Y, TILE_PIXEL)
        self.terrain = GridInt(MAP_SIZE_X, MAP_SIZE_Y)
        self.rooms = []

        self.debug_surface = SurfaceItem()
        self.debug_surface.new(MAP_SIZE_X * TILE_PIXEL, MAP_SIZE_Y * TILE_PIXEL)

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
        self.terrain = mg.generator(self.debug_surface.surface)
