from enum import Enum, auto

import pygame

from engine.lib.vect import Vec2i, Vec2f
from engine.lib.tilePos import TilePos, Direction, DIR_LOC

from engine.scene import Scene, SceneSignal
from engine.resource import resource
from engine.camera import CameraStack

import setting
from scene.keys import readkey
from module.map import Map
from module.player import Player
from module.map_element import MapElementManage, MOVING_SPEED


class Stage(Enum):
    IDLE = auto()
    MOVING = auto()


class GameScene(Scene):

    stage: Stage
    player: Player
    movingCount: float

    def init(self):
        self.stage = Stage.IDLE
        self.movingVect = Vec2f()
        self.movingCount = 0

        resource.add_surface("tilesheet", "assets/DungeonTileset.png")

        mapClass = Map()
        mapClass.tilemap_load_resource(resource.surface("tilesheet"), 16, 23)
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

        player = Player()
        self.player = player
        player.mapClass = mapClass
        self.surfaceList.add(player.sprite)

        playerPos = mapClass.player_and_stairs_pos()
        player.move_to(TilePos.from_vect2i(playerPos))

        camera.moveCenter(player.centerAPos())

        mem = MapElementManage(camera)
        self.objects[MapElementManage.NAME] = mem
        mem.add(player)
        mem.checkCamera(player.name)

        # DEBUG
        # self.surfaceList.add(mapClass.tilemap)

    def player_set_moving(self, d: Direction):
        if not self.player.check_move(d):
            return
        self.stage = Stage.MOVING
        self.movingCount = 0
        movingVect = Vec2f.from_tuple(DIR_LOC[d])
        movingDes = self.player.pos.direct(d)
        self.player.set_moving(movingVect, movingDes)

    def moving(self, delta: int):
        self.movingCount += MOVING_SPEED * delta
        if self.movingCount >= setting.TILE_PIXEL:
            self.player.reached()
            self.stage = Stage.IDLE
        else:
            self.player.moving(delta)
        self.objects["map_camera"].onFocus(self.player.centerAPos())
        self.objects[MapElementManage.NAME].checkAllCamera()

    def event_handle(self, event: pygame.event.Event, delta: int):
        if self.stage != Stage.IDLE:
            return

        if event.type == pygame.KEYDOWN:
            key = readkey(event)
            if key is None:
                return
            match key:
                case "LEFT":
                    self.player_set_moving(Direction.LEFT)
                case "RIGHT":
                    self.player_set_moving(Direction.RIGHT)
                case "UP":
                    self.player_set_moving(Direction.UP)
                case "DOWN":
                    self.player_set_moving(Direction.DOWN)

    def process(self, delta: int) -> SceneSignal:
        match self.stage:
            case Stage.IDLE:
                return
            case Stage.MOVING:
                self.moving(delta)


gameScene = GameScene()
