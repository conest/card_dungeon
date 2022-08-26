from enum import Enum, auto

import setting
from engine.lib.vect import Vec2i, Vec2f
from engine.resource import resource
from engine.sprite import AnimatedSprite
from engine.lib.tilePos import TilePos, Direction, DIR_LOC

from creature.creature import Creature
from creature.kind import Kind
from module.map import Map
from module.map_terrain import Terrain


class PlayBehavior(Enum):
    IDLE = auto()
    MOVE = auto()
    ATTACK = auto()


class Player(Creature):
    NAME = "player"

    def __init__(self, mapClass: Map):
        resource.add_surface(Player.NAME, "assets/Dwarves.png")
        resource.scale_surface(Player.NAME, setting.ZOOM)
        super().__init__(Player.NAME, AnimatedSprite(resource.surface("player")), mapClass)

        self.kind = Kind.Player
        self.sprite.name = Player.NAME
        self.sprite.set_framesHV(25, 6)
        self._load_animation()

    def __str__(self) -> str:
        return "[Player]"

    def _load_animation(self):
        player = self.sprite

        frames: list = [(1, 5, 200), (2, 5, 200), (3, 5, 200), (4, 5, 200)]
        player.add_and_load_animation("idle", frames, True)

        player.animation.play("idle")

    def set_move(self, d: Direction):
        movingVect = Vec2f.from_tuple(DIR_LOC[d])
        movingDes = self.pos.direct(d)
        self.set_moving(movingVect, movingDes)
        self.mapClass.creatureMap.set_grid_v(self.pos, 0)
        self.mapClass.creatureMap.set_grid_v(movingDes, self.kind)

    def check_attack_move(self, d: Direction) -> PlayBehavior:
        newLoc = self.pos.direct(d)
        if self.mapClass.creatureMap.get_v(newLoc) != Kind.Nothing:
            return PlayBehavior.ATTACK
        if self.mapClass.terrain.get_v(newLoc) == Terrain.WALL:
            return PlayBehavior.IDLE
        return PlayBehavior.MOVE
