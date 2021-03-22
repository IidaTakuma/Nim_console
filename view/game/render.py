from config import (WINDOW_HEIGHT, WINDOW_WIDTH)
from view.game.constant import (
    PILE_COUNT, STONE_MAX,
    HALF_LINE_TOP_Y, HALF_LINE_BOTTOM_Y, HALF_LINE_X,
    TEXT_BOX_TOP_Y, TEXT_BOX_BOTTOM_Y, TEXT_BOX_LEFT_X, TEXT_BOX_RIGHT_X,
    FIELD_TOP_Y, FIELD_BOTTOM_Y, FIELD_LEFT_X, FIELD_RIGHT_X,
    PILE_LINE_Y, PILE_LINE_LEFT_X, PILE_LINE_RIGHT_X,
    PILE_NUMBER_Y, PILE_NUMBER_LEFT_X, PILE_NUMBER_RIGHT_X,
    SCALE_LINE_TOP_Y, SCALE_LINE_BOTTOM_Y, SCALE_LINE_X,
    SCALE_NUMBER_TOP_Y, SCALE_NUMBER_BOTTOM_Y, SCALE_NUMBER_X,
    MATRIX_TOP_Y, MATRIX_BOTTOM_Y, MATRIX_LEFT_X, MATRIX_RIGHT_X,
    GAMELOG_BOX_TOP_Y, GAMELOG_BOX_BOTTOM_Y, GAMELOG_BOX_LEFT_X, GAMELOG_BOX_RIGHT_X,
    GAMELOG_TEXT_TOP_Y, GAMELOG_TEXT_BOTTOM_Y, GAMELOG_TEXT_LEFT_X, GAMELOG_TEXT_RIGHT_X,
    CAUTION_BOX_TOP_Y, CAUTION_BOX_BOTTOM_Y, CAUTION_BOX_LEFT_X, CAUTION_BOX_RIGHT_X
)

import numpy as np
from base.render import Render


class GameSceneRender(Render):

    def render(self, turn_player, turn_player_index, text, game_log,
               pile_cursor_pos_x, scale_cursor_pos_y, caution, fields):
        self.refresh_window()
        self._render_flame()
        self._render_field()
        self._render_textbox(turn_player, turn_player_index, text)
        self._render_game_log(game_log)
        self._render_cursor(pile_cursor_pos_x, scale_cursor_pos_y)
        self._render_caution(caution)
        self._render_game_log(game_log)
        self._render_matrix(fields)

    def _render_flame(self):
        # 画面全体を縦に二分する線
        self.draw_vertical_line(
            HALF_LINE_X,
            HALF_LINE_TOP_Y, HALF_LINE_BOTTOM_Y - 1)

    def _render_field(self):
        # 盤面の枠線
        self.draw_rectangle(
            FIELD_TOP_Y, FIELD_BOTTOM_Y,
            FIELD_LEFT_X, FIELD_RIGHT_X)
        # 左の目盛りの線
        self.draw_vertical_line(
            SCALE_LINE_X,
            SCALE_LINE_TOP_Y, SCALE_LINE_BOTTOM_Y,
            chr="|", fin="|")

        # 盤面 -> 左の目盛り
        for i in range(0, 20):
            self.window.addstr(SCALE_NUMBER_BOTTOM_Y - i - 1,
                               SCALE_NUMBER_X, str(i + 1))

        # 下の番号の線
        self.draw_horizintal_line(
            PILE_LINE_Y,
            PILE_LINE_LEFT_X, PILE_LINE_RIGHT_X)

        # 盤面 -> 下の番号
        for i in range(0, 8):
            self.window.addstr(PILE_NUMBER_Y,
                               PILE_NUMBER_LEFT_X + i * 2, str(i))

    def _render_textbox(self, turn_player, turn_player_index, text):
        # テキストボックスの枠線
        self.draw_rectangle(
            TEXT_BOX_TOP_Y, TEXT_BOX_BOTTOM_Y,
            TEXT_BOX_LEFT_X, TEXT_BOX_RIGHT_X)
        # テキストを描画
        self.window.addstr(TEXT_BOX_TOP_Y + 1,
                           TEXT_BOX_LEFT_X + 1,
                           "Player{}".format(
                               turn_player_index + 1))

        self.window.addstr(TEXT_BOX_TOP_Y + 2,
                           TEXT_BOX_LEFT_X + 1,
                           text)

    def _render_game_log(self, game_log):
        # ログの枠線
        self.draw_rectangle(
            GAMELOG_BOX_TOP_Y, GAMELOG_BOX_BOTTOM_Y,
            GAMELOG_BOX_LEFT_X, GAMELOG_BOX_RIGHT_X)
        cnt = 0
        for i in range(len(game_log)):
            if len(game_log) - i < 10:
                self.window.addstr(GAMELOG_TEXT_TOP_Y + cnt * 3,
                                   GAMELOG_TEXT_LEFT_X,
                                   game_log[i][0])
                self.window.addstr(GAMELOG_TEXT_TOP_Y + cnt * 3 + 1,
                                   GAMELOG_TEXT_LEFT_X,
                                   game_log[i][1])
                self.window.addstr(GAMELOG_TEXT_TOP_Y + cnt * 3 + 2,
                                   GAMELOG_TEXT_LEFT_X,
                                   "---------------")
                cnt += 1

    def _render_cursor(self, pile_cursor_pos_x, scale_cursor_pos_y):
        self.window.addstr(PILE_NUMBER_Y + 1, pile_cursor_pos_x, "^")
        self.window.addstr(scale_cursor_pos_y, SCALE_NUMBER_X - 1, ">")

    def _render_matrix(self, fields):
        # 盤面 -> 石の描画
        matrix = self._generate_matrix_from_fields(fields)
        self.draw_matrix(
            matrix,
            MATRIX_BOTTOM_Y, MATRIX_LEFT_X)

    def _render_caution(self, caution):
        if caution == "":
            return
        # 警告ボックスの枠線
        self.draw_rectangle(
            CAUTION_BOX_TOP_Y, CAUTION_BOX_BOTTOM_Y,
            CAUTION_BOX_LEFT_X, CAUTION_BOX_RIGHT_X)

        self.window.addstr(CAUTION_BOX_TOP_Y + 1,
                           CAUTION_BOX_LEFT_X + 1,
                           caution)

    def _generate_matrix_from_fields(self, fields):
        matrix = np.zeros((PILE_COUNT, STONE_MAX))
        for i in range(STONE_MAX):
            for p in range(PILE_COUNT):
                if fields[p] > i:
                    matrix[p][i] = 1

        return matrix
