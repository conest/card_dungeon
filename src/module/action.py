from enum import Enum, auto
import pygame

from engine.lib.vect import Vec2i, Vec2f
from engine.lib.tilePos import TilePos, Direction
from engine.camera import CameraStack
from engine.surfaceItem import SurfaceList, SurfaceItem

import setting
from module.map_element import MapElementManage
from module.map import Map
from module.map_terrain import Terrain
from module.player import Player
from creature.creature import Behavior, Creature, CreatureGroup, MOVING_SPEED, ATTACK_SPEED
from creature.kind import Kind


class Stage(Enum):
    IDLE = auto()
    MOVE = auto()
    ATTACK = auto()
    C_ATTACK = auto()


class Action:

    stage: Stage
    stageList: list[Stage]
    animateTimeCount: float

    player: Player
    enemies: CreatureGroup
    elements: MapElementManage
    camera: CameraStack
    surfaceList: SurfaceList
    mapClass: Map

    source: Creature
    target: Creature
    tPosition: Vec2f

    attackedEffect: SurfaceItem
    attackedMask: pygame.mask.Mask

    def __init__(self, surfaceList: SurfaceList):
        self.stage = Stage.IDLE
        self.stageList = []  # reversed list
        self.animateTimeCount = 0
        self.surfaceList = surfaceList

        self.load_attackedEffect()

    def load_attackedEffect(self):
        attackedEffect = SurfaceItem()
        self.attackedEffect = attackedEffect
        attackedEffect.name = "attackedEffect"
        attackedEffect.new(setting.TILE_PIXEL_ZOOMED, setting.TILE_PIXEL_ZOOMED)
        attackedEffect.surface.fill((0))
        attackedEffect.visible = False
        attackedEffect.zIndex = 5
        self.surfaceList.add(attackedEffect)

    def player_wait(self):
        self.stageList = [Stage.MOVE, Stage.C_ATTACK]  # reversed list
        self.enemies.gen_behavior()
        self.next_stage()

    def player_try_move(self, d: Direction):
        newLoc = self.player.pos.direct(d)
        # Idle
        if self.mapClass.terrain.get_v(newLoc) == Terrain.WALL:
            return
        if self.mapClass.creatureMap.get_v(newLoc) != Kind.Nothing:
            # Attack
            pos = self.player.pos.direct(d)
            target = self.enemies.get_by_pos(pos)
            self.attack(self.player, target)
            self.stageList = [Stage.MOVE, Stage.C_ATTACK, Stage.ATTACK]  # reversed list
        else:
            # Move
            self.player.set_move(d)
            self.stageList = [Stage.C_ATTACK, Stage.MOVE]  # reversed list
        self.enemies.gen_behavior()
        self.next_stage()

    def next_stage(self):
        if self.stageList == []:
            self.stage_set(Stage.IDLE)
            self.enemies.reset_behavior()
            return
        self.stage_set(self.stageList.pop())

    def stage_set(self, stage: Stage):
        self.stage = stage
        self.animateTimeCount = 0

    def attack(self, source: Creature, target: Creature):
        self.stage_set(Stage.ATTACK)
        self.source = source
        self.target = target

        self.tPosition = source.sprite.position
        dd = target.pos - source.pos
        scale = setting.ZOOM * 4
        df = Vec2f(dd.x * scale, dd.y * scale)
        source.sprite.position = source.sprite.position + df

        self.attackedEffect.surface.fill(0)
        self.target.sprite.draw_directly(self.attackedEffect.surface)
        self.attackedMask = pygame.mask.from_surface(self.attackedEffect.surface)
        self.attackedMask.to_surface(self.attackedEffect.surface, setcolor=(255, 0, 0, 255), unsetcolor=(0, 0, 0, 0))

        self.attackedEffect.set_position_v(target.sprite.position)
        self.attackedEffect.visible = True

    def process(self, delta: int):
        match self.stage:
            case Stage.IDLE:
                pass
            case Stage.MOVE:
                self.process_moving(delta)
                self.camera.onFocus(self.player.centerAPos())
                self.elements.checkAllCamera()
            case Stage.ATTACK:
                self.process_attack(delta)
            case Stage.C_ATTACK:
                self.check_enemy_attack(delta)

    def process_moving(self, delta: int):
        self.animateTimeCount += MOVING_SPEED * delta
        if self.animateTimeCount >= setting.TILE_PIXEL:
            self.player.reached()
            self.enemies.reached()
            self.next_stage()
        else:
            self.player.moving(delta)
            self.enemies.moving(delta)

    def process_attack(self, delta: int):
        self.animateTimeCount += ATTACK_SPEED * delta
        if self.animateTimeCount < setting.TILE_PIXEL:
            alpha = 255 * (1 - self.animateTimeCount / setting.TILE_PIXEL)
            self.attackedMask.to_surface(self.attackedEffect.surface, setcolor=(255, 0, 0, alpha), unsetcolor=(0, 0, 0, 0))
            return

        # Ending a attack
        self.attackedEffect.visible = False
        self.source.sprite.position = self.tPosition
        self.apply_attack()

        self.next_stage()

    def check_enemy_attack(self, delta: int):
        nAttacker = self.enemies.get_attacker()
        if nAttacker is None:
            self.next_stage()
            return
        # Have enemy attack
        self.attack(nAttacker, self.player)
        self.stageList.append(Stage.C_ATTACK)
        self.stage_set(Stage.ATTACK)
        self.process_attack(delta)

    def apply_attack(self):
        target = self.target
        isDead = target.attacked(self.source)
        # TODO: Player's death
        if (target.name == Player.NAME) and isDead:
            print("Oh, you are dead")
            return
        # Enemy dead
        if isDead:
            self.mapClass.creatureMap.set_grid_v(target.pos, Kind.Nothing)
            self.elements.delete(target.name)
            self.enemies.delete(target.name)
            self.surfaceList.delete(target.sprite.name)
