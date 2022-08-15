from enum import Enum, auto
import pygame

import setting
from engine.lib.vect import Vec2f
from engine.lib.num import approach
from engine.lib.tilePos import TilePos
from engine.resource import resource
from engine.sufaceItem import SurfaceItem
from engine.sprite import AnimatedSprite
from engine.animation import Animation
from module.map_element import MapElement


class Status(Enum):
    IDLE = auto()
    WALK = auto()
    ATTACK = auto()


class Player(MapElement):
    NAME = "player"

    status: Status

    def __init__(self):
        resource.add_surface(Player.NAME, "assets/Dwarves.png")
        resource.scale_surface(Player.NAME, setting.ZOOM)
        super().__init__(Player.NAME, AnimatedSprite(resource.surface("player")))

        self.sprite.name = Player.NAME
        self.sprite.set_framesHV(25, 6)
        self._load_animation()

        self.status = Status.IDLE

    def __str__(self) -> str:
        return "[Player]"

    def move(self, x: int, y: int):
        self.pos += TilePos(x, y)
        self.sprite.position = Vec2f(self.pos.x, self.pos.y) \
            * setting.TILE_PIXEL * setting.ZOOM

    def _load_animation(self):
        player = self.sprite

        frames: list = [(1, 5, 200), (2, 5, 200), (3, 5, 200), (4, 5, 200)]
        player.add_and_load_animation("idle", frames, True)

        player.animation.play("idle")
