#! /usr/bin/env python3
import engine
from scene.scene_main import gameScene
import setting


def main():
    engine.main.init(setting.WINDOW_SIZE, setting.WINDOW_FLAG, setting.WINDOW_CAPTION, vsync=0)
    engine.main.set_fps(setting.FPS)

    gameScene.init()

    engine.main.load_scene(gameScene)
    engine.main.run()


if __name__ == "__main__":
    main()
