from enum import Enum, auto

from engine.lib.tilePos import TilePos, Direction
from engine.camera import CameraStack
from engine.surfaceItem import SurfaceList, SurfaceItem

import setting
from module.map_element import MapElementManage
from module.player import PlayBehavior, Player
from creature.creature import Creature, CreatureGroup, MOVING_SPEED, ATTACK_SPEED


class Act(Enum):
    IDLE = auto()
    MOVE = auto()
    ATTACK = auto()


class Action:

    act: Act
    animateTimeCount: float

    player: Player
    enemies: CreatureGroup
    elements: MapElementManage
    camera: CameraStack
    surfaceList: SurfaceList

    source: Creature
    target: Creature

    attackedEffect: SurfaceItem

    def __init__(self, surfaceList: SurfaceList):
        self.act = Act.IDLE
        self.animateTimeCount = 0
        self.surfaceList = surfaceList

        self.load_attackedEffect()

    def load_attackedEffect(self):
        attackedEffect = SurfaceItem()
        self.attackedEffect = attackedEffect
        attackedEffect.name = "attackedEffect"
        attackedEffect.new(setting.TILE_PIXEL_ZOOMED, setting.TILE_PIXEL_ZOOMED)
        attackedEffect.surface.fill((255, 0, 0, 128))
        attackedEffect.visible = False
        attackedEffect.zIndex = 5
        self.surfaceList.add(attackedEffect)      

    def player_try_move(self, d: Direction):
        match self.player.check_attack_move(d):
            case PlayBehavior.MOVE:
                self.act = Act.MOVE
                self.player.set_move(d)
                self.animateTimeCount = 0
                self.enemies.random_move()
            case PlayBehavior.ATTACK:
                pos = self.player.pos.direct(d)
                target = self.enemies.get_by_pos(pos)
                # TODO
                self.attack(self.player, target)
                print(f"attack: {target.name}")

    def attack(self, source: Creature, target: Creature):
        self.act = Act.ATTACK
        self.source = source
        self.target = target
        # TODO
        self.attackedEffect.set_position_v(target.sprite.position)
        self.attackedEffect.visible = True
        self.animateTimeCount = 0

    def process(self, delta: int):
        match self.act:
            case Act.IDLE:
                pass
            case Act.MOVE:
                self.process_moving(delta)
                self.camera.onFocus(self.player.centerAPos())
                self.elements.checkAllCamera()
            case Act.ATTACK:
                self.process_attack(delta)

    def process_moving(self, delta: int):
        self.animateTimeCount += MOVING_SPEED * delta
        if self.animateTimeCount >= setting.TILE_PIXEL:
            self.player.reached()
            self.enemies.reached()
            self.act = Act.IDLE
        else:
            self.player.moving(delta)
            self.enemies.moving(delta)

    def process_attack(self, delta: int):
        self.animateTimeCount += ATTACK_SPEED * delta
        if self.animateTimeCount >= setting.TILE_PIXEL:
            self.act = Act.IDLE
            self.attackedEffect.visible = False
