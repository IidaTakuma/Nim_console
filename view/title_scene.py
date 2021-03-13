import curses
from curses import (KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_ENTER)
import time
import numpy as np

import config

from .render import Render


class TitleScene():

    MENUS = [(15, "Player vs Computer", "You Play NIM with Computer"),
             (17, "Player vs Player", "You Play NIM with Friend"),
             (19, "Computer vs Computer", "Computer ga katteni Game suru"),
             (21, "HELP", "Rule ha Kochira"),
             (23, "EXIT", "Thank you for Playing! ByeBye~")
             ]

    # scale: 5 x 56
    TITLE = [r"  _   _ ___ __  __    ____                      _       ",
             r" | \ | |_ _|  \/  |  / ___|___  _ __  ___  ___ | | ___  ",
             r" |  \| || || |\/| | | |   / _ \| '_ \/ __|/ _ \| |/ _ \ ",
             r" | |\  || || |  | | | |__| (_) | | | \__ \ (_) | |  __/ ",
             r" |_| \_|___|_|  |_|  \____\___/|_| |_|___/\___/|_|\___| ",
             ]

    def __init__(self):
        self.selected_menu = 0

    def render(self, window):
        self._render_title(window)
        self._render_menu(window)
        self._render_selected_menu(window)
        Render.draw_horizintal_line(window, 11, 5, 66)
        Render.draw_horizintal_line(window, 12, 5, 66)

    def get_key_event(self, event):
        if event == KEY_UP:
            if self.selected_menu > 0:
                self.selected_menu -= 1
            return 0
        elif event == KEY_DOWN:
            if self.selected_menu < 4:
                self.selected_menu += 1
            return 0
        elif event == KEY_ENTER:
            return self.selected_menu
        else:
            return 0

    def _render_title(self, window):

        for i, line in enumerate(self.TITLE):
            window.addstr(5 + i, self._calc_center_x_of_text(line), line)

    def _render_menu(self, window):
        for i, menu in enumerate(self.MENUS):
            if self.selected_menu != i:
                window.addstr(
                    menu[0], self._calc_center_x_of_text(menu[1]), menu[1])

    def _render_selected_menu(self, window):
        pos = self.MENUS[self.selected_menu][0]
        text = self.MENUS[self.selected_menu][1]
        description = self.MENUS[self.selected_menu][2]

        # 選ばれた文字を太字で描画する
        selected_text = " -[ " + text + " ]- "
        window.addstr(pos, self._calc_center_x_of_text(
            selected_text), selected_text)

        # 説明を下部に描画する
        window.addstr(27, self._calc_center_x_of_text(
            description), description)

    def _calc_center_x_of_text(self, text):
        return int(config.WINDOW_WIDTH / 2 - int(len(text) / 2))
