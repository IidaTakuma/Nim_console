import curses
import numpy as np


class Render():

    @classmethod
    def init_cruses(cls, height, width, timeout):
        curses.initscr()
        window = curses.newwin(height, width, 0, 0)
        window.timeout(timeout)  # getch()の受付時間
        window.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        window.border(0)  # windowの周りに線を描画
        return window

    @classmethod
    def close_cruses(cls):
        curses.echo()
        curses.endwin()

    def refresh_window(self, window):
        window.clear()
        window.border(0)

    def _draw_window_flame(self, window, height, width):
        self.draw_rectangle(window, 0, 0, height - 1, width - 1)

    def draw_rectangle(self, window, start_y, start_x, end_y, end_x,
                       v_chr="|", h_chr="-", c_chr="+"):
        self.draw_vertical_line(
            window, start_x, start_y, end_y, v_chr)
        self.draw_vertical_line(
            window, end_x, start_y, end_y, v_chr)
        self.draw_horizintal_line(
            window, start_y, start_x, end_x, h_chr)
        self.draw_horizintal_line(
            window, end_y, start_x, end_x, h_chr)

        window.addstr(start_y, start_x, c_chr)
        window.addstr(start_y, end_x, c_chr)
        window.addstr(end_y, start_x, c_chr)
        window.addstr(end_y, end_x, c_chr)

    def draw_horizintal_line(self, window, y, start_x, end_x, chr='-', fin='+'):
        for x in range(start_x, end_x):
            window.addstr(y, x, chr)

        window.addstr(y, start_x, fin)
        window.addstr(y, end_x, fin)

    def draw_vertical_line(self, window, x, start_y, end_y, chr='|', fin='+'):
        for y in range(start_y, end_y):
            window.addstr(y, x, chr)

        window.addstr(start_y, x, fin)
        window.addstr(end_y, x, fin)

    def draw_matrix(self, window, matrix, bottom_y, left_x):
        # matrixを描画
        for y in range(matrix.shape[1]):
            for x in range(matrix.shape[0]):
                if matrix[x][y] == 1:
                    window.addstr(bottom_y - y, left_x + 2 * x, "■")
                else:
                    window.addstr(bottom_y - y, left_x + 2 * x, "□")
