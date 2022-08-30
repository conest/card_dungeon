import pygame

WINDOW_SIZE = (800, 450)
# WINDOW_SIZE = (800, 800)

WINDOW_FLAG = pygame.RESIZABLE
WINDOW_FLAG = pygame.RESIZABLE | pygame.SCALED
WINDOW_CAPTION = "Card Dungeon"

FPS = 30
ZOOM = 2

MAP_SIZE_X = 40
MAP_SIZE_Y = 40
TILE_PIXEL = 16
TILE_PIXEL_ZOOMED = ZOOM * TILE_PIXEL

ASSERT_DUNGEON = "assets/Dungeon_Tileset.png"
ASSERT_UI_PLAY = "assets/ui.png"
ASSERT_PLAYER = "assets/Dwarves.png"
ASSERT_ANIMALS = "assets/AnimalsSheet.png"

ASSERT_FONT_SMPIX = "assets/small_pixel.ttf"