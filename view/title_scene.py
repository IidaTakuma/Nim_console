from curses import (KEY_DOWN, KEY_UP, KEY_ENTER)

import config

from .render import Render

TITLE_TOP_Y = 7
TITLE_UNDER_LINE_Y = 13
MENU_TOP_Y = 16
DESCRIPTION_Y = 28


class TitleScene():

    MENUS = [(MENU_TOP_Y, "Player vs Computer",
              "You Play NIM with Computer"),
             (MENU_TOP_Y + 2, "Player vs Player",
              "You Play NIM with Friend"),
             (MENU_TOP_Y + 4, "Computer vs Computer",
              "Computer ga katteni Game suru"),
             (MENU_TOP_Y + 6, "HELP",
              "Rule ha Kochira"),
             (MENU_TOP_Y + 8, "EXIT",
              "Thank you for Playing! ByeBye~")
             ]

    # scale: 5 x 56
    TITLE = [r"  _   _ ___ __  __    ____                      _       ",
             r" | \ | |_ _|  \/  |  / ___|___  _ __  ___  ___ | | ___  ",
             r" |  \| || || |\/| | | |   / _ \| '_ \/ __|/ _ \| |/ _ \ ",
             r" | |\  || || |  | | | |__| (_) | | | \__ \ (_) | |  __/ ",
             r" |_| \_|___|_|  |_|  \____\___/|_| |_|___/\___/|_|\___| ",
             ]

    def __init__(self, window):
        self.selected_menu = 0
        self.window = window

    def run(self):
        while True:
            event = self.window.getch()
            if event in [KEY_DOWN, KEY_UP, KEY_ENTER]:
                scene_index = self.get_key_event(event)
                if scene_index != -1:
                    break
            self.render()

    def get_key_event(self, event):
        if event == KEY_UP:
            if self.selected_menu > 0:
                self.selected_menu -= 1
            return -1
        elif event == KEY_DOWN:
            if self.selected_menu < 4:
                self.selected_menu += 1
            return -1
        elif event == KEY_ENTER:
            return self.selected_menu
        else:
            return -1

    def render(self):
        Render.refresh_window(self.window)
        self._render_title()
        self._render_menu()
        self._render_selected_menu()

    def _render_title(self):

        for i, line in enumerate(self.TITLE):
            self.window.addstr(
                TITLE_TOP_Y + i, self._calc_center_x_of_text(line), line)

        Render.draw_horizintal_line(self.window, TITLE_UNDER_LINE_Y, 6, 65)

    def _render_menu(self):
        for i, menu in enumerate(self.MENUS):
            if self.selected_menu != i:
                self.window.addstr(
                    menu[0], self._calc_center_x_of_text(menu[1]), menu[1])

    def _render_selected_menu(self):
        pos = self.MENUS[self.selected_menu][0]
        text = self.MENUS[self.selected_menu][1]
        description = self.MENUS[self.selected_menu][2]

        # 選ばれた文字を太字で描画する
        selected_text = " -[ " + text + " ]- "
        self.window.addstr(pos, self._calc_center_x_of_text(
            selected_text), selected_text)

        # 説明を下部に描画する
        self.window.addstr(DESCRIPTION_Y, self._calc_center_x_of_text(
            description), description)

    def _calc_center_x_of_text(self, text):
        return int(config.WINDOW_WIDTH / 2 - int(len(text) / 2))
