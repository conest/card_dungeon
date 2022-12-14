import pygame

from engine.lib.vect import Vec2i
from engine.lib.tilePos import TilePos, Direction
from engine.scene import Scene, SceneSignal
from engine.resource import resource
from engine.camera import CameraStack

import setting
import asset as ASSET

from scene.keys import readkey
from module.map import Map
from module.player import Player
from module.map_element import MapElementManage
from module.action import Stage, Action
from creature import enemy_tool as etool
from creature.creature import CreatureGroup
from module.ui import UI_play
from card.potion import Potion


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
        resource.add_surface(ASSET.DUNGEON, ASSET.DUNGEON)
        resource.add_surface(ASSET.ANIMALS, ASSET.ANIMALS)
        resource.scale_surface(ASSET.ANIMALS, setting.ZOOM)
        resource.add_font(ASSET.FONT_SMPIX, ASSET.FONT_SMPIX, 8)

        resource.add_surface(ASSET.CARD_POTION, ASSET.CARD_POTION)

        mapClass = Map()
        mapClass.tilemap_load_resource(resource.surface(ASSET.DUNGEON), 10, 10)
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

        ui = UI_play()
        self.surfaceList.add(ui)
        self.surfaceList.sort()

        self.link(player.signals.get("change_attribute"), ui._link_player_change_attribute)
        self.link(player.signals.get("change_hp"), ui._link_hp_change)
        self.link(player.signals.get("get_card"), ui._link_get_card)
        self.link(ui.signals.get("use_card"), player._link_use_card)
        player.emit_change_attribute()

        # Card
        player.get_card(Potion())

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
                case "C":
                    self.player.get_card(Potion())

    def process(self, delta: int) -> SceneSignal:
        self.action.process(delta)


gameScene = GameScene()
