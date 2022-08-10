import random
from engine.lib.grid import GridInt
from engine.lib.vect import Vec2i





def _gen_rooms(grid: GridInt):
    ROOM_TRYING_NUM = 100
    ROOM_SIZE_MAX_X = 12
    ROOM_SIZE_MIN_X = 4
    ROOM_SIZE_MAX_Y = 10
    ROOM_SIZE_MIN_Y = 4

    grid.reset(1)
    size = grid.size()
    for _ in range(ROOM_TRYING_NUM):
        sx = random.randint(ROOM_SIZE_MIN_X, ROOM_SIZE_MAX_X + 1)
        sy = random.randint(ROOM_SIZE_MIN_Y, ROOM_SIZE_MAX_Y + 1)


def map_generate(grid: GridInt):
    size = grid.size()

