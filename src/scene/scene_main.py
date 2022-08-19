from enum import Enum, auto

import pygame

from engine.lib.vect import Vec2i, Vec2f
from engine.lib.tilePos import TilePos, Direction
from engine.scene import Scene, SceneSignal
from engine.resource import resource
from engine.camera import CameraStack

import setting

from scene.keys import readkey
from module.map import Map
from module.player import Player
from module.map_element import MapElementManage
from creature import enemy_tool as etool
from creature.creature import CreatureGroup
from creature.creature import MOVING_SPEED


class Stage(Enum):
    IDLE = auto()
    MOVING = auto()


class GameScene(Scene):

    stage: Stage

    mem: MapElementManage
    '''All the elements'''
    enemies: CreatureGroup
    ''' Enemy Group'''
    player: Player
    movingCount: float

    def init(self):
        self.stage = Stage.IDLE
        self.movingVect = Vec2f()
        self.movingCount = 0

        resource.add_surface("DungeonTileset", "assets/DungeonTileset.png")
        resource.add_surface("animalsheet", "assets/AnimalsSheet.png")
        resource.scale_surface("animalsheet", setting.ZOOM)

        mapClass = Map()
        mapClass.tilemap_load_resource(resource.surface("DungeonTileset"), 16, 23)
        mapClass.map_generate()
        mapClass.draw_map()
        self.objects["map"] = mapClass

        windowSize = Vec2i(setting.WINDOW_SIZE[0], setting.WINDOW_SIZE[1])
        camera = CameraStack(windowSize, setting.ZOOM, True)
        camera.zIndex = -1
        camera.add_source(mapClass.si())
        camera.update_surface()
        self.objects["map_camera"] = camera
        self.surfaceList.add(camera)

        player = Player(mapClass)
        self.player = player
        self.surfaceList.add(player.sprite)

        playerPos = mapClass.player_and_stairs_pos()
        player.move_to(TilePos.from_vect2i(playerPos))

        camera.moveCenter(player.centerAPos())

        mem = MapElementManage(camera)
        self.mem = mem
        self.enemies = CreatureGroup()
        mem.add(player)

        eList = etool.gen_enemies(mapClass)
        for e in eList:
            self.surfaceList.add(e.sprite)
            self.enemies.add(e)
            mem.add(e)
        mem.checkAllCamera()

        # DEBUG
        # self.surfaceList.add(mapClass.tilemap)

    def player_try_move(self, d: Direction):
        if not self.player.check_move(d):
            return
        self.player.set_move(d)

        self.stage = Stage.MOVING
        self.movingCount = 0
        self.enemies.random_move()

    def event_handle(self, event: pygame.event.Event, delta: int):
        if self.stage != Stage.IDLE:
            return
        if event.type == pygame.KEYDOWN:
            key = readkey(event)
            if key is None:
                return
            match key:
                case "LEFT":
                    self.player_try_move(Direction.LEFT)
                case "RIGHT":
                    self.player_try_move(Direction.RIGHT)
                case "UP":
                    self.player_try_move(Direction.UP)
                case "DOWN":
                    self.player_try_move(Direction.DOWN)

    def process(self, delta: int) -> SceneSignal:
        match self.stage:
            case Stage.IDLE:
                return
            case Stage.MOVING:
                self.process_moving(delta)

    def process_moving(self, delta: int):
        self.movingCount += MOVING_SPEED * delta
        if self.movingCount >= setting.TILE_PIXEL:
            self.player.reached()
            self.enemies.reached()
            self.stage = Stage.IDLE
        else:
            self.player.moving(delta)
            self.enemies.moving(delta)

        self.objects["map_camera"].onFocus(self.player.centerAPos())
        self.mem.checkAllCamera()


gameScene = GameScene()
