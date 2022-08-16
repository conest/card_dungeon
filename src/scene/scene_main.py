import functools
import pygame

from engine.lib.vect import Vec2i
from engine.lib.tilePos import TilePos

from engine.scene import Scene
from engine.resource import resource
from engine.camera import Camera, CameraStack

import setting
from scene.keys import readkey
from module.map import Map
from module.player import Player
from module.map_element import MapElementManage
from module import map_algorithm as algorithm
from module.map_generator import Terrain


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
    # self.surfaceList.add(camera)
    self.surfaceList.add(map.tilemap)

    player = Player()
    player.move_to(11, 11)
    self.objects[Player.NAME] = camera
    self.surfaceList.add(player.sprite)

    mem = MapElementManage(camera)
    self.objects[MapElementManage.NAME] = mem
    mem.add(player)
    mem.checkCamera(player.name)

    # DEBUG
    self.pathStart = Vec2i()
    self.pathTarget = Vec2i()
    self.surfaceList.add(map.debug_surface)


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

    if event.type == pygame.MOUSEBUTTONUP:
        loc = Vec2i(event.pos[0], event.pos[1]) // 16
        print(f'loc: {loc}')
        if event.button == 1:
            stime = pygame.time.get_ticks()
            path = algorithm.bfsPath(self.objects["map"].terrain, Terrain.WALL, TilePos().fromVect(loc))
            print(f'Time: {pygame.time.get_ticks() -stime}')
            print(f"path size: {len(path)}")
            debug_surface: pygame.Surface = self.objects["map"].debug_surface.surface
            debug_surface.fill((0))
            for p in path:
                rect = pygame.Rect(p.x * 16 + 6, p.y * 16 + 6, 4, 4)
                pygame.draw.rect(debug_surface, pygame.Color(255, 255, 0), rect)
        if event.button == 3:
            stime = pygame.time.get_ticks()
            path = algorithm.bfsArea(self.objects["map"].terrain, Terrain.WALL, TilePos().fromVect(loc))
            print(f'Time: {pygame.time.get_ticks() -stime}')
            print(f"path size: {len(path)}")
            debug_surface: pygame.Surface = self.objects["map"].debug_surface.surface
            debug_surface.fill((0))
            for p in path:
                rect = pygame.Rect(p.x * 16 + 6, p.y * 16 + 6, 4, 4)
                pygame.draw.rect(debug_surface, pygame.Color(255, 0, 255), rect)


gameScene = Scene()
gameScene.init = functools.partial(init, gameScene)
gameScene.event_handle = functools.partial(event_handle, gameScene)
