import pygame

from engine.scene import Scene, SceneSignal
from engine.resource import resource
from engine.sprite import Sprite
from engine.surfaceItem import SurfaceItem
from engine.font import Font

import setting


class UI_play(SurfaceItem):
    NAME = "UI_play"
    font_hp: Font
    font_atk: Font
    font_def: Font

    def __init__(self):
        super().__init__()
        resource.add_surface(setting.ASSERT_UI_PLAY, setting.ASSERT_UI_PLAY)
        self.load_surface(resource.surface(setting.ASSERT_UI_PLAY))
        self.name = UI_play.NAME
        self.zIndex = 10
        self.set_position(0, 340)

        self.font_hp = Font(resource.font(setting.ASSERT_FONT_SMPIX))
        self.font_hp.set_string("-")
        self.font_hp.set_position(113, 67)
        self.font_atk = Font(resource.font(setting.ASSERT_FONT_SMPIX))
        self.font_atk.set_string("-")
        self.font_atk.set_position(150, 67)
        self.font_def = Font(resource.font(setting.ASSERT_FONT_SMPIX))
        self.font_def.set_string("-")
        self.font_def.set_position(187, 67)

    def draw(self, surface: pygame.Surface):
        '''(@UI_play) Overload SurfaceItem's draw method'''
        if self.visible:
            surface.blit(self.surface, self.position.to_tuple_int())
            self.draw_fonts(surface)

    def draw_fonts(self, surface: pygame.Surface):
        self.font_hp.draw_to(surface, self.font_hp.position + self.position)
        self.font_atk.draw_to(surface, self.font_atk.position + self.position)
        self.font_def.draw_to(surface, self.font_def.position + self.position)

    def _link_player_change_attribute(self, data: list):
        self.font_hp.set_string(str(data[0]))
        self.font_atk.set_string(str(data[1]))
        self.font_def.set_string(str(data[2]))
