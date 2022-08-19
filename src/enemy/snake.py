import setting
from engine.resource import resource
from module.creature import Creature
from engine.sprite import AnimatedSprite


class Snake(Creature):
    NAME = "Snake"

    def __init__(self, name: str, resourceName: str):
        super().__init__(name, AnimatedSprite(resource.surface(resourceName)))

        self.sprite.set_framesHV(20, 7)
        self._load_animation()

    def _load_animation(self):
        frames: list = [(0, 6, 200), (1, 6, 200), (2, 6, 200), (3, 6, 200)]
        self.sprite.add_and_load_animation("idle", frames, True)
        self.sprite.animation.play("idle")
