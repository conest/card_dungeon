import pygame

keys = {
    "RIGHT": (pygame.K_RIGHT, pygame.K_d),
    "LEFT": (pygame.K_LEFT, pygame.K_a),
    "UP": (pygame.K_UP, pygame.K_w),
    "DOWN": (pygame.K_DOWN, pygame.K_s),
    "WAIT": (pygame.K_SPACE),
    "C": (pygame.K_c),
}


def readkey(event: pygame.event.Event) -> str:
    for keyname, keyValue in keys.items():
        match keyValue:
            case int():
                if event.key == keyValue:
                    return keyname
            case tuple():
                for key in keyValue:
                    if event.key == key:
                        return keyname
    return None
