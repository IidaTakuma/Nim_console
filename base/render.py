import curses


class Render():

    def __init__(self, window):
        self.window = window

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

    def refresh_window(self):
        self.window.clear()
        self.window.border(0)

    def draw_window_flame(self, height, width):
        self.draw_rectangle(0, height - 1, 0, width - 1)

    def draw_rectangle(self, start_y, end_y, start_x, end_x,
                       v_chr="|", h_chr="-", c_chr="+"):
        self.draw_vertical_line(
            start_x, start_y, end_y, v_chr)
        self.draw_vertical_line(
            end_x, start_y, end_y, v_chr)
        self.draw_horizintal_line(
            start_y, start_x, end_x, h_chr)
        self.draw_horizintal_line(
            end_y, start_x, end_x, h_chr)

        self.window.addstr(start_y, start_x, c_chr)
        self.window.addstr(start_y, end_x, c_chr)
        self.window.addstr(end_y, start_x, c_chr)
        self.window.addstr(end_y, end_x, c_chr)

    def draw_horizintal_line(self, y, start_x, end_x, chr='-', fin='+'):
        for x in range(start_x, end_x):
            self.window.addstr(y, x, chr)

        self.window.addstr(y, start_x, fin)
        self.window.addstr(y, end_x, fin)

    def draw_vertical_line(self, x, start_y, end_y, chr='|', fin='+'):
        for y in range(start_y, end_y):
            self.window.addstr(y, x, chr)

        self.window.addstr(start_y, x, fin)
        self.window.addstr(end_y, x, fin)

    def draw_matrix(self, matrix, bottom_y, left_x):
        # matrixを描画
        for y in range(matrix.shape[1]):
            for x in range(matrix.shape[0]):
                if matrix[x][y] == 1:
                    self.window.addstr(bottom_y - y, left_x + 2 * x, "■")
                else:
                    self.window.addstr(bottom_y - y, left_x + 2 * x, "□")
