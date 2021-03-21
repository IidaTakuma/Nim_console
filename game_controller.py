import random
import curses
from curses import (KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_ENTER)

import config
from view.render import Render

from view.title_scene import TitleScene
from view.game_scene import GameScene
# from player_agent import PlayerAgent
# from computer_agent import ComputerAgent


class GameController():
    def __init__(self, scene_index=-1):
        self.scene_index = scene_index
        self.window = Render.init_cruses(
            config.WINDOW_HEIGHT, config.WINDOW_WIDTH, config.TIMEOUT)

    def run(self):
        while True:

            if self.scene_index == -1:
                title_scene = TitleScene(self.window)
                title_scene.run()
                self.scene_index = title_scene.selected_menu
            elif self.scene_index == 0:
                game_scene = GameScene(self.window, 0)
                game_scene.run()
                self.scene_index = -1
            elif self.scene_index == 1:
                game_scene = GameScene(self.window, 1)
                game_scene.run()
                self.scene_index = -1
            elif self.scene_index == 3:
                # help
                pass
            elif self.scene_index == 5:
                Render.close_cruses()
                break
            else:
                return

    def close_game(self):
        curses.endwin()
