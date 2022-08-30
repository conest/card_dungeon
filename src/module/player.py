import setting
from engine.lib.vect import Vec2f
from engine.resource import resource
from engine.sprite import AnimatedSprite
from engine.lib.tilePos import Direction, DIR_LOC
from engine.signal import Signal

from creature.creature import Creature
from creature.kind import Kind
from module.map import Map


class Player(Creature):
    NAME = "player"
    KIND = Kind.Player

    maxHP: int = 50
    hp: int = 50
    atk: int = 10
    defence: int = 10

    def __init__(self, mapClass: Map):
        resource.add_surface(Player.NAME, setting.ASSERT_PLAYER)
        resource.scale_surface(Player.NAME, setting.ZOOM)
        super().__init__(Player.NAME, AnimatedSprite(resource.surface("player")), mapClass)

        self.kind = Player.KIND
        self.sprite.name = Player.NAME
        self.sprite.set_framesHV(25, 6)
        self._load_animation()
        self.sprite.zIndex = 2

        self.maxHP = Player.maxHP
        self.hp = Player.hp
        self.atk = Player.atk
        self.defence = Player.defence

        self.signals.sign(Signal("change_attribute", Player.NAME))

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
        self.mapClass.creatureMap.set_grid_v(self.pos, Kind.Nothing)
        self.mapClass.creatureMap.set_grid_v(movingDes, self.kind)

    def change_attribute(self):
        self.signals.set_data("change_attribute", [self.hp, self.atk, self.defence])
        self.signals.active("change_attribute")
