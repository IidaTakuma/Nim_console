from base.render import Render
import config

TITLE_TOP_Y = 7
TITLE_UNDER_LINE_Y = 13
MENU_TOP_Y = 16
DESCRIPTION_Y = 28


class TitleSceneRender(Render):

    MENUS = [(MENU_TOP_Y, "Player vs Computer",
              "Play NIM with Computer"),
             (MENU_TOP_Y + 2, "Player vs Player",
              "Play NIM with Other Player"),
             (MENU_TOP_Y + 4, "Computer vs Computer",
              "Simulate NIM by Computer"),
             (MENU_TOP_Y + 6, "HELP",
              "This Function is Unimplemented"),
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

    def render(self, selected_menu):
        self.refresh_window()
        self._render_title()
        self._render_menu(selected_menu)
        self._render_selected_menu(selected_menu)

    def _render_title(self):
        for i, line in enumerate(self.TITLE):
            self.window.addstr(
                TITLE_TOP_Y + i, self._calc_center_x_of_text(line), line)
        self.draw_horizintal_line(TITLE_UNDER_LINE_Y, 6, 65)

    def _render_menu(self, selected_menu):
        for i, menu in enumerate(self.MENUS):
            if selected_menu != i:
                self.window.addstr(
                    menu[0], self._calc_center_x_of_text(menu[1]), menu[1])

    def _render_selected_menu(self, selected_menu):
        pos_y = self.MENUS[selected_menu][0]
        menu = self.MENUS[selected_menu][1]
        description = self.MENUS[selected_menu][2]

        # 選ばれたメニューを描画
        selected_text = " -[ " + menu + " ]- "
        self.window.addstr(pos_y, self._calc_center_x_of_text(
            selected_text), selected_text)

        # 説明を描画
        self.window.addstr(DESCRIPTION_Y, self._calc_center_x_of_text(
            description), description)

    def _calc_center_x_of_text(self, text):
        return int(config.WINDOW_WIDTH / 2 - int(len(text) / 2))
