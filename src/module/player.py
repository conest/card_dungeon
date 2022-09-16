import setting
import asset as ASSET

from engine.lib.vect import Vec2f
from engine.resource import resource
from engine.sprite import AnimatedSprite
from engine.lib.tilePos import Direction, DIR_LOC
from engine.signal import Signal

from creature.creature import Creature
from creature.kind import Kind
from module.map import Map
from card.card import Card


class Player(Creature):
    NAME = "player"
    KIND = Kind.Player

    maxHP: int = 50
    hp: int = 50
    atk: int = 10
    defence: int = 10

    cards: list[Card]

    def __init__(self, mapClass: Map):
        resource.add_surface(Player.NAME, ASSET.PLAYER)
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

        self.cards = []

        self.signals.sign(Signal("change_attribute", Player.NAME))
        self.signals.sign(Signal("change_hp", Player.NAME))
        self.signals.sign(Signal("get_card", Player.NAME))

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

    def attacked(self, attacker: Creature) -> bool:
        '''(@Player) Overload Creature's attacked method'''
        damage = max(0, attacker.atk - self.defence)
        print(f'! {self.name} attacked by {attacker.name} cause {damage} damage')
        isDead = self.set_hp(-damage)
        self.emit_change_hp()
        if isDead:
            # TODO: player isDead
            pass
        return isDead

    def get_card(self, card: Card):
        self.cards.append(card)
        self.emit_get_card(card)

    def _link_use_card(self, data: list):
        '''data: [index]'''
        [index] = data
        self.cards[index].use()
        self.cards.pop(index)

        # TODO: For potion effect only
        self.hp += 20
        self.hp = min(self.maxHP, self.hp)
        self.emit_change_hp()

    def emit_change_attribute(self):
        self.signals.set_data("change_attribute", [self.hp, self.atk, self.defence])
        self.signals.active("change_attribute")

    def emit_change_hp(self):
        self.signals.set_data("change_hp", [self.hp, self.maxHP])
        self.signals.active("change_hp")

    def emit_get_card(self, card: Card):
        self.signals.set_data("get_card", [card])
        self.signals.active("get_card")
