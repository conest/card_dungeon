import random
from enum import IntEnum

import pygame
from pygame import Rect
from engine.lib.grid import GridInt
from engine.lib.vect import Vec2i
from engine.tilemap import TileMap


class Terrain(IntEnum):
    WALL = 241


MAP_SIZE_X = 70
MAP_SIZE_Y = 70
TILE_PIXEL = 16


class Map:
    size: Vec2i
    tilemap: TileMap
    terrain: GridInt

    def __init__(self):
        self.size = Vec2i(MAP_SIZE_X, MAP_SIZE_Y)
        self.tilemap = TileMap(MAP_SIZE_X, MAP_SIZE_Y, TILE_PIXEL)
        self.terrain = GridInt(MAP_SIZE_X, MAP_SIZE_Y)

    def tilemap_load_resource(self, s: pygame.Surface, h: int, v: int):
        self.tilemap.load_sheet(s)
        self.tilemap.set_sheetHV(h, v)

    def sync_map(self):
        for i, t in enumerate(self.terrain.arr):
            if t == 1:
                self.tilemap.set_map_direct(i, Terrain.WALL)

    def draw_map(self):
        self.sync_map()
        self.tilemap.update_surface()

    def map_generate(self):
        self._gen_rooms()

    def _gen_rooms(self):
        ROOM_TRYING_NUM = 200
        ROOM_SIZE_MAX_X = 12
        ROOM_SIZE_MIN_X = 4
        ROOM_SIZE_MAX_Y = 10
        ROOM_SIZE_MIN_Y = 4

        self.terrain.reset(1)
        roomList = []
        # Gen rooms
        for _ in range(ROOM_TRYING_NUM):
            sx = random.randint(ROOM_SIZE_MIN_X, ROOM_SIZE_MAX_X + 1)
            sy = random.randint(ROOM_SIZE_MIN_Y, ROOM_SIZE_MAX_Y + 1)
            x = random.randint(0, MAP_SIZE_X - 1 - sx)
            y = random.randint(0, MAP_SIZE_Y - 1 - sy)
            newRoom = Rect(x, y, sx, sy)
            overlap = False
            for r in roomList:
                if newRoom.colliderect(r):
                    overlap = True
                    break
            if not overlap:
                roomList.append(newRoom)

        # Write rooms
        for r in roomList:
            for y in range(1, r.h):
                for x in range(1, r.w):
                    self.terrain.set_grid(x + r.x, y + r.y, 0)