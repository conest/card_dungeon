import functools
import pygame

from engine.lib.vect import Vec2i
from engine.scene import Scene
from engine.resource import resource
from engine.camera import Camera, CameraStack

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
    camera = Camera(windowSize, setting.ZOOM, True)
    camera.load_source(map.si())
    camera.update_surface()
    self.objects["map_camera"] = camera
    self.surfaceList.add(camera)

    mem = MapElementManage(camera)
    self.objects[MapElementManage.NAME] = mem
    player = Player()
    player.move_to(11, 11)
    mem.add(player)
    mem.checkCamera()
    self.surfaceList.add(player.sprite)


def event_handle(self: Scene, event: pygame.event.Event, delta: int):
    if event.type == pygame.KEYDOWN:
        key = readkey(event)
        if key is None:
            return
        match key:
            case "LEFT":
                self.objects["map_camera"].move(-8, 0)
                self.objects[MapElementManage.NAME].checkCamera()
            case "RIGHT":
                self.objects["map_camera"].move(8, 0)
                self.objects[MapElementManage.NAME].checkCamera()
            case "UP":
                self.objects["map_camera"].move(0, -8)
                self.objects[MapElementManage.NAME].checkCamera()
            case "DOWN":
                self.objects["map_camera"].move(0, 8)
                self.objects[MapElementManage.NAME].checkCamera()


gameScene = Scene()
gameScene.init = functools.partial(init, gameScene)
gameScene.event_handle = functools.partial(event_handle, gameScene)
