import pygame

keys = {
    "RIGHT": (pygame.K_RIGHT, pygame.K_d),
    "LEFT": (pygame.K_LEFT, pygame.K_a),
    "UP": (pygame.K_UP, pygame.K_w),
    "DOWN": (pygame.K_DOWN, pygame.K_s),
}


def readkey(event: pygame.event.Event) -> str:
    for keyname, keytuple in keys.items():
        for key in keytuple:
            if event.key == key:
                return keyname
    return None
