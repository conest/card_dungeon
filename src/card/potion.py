from engine.ui import UIelement
from engine.resource import resource

from card.card import Card, Catalog
import asset as ASSET


class Potion(Card):

    def __init__(self):
        self.name = "potion"
        self.description = "Restore 20 HP immediately"
        self.catalog = Catalog.ITEM
        self.ui = UIelement()
        self.ui.load_surface(resource.surface(ASSET.CARD_POTION))

    def use(self):
        print("use a potion")
