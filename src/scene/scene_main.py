import pygame

from engine.lib.vect import Vec2i
from engine.lib.tilePos import TilePos, Direction
from engine.scene import Scene, SceneSignal
from engine.resource import resource
from engine.camera import CameraStack
from engine.sprite import Sprite

import setting

from scene.keys import readkey
from module.map import Map
from module.player import Player
from module.map_element import MapElementManage
from module.action import Stage, Action
from creature import enemy_tool as etool
from creature.creature import CreatureGroup


class GameScene(Scene):

    action: Action

    mapClass: Map
    elements: MapElementManage
    '''All the elements'''
    enemies: CreatureGroup
    ''' Enemy Group'''
    player: Player
    movingCount: float

    def init(self):
        resource.add_surface("DungeonTileset", "assets/Dungeon_Tileset.png")
        resource.add_surface("animalsheet", "assets/AnimalsSheet.png")
        resource.scale_surface("animalsheet", setting.ZOOM)

        mapClass = Map()
        mapClass.tilemap_load_resource(resource.surface("DungeonTileset"), 10, 10)
        mapClass.map_generate()
        mapClass.draw_map()
        self.mapClass = mapClass

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

        elements = MapElementManage(camera)
        self.elements = elements
        self.enemies = CreatureGroup()
        elements.add(player)

        self.action = Action(self.surfaceList)
        self.action.player = self.player
        self.action.enemies = self.enemies
        self.action.elements = elements
        self.action.camera = camera
        self.action.mapClass = mapClass

        eList = etool.gen_enemies(mapClass)
        for e in eList:
            self.surfaceList.add(e.sprite)
            self.enemies.add(e)
            elements.add(e)
        elements.checkAllCamera()

        resource.add_surface("ui", "assets/ui.png")
        ui = Sprite(resource.surface("ui"))
        ui.name = "ui"
        ui.zIndex = 10
        ui.set_position(0, 300)
        self.surfaceList.add(ui)
        self.surfaceList.sort()

        # DEBUG
        # self.surfaceList.add(mapClass.tilemap)

    def event_handle(self, event: pygame.event.Event, delta: int):
        if self.action.stage != Stage.IDLE:
            return
        if event.type == pygame.KEYDOWN:
            key = readkey(event)
            if key is None:
                return
            match key:
                case "LEFT":
                    self.action.player_try_move(Direction.LEFT)
                case "RIGHT":
                    self.action.player_try_move(Direction.RIGHT)
                case "UP":
                    self.action.player_try_move(Direction.UP)
                case "DOWN":
                    self.action.player_try_move(Direction.DOWN)
                case "WAIT":
                    self.action.player_wait()

    def process(self, delta: int) -> SceneSignal:
        self.action.process(delta)


gameScene = GameScene()
