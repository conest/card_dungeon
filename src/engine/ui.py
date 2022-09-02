from __future__ import annotations
import pygame
from .surfaceItem import SurfaceItem


class UIelement(SurfaceItem):
    '''A class to provide relative position and draw function'''
    NAME = "UIelement"
    parent: UIelement
    children: dict[str, UIelement]

    def __init__(self, parent: UIelement = None, s: pygame.Surface = None):
        super().__init__(s)
        self.parent = parent
        self.children = {}

    def add_child(self, name: str, child: UIelement):
        self.children[name] = child

    def draw(self, surface: pygame.Surface):
        '''(@UIelement) Overload SurfaceItem's draw method'''
        if not self.visible:
            return

        draw_pos = self.position
        if self.parent is not None:
            draw_pos = self.parent.position + self.position
        else:
            draw_pos = self.position

        self.draw_custom(surface, draw_pos, self.size)

        if len(self.children) > 0:
            for c in self.children.values():
                c.draw(surface)
