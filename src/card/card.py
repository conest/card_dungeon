from __future__ import annotations
from enum import Enum, auto

from engine.ui import UIelement


class Catalog(Enum):
    MOVE = auto()
    ITEM = auto()
    EQUIPMENT = auto()


class Card:
    NAME = "Card"

    name: str
    description: str
    catalog: Catalog

    ui: UIelement

    def __init__(self):
        pass

    def use(self):
        pass
