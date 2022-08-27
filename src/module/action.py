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
from creature.creature import Creature, CreatureGroup, MOVING_SPEED, ATTACK_SPEED
from creature.kind import Kind


class Stage(Enum):
    IDLE = auto()
    MOVE = auto()
    ATTACK = auto()


class Action:

    stage: Stage
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

    def player_try_move(self, d: Direction):
        newLoc = self.player.pos.direct(d)
        # Idle
        if self.mapClass.terrain.get_v(newLoc) == Terrain.WALL:
            return
        # Attack
        if self.mapClass.creatureMap.get_v(newLoc) != Kind.Nothing:
            pos = self.player.pos.direct(d)
            target = self.enemies.get_by_pos(pos)
            self.attack(self.player, target)
            return
        # Move
        self.player.set_move(d)
        self.enemiesAI()

    def stage_set(self, stage: Stage):
        # TODO
        # print(stage)
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

    def enemiesAI(self):
        # TODO
        self.enemies.ai()
        self.stage_set(Stage.MOVE)

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

    def process_moving(self, delta: int):
        self.animateTimeCount += MOVING_SPEED * delta
        if self.animateTimeCount >= setting.TILE_PIXEL:
            self.player.reached()
            self.enemies.reached()
            self.stage = Stage.IDLE
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
        # TODO
        self.enemiesAI()
