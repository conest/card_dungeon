import random
from enum import IntEnum

import pygame
import setting

from pygame import Rect
from engine.lib.grid import GridInt
from engine.lib.vect import Vec2i
from engine.lib.tilePos import Direction, TilePos

MAP_SIZE_X = setting.MAP_SIZE_X
MAP_SIZE_Y = setting.MAP_SIZE_Y
TILE_PIXEL = setting.TILE_PIXEL


class Terrain(IntEnum):
    EMPTY = 0
    PATH = 1
    ROOM = 2
    DOOR = 11
    FOYER = 12

    WALL = 21
    STAIRS = 30
    BORDER = 99

    PLAYER = 100
    ENEMY = 101


def generator(debug_surface: pygame.Surface) -> tuple[GridInt, list]:

    terrain = GridInt(MAP_SIZE_X, MAP_SIZE_Y)
    markMap = GridInt(MAP_SIZE_X, MAP_SIZE_Y)
    rooms = []

    def gen_rooms():
        ROOM_TRYING_NUM = 200
        ROOM_SIZE_MAX_X = 10
        ROOM_SIZE_MIN_X = 4
        ROOM_SIZE_MAX_Y = 8
        ROOM_SIZE_MIN_Y = 4

        terrain.reset(Terrain.WALL)
        # gen rooms
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

        # make rooms
        for r in rooms:
            for y in range(1, r.h):
                for x in range(1, r.w):
                    terrain.set_grid(x + r.x, y + r.y, Terrain.ROOM)

        # shrink rooms
        for r in rooms:
            r.x += 1
            r.y += 1
            r.w -= 1
            r.h -= 1

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
                if terrain.get(x, y) != Terrain.WALL:
                    empty = False
        return empty

    def mark_available_connection():
        for y in range(1, MAP_SIZE_X - 1):
            for x in range(1, MAP_SIZE_Y - 1):
                if _check_8tiles(Vec2i(x, y)):
                    markMap.set_grid(x, y, 1)

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
            terrain.set_grid(next1.x, next1.y, Terrain.PATH)
            terrain.set_grid(next2.x, next2.y, Terrain.PATH)

            start = next2
            adl = available_direction_list(start)

    def gen_connection():
        mark_available_connection()
        # Generate all sections
        while True:
            nodeList = []
            acl = available_connection_list()
            if len(acl) == 0:
                break

            start: TilePos = random.choice(acl)
            terrain.set_grid(start.x, start.y, Terrain.PATH)
            mark_8tiles_unavailable(start)
            nodeList.append(start)

            # Generate all road in one section
            while True:
                one_way_generate(start, nodeList)
                nodeList.pop()
                if len(nodeList) == 0:
                    break
                start = nodeList[-1]

    def check_right_door(door: Vec2i, fd: Vec2i, rd: Vec2i, aDoors: list):
        if terrain.get(door.x, door.y) == Terrain.WALL and terrain.get(fd.x, fd.y) != Terrain.WALL:
            markMap.set_grid(door.x, door.y, 1)
            aDoors.append((door, rd))

    def make_room_doors(room: Rect) -> list[tuple]:
        '''Return tuple: (Door location, in room side / foyer)'''
        aDoors = []
        downWall = room.y + room.h
        rightWall = room.x + room.w

        # UP side
        if room.y > 1:
            for x in range(room.x, rightWall):
                door = Vec2i(x, room.y - 1)
                fd = Vec2i(x, room.y - 2)
                rd = Vec2i(x, room.y)
                check_right_door(door, fd, rd, aDoors)

        # DOWN side
        if downWall < MAP_SIZE_Y - 1:
            for x in range(room.x, rightWall):
                door = Vec2i(x, downWall)
                fd = Vec2i(x, downWall + 1)
                rd = Vec2i(x, downWall - 1)
                check_right_door(door, fd, rd, aDoors)

        # LEFT side
        if room.x > 1:
            for y in range(room.y, downWall):
                door = Vec2i(room.x - 1, y)
                fd = Vec2i(room.x - 2, y)
                rd = Vec2i(room.x, y)
                check_right_door(door, fd, rd, aDoors)

        # RIGHT side
        if rightWall < MAP_SIZE_X - 1:
            for y in range(room.y, downWall):
                door = Vec2i(rightWall, y)
                fd = Vec2i(rightWall + 1, y)
                rd = Vec2i(rightWall - 1, y)
                check_right_door(door, fd, rd, aDoors)

        return aDoors

    def gen_doors():
        MIN_DOORS = 2
        MAX_DOORS = 4
        markMap.reset()
        for room in rooms:
            doors = make_room_doors(room)
            random.shuffle(doors)
            doornum = random.randint(MIN_DOORS, MAX_DOORS)
            # small chance have no door
            # if random.randint(0, 20) == 0:
            #     doornum = 0
            for _ in range(doornum):
                if len(doors) == 0:
                    break
                tup = doors.pop()
                terrain.set_grid(tup[0].x, tup[0].y, Terrain.DOOR)
                terrain.set_grid(tup[1].x, tup[1].y, Terrain.FOYER)

    def find_deadend() -> list[Vec2i]:
        deadends = []
        for y in range(1, MAP_SIZE_X - 1):
            for x in range(1, MAP_SIZE_Y - 1):
                if terrain.get(x, y) != Terrain.PATH:
                    continue
                wallNum = 0
                if terrain.get(x - 1, y) == Terrain.WALL:
                    wallNum += 1
                if terrain.get(x + 1, y) == Terrain.WALL:
                    wallNum += 1
                if terrain.get(x, y - 1) == Terrain.WALL:
                    wallNum += 1
                if terrain.get(x, y + 1) == Terrain.WALL:
                    wallNum += 1
                # count
                if wallNum >= 3:
                    deadends.append(Vec2i(x, y))
        return deadends

    def simplify_path():
        SIMPLIFY_NUM = 160
        count = SIMPLIFY_NUM
        deadends = find_deadend()
        if len(deadends) == 0:
            return
        while count > 0:
            count -= 1
            de = deadends.pop()
            terrain.set_grid(de.x, de.y, Terrain.WALL)
            if len(deadends) == 0:
                deadends = find_deadend()
                if len(deadends) == 0:
                    return

    def _debug_check_markMap():
        for y in range(1, MAP_SIZE_X - 1):
            for x in range(1, MAP_SIZE_Y - 1):
                if markMap.get(x, y) == 1:
                    rect = Rect(x * TILE_PIXEL + 6, y * TILE_PIXEL + 6, 4, 4)
                    pygame.draw.rect(debug_surface, pygame.Color(0, 255, 0), rect)

    def _debug_draw_terrain_mark():
        for y in range(1, MAP_SIZE_X - 1):
            for x in range(1, MAP_SIZE_Y - 1):
                if terrain.get(x, y) == Terrain.ROOM:
                    rect = Rect(x * TILE_PIXEL + 6, y * TILE_PIXEL + 6, 4, 4)
                    pygame.draw.rect(debug_surface, pygame.Color(255, 255, 0), rect)
                if terrain.get(x, y) == Terrain.PATH:
                    rect = Rect(x * TILE_PIXEL + 6, y * TILE_PIXEL + 6, 4, 4)
                    pygame.draw.rect(debug_surface, pygame.Color(0, 255, 255), rect)
                if terrain.get(x, y) == Terrain.DOOR:
                    rect = Rect(x * TILE_PIXEL + 6, y * TILE_PIXEL + 6, 4, 4)
                    pygame.draw.rect(debug_surface, pygame.Color(255, 0, 0), rect)
                if terrain.get(x, y) == Terrain.FOYER:
                    rect = Rect(x * TILE_PIXEL + 6, y * TILE_PIXEL + 6, 4, 4)
                    pygame.draw.rect(debug_surface, pygame.Color(128, 0, 128), rect)

    # Processing functions
    gen_rooms()
    gen_connection()
    gen_doors()
    # _debug_check_markMap()
    # _debug_draw_terrain_mark()
    simplify_path()

    return (terrain, rooms)
