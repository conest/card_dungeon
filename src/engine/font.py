import pygame
from .surfaceItem import SurfaceItem
from .ui import UIelement


class Font(SurfaceItem):
    font: pygame.font.Font

    def __init__(self, font: pygame.font.Font):
        super().__init__()
        self.name = "Font"
        self.font = font

    def set_string(self, string: str, color: tuple = (0, 0, 0)):
        ns = self.font.render(string, False, color)
        self.load_surface(ns)


class Font_UI(UIelement):
    font: pygame.font.Font

    def __init__(self, font: pygame.font.Font, parent: UIelement = None):
        super().__init__(parent)
        self.name = "Font_UI"
        self.font = font

    def set_string(self, string: str, color: tuple = (0, 0, 0)):
        ns = self.font.render(string, False, color)
        self.load_surface(ns)
