from engine.resource import resource
from creature.creature import Creature
from engine.sprite import AnimatedSprite
from module.map import Map
from creature.kind import Kind


class Snake(Creature):
    NAME = "Snake"
    KIND = Kind.Snake

    def __init__(self, name: str, resourceName: str, m: Map):
        super().__init__(name, AnimatedSprite(resource.surface(resourceName)), m)

        self.kind = Snake.KIND
        self.sprite.set_framesHV(20, 7)
        self._load_animation()

    def _load_animation(self):
        frames: list = [(0, 6, 200), (1, 6, 200), (2, 6, 200), (3, 6, 200)]
        self.sprite.add_and_load_animation("idle", frames, True)
        self.sprite.animation.play("idle")

    def ai(self):
        (nextToPlayer, availableMove) = self.check_around()
        if nextToPlayer:
            print(f'{self.name} -> melee attack')
        else:
            self.random_move()
