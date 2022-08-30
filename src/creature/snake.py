from engine.resource import resource
from engine.sprite import AnimatedSprite
from engine.lib.tilePos import TilePos
from module.map import Map
from creature.kind import Kind
from creature.creature import Creature, Behavior


class Snake(Creature):
    NAME = "Snake"
    KIND = Kind.Snake

    maxHP: int = 10
    hp: int = 10
    atk: int = 15
    defence: int = 5

    def __init__(self, name: str, resourceName: str, m: Map):
        super().__init__(name, AnimatedSprite(resource.surface(resourceName)), m)

        self.kind = Snake.KIND
        self.sprite.set_framesHV(20, 7)
        self._load_animation()

    def _load_animation(self):
        frames: list = [(0, 6, 200), (1, 6, 200), (2, 6, 200), (3, 6, 200)]
        self.sprite.add_and_load_animation("idle", frames, True)
        self.sprite.animation.play("idle")

    def ai(self) -> tuple[Behavior, TilePos]:
        (nextToPlayer, availableMove) = self.check_around()
        behavior = Behavior.IDLE
        tp = None
        if nextToPlayer:
            behavior = Behavior.ATTACK
            tp = nextToPlayer
        else:
            tp = self.random_move()
            behavior = Behavior.MOVE
        return (behavior, tp)
