from engine.resource import resource
from engine.ui import UIelement
from engine.font import Font_UI

import asset as ASSET


class UI_play(UIelement):
    NAME = "UI_play"

    def __init__(self):
        super().__init__()
        self.name = UI_play.NAME
        resource.add_surface(ASSET.UI_PLAY, ASSET.UI_PLAY)
        self.load_surface(resource.surface(ASSET.UI_PLAY))
        self.zIndex = 10
        self.set_position(0, 340)

        resource.add_surface(ASSET.HP_BAR, ASSET.HP_BAR)
        self.add_child("hp_bar", UIelement(self, resource.surface(ASSET.HP_BAR)))
        self.children["hp_bar"].set_position(98, 37)

        self.add_child("font_hp", Font_UI(resource.font(ASSET.FONT_SMPIX), self))
        self.children["font_hp"].set_position(160, 37)
        self.children["font_hp"].set_string("50 / 50")

        self.add_child("font_maxhp", Font_UI(resource.font(ASSET.FONT_SMPIX), self))
        self.children["font_maxhp"].set_position(113, 67)
        self.add_child("font_atk", Font_UI(resource.font(ASSET.FONT_SMPIX), self))
        self.children["font_atk"].set_position(150, 67)
        self.add_child("font_def", Font_UI(resource.font(ASSET.FONT_SMPIX), self))
        self.children["font_def"].set_position(187, 67)

        self.add_child("card_font", Font_UI(resource.font(ASSET.FONT_SMPIX), self))
        self.children["card_font"].set_string("Sword")
        self.children["card_font"].set_position(428, 31)

    def _link_player_change_attribute(self, data: list):
        '''data: [hp, atk, def]'''
        self.children["font_maxhp"].set_string(str(data[0]))
        self.children["font_atk"].set_string(str(data[1]))
        self.children["font_def"].set_string(str(data[2]))

    def _link_hp_change(self, data: list):
        '''data: [hp, maxHp]'''
        [hp, maxHp] = data
        self.children["font_hp"].set_string(f'{hp} / {maxHp}')
        self.children["hp_bar"].size.w = hp / maxHp * resource.surface(ASSET.HP_BAR).get_width()
