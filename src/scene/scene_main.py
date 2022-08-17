import functools
import pygame

from engine.lib.vect import Vec2i
from engine.lib.tilePos import TilePos, Direction

from engine.scene import Scene
from engine.resource import resource
from engine.camera import CameraStack

import setting
from scene.keys import readkey
from module.map import Map
from module.player import Player
from module.map_element import MapElementManage


def init(self: Scene):
    resource.add_surface("tilesheet", "assets/DungeonTileset.png")

    mapClass = Map()
    mapClass.tilemap_load_resource(resource.surface("tilesheet"), 16, 23)
    mapClass.map_generate()
    mapClass.draw_map()
    self.objects["map"] = mapClass

    windowSize = Vec2i(setting.WINDOW_SIZE[0], setting.WINDOW_SIZE[1])
    camera = CameraStack(windowSize, setting.ZOOM, True)
    camera.add_source(mapClass.si())
    camera.update_surface()
    self.objects["map_camera"] = camera
    self.surfaceList.add(camera)

    player = Player()
    player.mapClass = mapClass
    (playerPos, _) = mapClass.player_and_stairs_pos()
    player.move_to(TilePos.from_vect2i(playerPos))
    self.objects[Player.NAME] = player
    self.surfaceList.add(player.sprite)

    camera.moveCenter(player.centerAPos())

    mem = MapElementManage(camera)
    self.objects[MapElementManage.NAME] = mem
    mem.add(player)
    mem.checkCamera(player.name)

    # DEBUG
    # self.surfaceList.add(map.tilemap)


def event_handle(self: Scene, event: pygame.event.Event, delta: int):
    if event.type == pygame.KEYDOWN:
        key = readkey(event)
        if key is None:
            return
        match key:
            case "LEFT":
                self.objects["map_camera"].move(-16, 0)
                self.objects["player"].move(Direction.LEFT)
                self.objects[MapElementManage.NAME].checkAllCamera()
            case "RIGHT":
                self.objects["map_camera"].move(16, 0)
                self.objects["player"].move(Direction.RIGHT)
                self.objects[MapElementManage.NAME].checkAllCamera()
            case "UP":
                self.objects["map_camera"].move(0, -16)
                self.objects["player"].move(Direction.UP)
                self.objects[MapElementManage.NAME].checkAllCamera()
            case "DOWN":
                self.objects["map_camera"].move(0, 16)
                self.objects["player"].move(Direction.DOWN)
                self.objects[MapElementManage.NAME].checkAllCamera()


gameScene = Scene()
gameScene.init = functools.partial(init, gameScene)
gameScene.event_handle = functools.partial(event_handle, gameScene)
