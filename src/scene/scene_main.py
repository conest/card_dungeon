import functools
import pygame

from scene.keys import readkey
from engine.scene import Scene
from engine.resource import resource
from engine.camera import Camera
# from engine.tilemap import TileMap
from engine.lib.vect import Vec2i
from module.map import Map
from module.map_pathfinding import aStar


def init(self: Scene):
    resource.add_surface("tilesheet", "assets/DungeonTileset.png")

    map = Map()
    map.tilemap_load_resource(resource.surface("tilesheet"), 16, 23)
    map.map_generate()
    map.draw_map()
    self.objects["map"] = map

    camera = Camera(800, 450, 2, True)
    camera.load_source(map.surface())
    camera.update_surface()
    self.objects["camera"] = camera

    self.surfaceList.add(map.tilemap)

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
                self.objects["camera"].move(-16, 0)
            case "RIGHT":
                self.objects["camera"].move(16, 0)
            case "UP":
                self.objects["camera"].move(0, -16)
            case "DOWN":
                self.objects["camera"].move(0, 16)

    if event.type == pygame.MOUSEBUTTONUP:
        loc = Vec2i(event.pos[0], event.pos[1]) // 16
        print(f'loc: {loc}')
        if event.button == 1:
            self.pathStart = loc
        if event.button == 3:
            self.pathTarget = loc
            path = aStar(self.objects["map"].terrain, self.pathStart, self.pathTarget)
            debug_surface: pygame.Surface = self.objects["map"].debug_surface.surface
            debug_surface.fill((0))
            for p in path:
                rect = pygame.Rect(p.x * 16 + 6, p.y * 16 + 6, 4, 4)
                pygame.draw.rect(debug_surface, pygame.Color(0, 255, 0), rect)


gameScene = Scene()
gameScene.init = functools.partial(init, gameScene)
gameScene.event_handle = functools.partial(event_handle, gameScene)
