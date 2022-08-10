import random
import pygame
from pygame import Rect
from engine.lib.grid import GridInt
from engine.lib.vect import Vec2i
from engine.lib.tilePos import Direction, TilePos

MAP_SIZE_X = 50
MAP_SIZE_Y = 50
TILE_PIXEL = 16


def generator(debug_surface: pygame.Surface) -> GridInt:

    terrain = GridInt(MAP_SIZE_X, MAP_SIZE_Y)
    rooms = []
    markMap = GridInt(MAP_SIZE_X, MAP_SIZE_Y)

    def gen_rooms():
        ROOM_TRYING_NUM = 200
        ROOM_SIZE_MAX_X = 10
        ROOM_SIZE_MIN_X = 4
        ROOM_SIZE_MAX_Y = 8
        ROOM_SIZE_MIN_Y = 4

        terrain.reset(1)
        # Gen rooms
        for _ in range(ROOM_TRYING_NUM):
            sx = random.randint(ROOM_SIZE_MIN_X, ROOM_SIZE_MAX_X + 1)
            sy = random.randint(ROOM_SIZE_MIN_Y, ROOM_SIZE_MAX_Y + 1)
            x = random.randint(0, MAP_SIZE_X - 1 - sx)
            y = random.randint(0, MAP_SIZE_Y - 1 - sy)
            newRoom = Rect(x, y, sx, sy)
            overlap = False
            for r in rooms:
                if newRoom.colliderect(r):
                    overlap = True
                    break
            if not overlap:
                rooms.append(newRoom)

        # Write rooms
        for r in rooms:
            for y in range(1, r.h):
                for x in range(1, r.w):
                    terrain.set_grid(x + r.x, y + r.y, 0)

    def _check_8tiles(loc: Vec2i) -> bool:
        '''Check 8 direction of a location is all blocked'''
        if loc.x < 1 or loc.x > MAP_SIZE_X - 2:
            return False
        if loc.y < 1 or loc.y > MAP_SIZE_Y - 2:
            return False

        sx = max(1, loc.x - 1)
        sy = max(1, loc.y - 1)
        dx = min(loc.x + 1, MAP_SIZE_X - 1)
        dy = min(loc.y + 1, MAP_SIZE_Y - 1)
        empty = True

        for x in range(sx, dx + 1):
            for y in range(sy, dy + 1):
                if terrain.get(x, y) != 1:
                    empty = False
        return empty

    def mark_available_connection():
        for y in range(1, MAP_SIZE_X - 1):
            for x in range(1, MAP_SIZE_Y - 1):
                if _check_8tiles(Vec2i(x, y)):
                    markMap.set_grid(x, y, 1)

    def _debug_draw_8tiles():
        for y in range(1, MAP_SIZE_X - 1):
            for x in range(1, MAP_SIZE_Y - 1):
                if markMap.get(x, y) == 1:
                    rect = Rect(x * TILE_PIXEL + 6, y * TILE_PIXEL + 6, 4, 4)
                    pygame.draw.rect(debug_surface, pygame.Color(0, 255, 0), rect)

    def available_connection_list() -> list:
        al = []
        for y in range(1, MAP_SIZE_X - 1):
            for x in range(1, MAP_SIZE_Y - 1):
                if markMap.get(x, y) == 1:
                    al.append(TilePos(x, y))
        return al

    def mark_8tiles_unavailable(loc: Vec2i):
        if loc.x < 1 or loc.x > MAP_SIZE_X - 2:
            return False
        if loc.y < 1 or loc.y > MAP_SIZE_Y - 2:
            return False

        sx = max(1, loc.x - 1)
        sy = max(1, loc.y - 1)
        dx = min(loc.x + 1, MAP_SIZE_X - 1)
        dy = min(loc.y + 1, MAP_SIZE_Y - 1)

        for x in range(sx, dx + 1):
            for y in range(sy, dy + 1):
                markMap.set_grid(x, y, 0)

    def available_direction_list(loc: Vec2i) -> list[Direction]:
        dl = []
        if loc.x > 1 and markMap.get(loc.x - 2, loc.y) == 1:
            dl.append(Direction.LEFT)
        if loc.x < MAP_SIZE_X - 2 and markMap.get(loc.x + 2, loc.y) == 1:
            dl.append(Direction.RIGHT)
        if loc.y > 1 and markMap.get(loc.x, loc.y - 2) == 1:
            dl.append(Direction.UP)
        if loc.y < MAP_SIZE_Y - 2 and markMap.get(loc.x, loc.y + 2) == 1:
            dl.append(Direction.DOWN)
        return dl

    def one_way_generate(start: TilePos, nodeList: list):
        adl = available_direction_list(start)

        while len(adl) > 0:
            direction: Direction = random.choice(adl)
            next1 = start.direct(direction)
            next2 = next1.direct(direction)
            nodeList.append(next2)
            mark_8tiles_unavailable(next2)
            # Carving tiles
            terrain.set_grid(next1.x, next1.y, 0)
            terrain.set_grid(next2.x, next2.y, 0)

            start = next2
            adl = available_direction_list(start)

    def gen_connection():

        while True:
            nodeList = []
            acl = available_connection_list()
            if len(acl) == 0:
                break

            start: TilePos = random.choice(acl)
            terrain.set_grid(start.x, start.y, 0)
            mark_8tiles_unavailable(start)
            nodeList.append(start)

            # Generate all road in one section
            while True:
                one_way_generate(start, nodeList)
                nodeList.pop()
                if len(nodeList) == 0:
                    break
                start = nodeList[-1]

    # Processing functions
    gen_rooms()
    mark_available_connection()
    gen_connection()

    return terrain
