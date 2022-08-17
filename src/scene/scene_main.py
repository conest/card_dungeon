import functools
import pygame

from engine.lib.vect import Vec2i

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

    map = Map()
    map.tilemap_load_resource(resource.surface("tilesheet"), 16, 23)
    map.map_generate()
    map.draw_map()

    self.objects["map"] = map

    windowSize = Vec2i(setting.WINDOW_SIZE[0], setting.WINDOW_SIZE[1])
    camera = CameraStack(windowSize, setting.ZOOM, True)
    camera.add_source(map.si())
    camera.update_surface()
    self.objects["map_camera"] = camera
    self.surfaceList.add(camera)

    player = Player()
    player.move_to(11, 11)
    self.objects[Player.NAME] = camera
    self.surfaceList.add(player.sprite)

    mem = MapElementManage(camera)
    self.objects[MapElementManage.NAME] = mem
    mem.add(player)
    mem.checkCamera(player.name)


def event_handle(self: Scene, event: pygame.event.Event, delta: int):
    if event.type == pygame.KEYDOWN:
        key = readkey(event)
        if key is None:
            return
        match key:
            case "LEFT":
                self.objects["map_camera"].move(-8, 0)
                self.objects[MapElementManage.NAME].checkAllCamera()
            case "RIGHT":
                self.objects["map_camera"].move(8, 0)
                self.objects[MapElementManage.NAME].checkAllCamera()
            case "UP":
                self.objects["map_camera"].move(0, -8)
                self.objects[MapElementManage.NAME].checkAllCamera()
            case "DOWN":
                self.objects["map_camera"].move(0, 8)
                self.objects[MapElementManage.NAME].checkAllCamera()


gameScene = Scene()
gameScene.init = functools.partial(init, gameScene)
gameScene.event_handle = functools.partial(event_handle, gameScene)
