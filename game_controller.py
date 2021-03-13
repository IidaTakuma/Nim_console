import random
import curses
from curses import (KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_ENTER)

import config
from view.render import Render

from view.title_scene import TitleScene
# from view.game_scene import GameScene
# from player_agent import PlayerAgent
# from computer_agent import ComputerAgent


class GameController():
    def __init__(self, scene_number=0):
        self.scene_number = scene_number
        self.window = Render.init_cruses(
            config.WINDOW_HEIGHT, config.WINDOW_WIDTH, config.TIMEOUT)
        self.cursor_pos = 0

        self.title_scene = TitleScene()

    def run(self):
        while True:
            self.window.clear()
            self.window.border(0)

            if self.scene_number == 0:
                self.render_title_scene()
            elif self.scene_number == 1:
                pass
                # self.game_scene()
            else:
                Render.close_cruses()
                break
                self.window.refresh()

    def render_title_scene(self):
        self.title_scene.render(self.window)
        event = self.window.getch()

        if event in [KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_ENTER]:
            self.scene_number = self.title_scene.get_key_event(event)

    def game_scene(self):
        pass
