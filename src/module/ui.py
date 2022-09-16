import pygame

from engine.resource import resource
from engine.ui import UIelement
from engine.font import Font_UI
from engine.signal import Signal

from card.card import Card

import asset as ASSET

CARD_PIXEL_SIZE = (45, 65)


class UI_play(UIelement):
    NAME = "UI_play"

    cards: list[Card]
    cardIndex: int
    clicked: bool = False

    def __init__(self):
        super().__init__()
        self.name = UI_play.NAME
        resource.add_surface(ASSET.UI_PLAY, ASSET.UI_PLAY)
        self.load_surface(resource.surface(ASSET.UI_PLAY))
        self.zIndex = 10
        self.set_position(0, 340)

        self.cards = []
        self.cardIndex = 0
        self.signals.sign(Signal("use_card", UI_play.NAME))

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

    def _link_get_card(self, data: list):
        '''data: [card]'''
        [card] = data
        self.add_card(card)

    def add_card(self, card: Card):
        self.cards.append(card)
        self.cardIndex += 1
        name = f'card{str(self.cardIndex)}'
        card.name = name
        card.ui.parent = self
        self.add_child(name, card.ui)
        self.children[name].set_position(371 + 50 * len(self.cards), 25)

    def use_card(self, i: int):
        self.emit_use_card(i)
        del self.children[self.cards[i].name]
        self.cards.pop(i)
        for i, card in enumerate(self.cards):
            self.children[card.name].set_position(421 + 50 * i, 25)

    def emit_use_card(self, index: int):
        self.signals.set_data("use_card", [index])
        self.signals.active("use_card")

    def update(self, _delta: int):
        if (pygame.mouse.get_pressed()[0] == 1 and not self.clicked):
            mousePos = pygame.mouse.get_pos()
            self.clicked = True
            if self.cards == []:
                return
            for i, card in enumerate(self.cards):
                rect = card.ui.rect().move(self.position.x, self.position.y)
                if rect.collidepoint(mousePos):
                    self.use_card(i)

        if (self.clicked and pygame.mouse.get_pressed()[0] == 0):
            self.clicked = False
