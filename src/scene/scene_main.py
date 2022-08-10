import functools
from engine.scene import Scene
from engine.resource import resource
# from engine.tilemap import TileMap
# from engine.lib.vect import Vec2i
from module.map import Map


def init(self):
    resource.add_surface("tilesheet", "assets/DungeonTileset.png")

    map = Map()
    map.tilemap_load_resource(resource.surface("tilesheet"), 16, 23)
    map.map_generate()
    map.draw_map()

    self.add_surface(map.tilemap)
    self.add_surface(map.debug_surface)


gameScene = Scene()
gameScene.init = functools.partial(init, gameScene)
