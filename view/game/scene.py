from agent.computer_agent import ComputerAgent
from agent.player_agent import PlayerAgent
import random
from curses import (KEY_DOWN, KEY_UP, KEY_LEFT,
                    KEY_RIGHT, KEY_ENTER, KEY_F1)
import numpy as np

import config
from base.render import Render

PILE_COUNT = 8  # 山の個数
STONE_MAX = 20  # 山ごとの石の個数の上限

# 枠組みの座標
HALF_LINE_X = 35
HALF_LINE_TOP_Y = 1
HALF_LINE_BOTTOM_Y = config.WINDOW_HEIGHT - 4

# テキストボックスの座標
TEXT_BOX_TOP_Y = 28
TEXT_BOX_BOTTOM_Y = 31
TEXT_BOX_LEFT_X = 3
TEXT_BOX_RIGHT_X = 32

# 警告の枠の座標
CAUTION_BOX_TOP_Y = 32
CAUTION_BOX_BOTTOM_Y = 34
CAUTION_BOX_LEFT_X = 3
CAUTION_BOX_RIGHT_X = 68

# 盤面の座標
FIELD_TOP_Y = 2
FIELD_BOTTOM_Y = 27
FIELD_LEFT_X = 3
FIELD_RIGHT_X = 32

# 盤面 -> 下の線の座標
PILE_LINE_Y = FIELD_BOTTOM_Y - 3
PILE_LINE_LEFT_X = FIELD_LEFT_X + 2
PILE_LINE_RIGHT_X = FIELD_RIGHT_X - 2

# 盤面 -> 下の番号の座標
PILE_NUMBER_Y = FIELD_BOTTOM_Y - 2
PILE_NUMBER_LEFT_X = FIELD_LEFT_X + 9
PILE_NUMBER_RIGHT_X = PILE_NUMBER_LEFT_X + 2 * PILE_COUNT

# 盤面 -> 目盛りの線の座標
SCALE_LINE_TOP_Y = FIELD_TOP_Y + 2
SCALE_LINE_BOTTOM_Y = SCALE_LINE_TOP_Y + STONE_MAX
SCALE_LINE_X = FIELD_LEFT_X + 5

# 盤面 -> 目盛りの番号の座標
SCALE_NUMBER_TOP_Y = FIELD_TOP_Y + 2
SCALE_NUMBER_BOTTOM_Y = SCALE_NUMBER_TOP_Y + STONE_MAX
SCALE_NUMBER_X = FIELD_LEFT_X + 3

# 盤面 -> 石のmatrixの座標
MATRIX_TOP_Y = 4
MATRIX_BOTTOM_Y = 23
MATRIX_LEFT_X = 12
MATRIX_RIGHT_X = 26

# ゲームログの枠の座標
GAMELOG_BOX_TOP_Y = 2
GAMELOG_BOX_BOTTOM_Y = 31
GAMELOG_BOX_LEFT_X = 38
GAMELOG_BOX_RIGHT_X = 68

# ゲームログのテキストの座標
GAMELOG_TEXT_TOP_Y = GAMELOG_BOX_TOP_Y + 2
GAMELOG_TEXT_BOTTOM_Y = GAMELOG_BOX_BOTTOM_Y - 2
GAMELOG_TEXT_LEFT_X = GAMELOG_BOX_LEFT_X + 2
GAMELOG_TEXT_RIGHT_X = GAMELOG_BOX_RIGHT_X - 2

# カーソル初期値
DEFAULT_PILE_SELECT_CURSOR_X = PILE_NUMBER_LEFT_X
DEFAULT_PILE_SELECT_CURSOR_Y = SCALE_NUMBER_BOTTOM_Y + 1


class GameScene():
    def __init__(self, window, start_player=0):
        self.window = window
        self.game_log = []
        self.text = ""
        self.caution = ""
        self.agents = []
        self.start_player = start_player - 1
        self.fields = self._generate_field()
        self.round = 0
        self.pile_cursor_pos_x = DEFAULT_PILE_SELECT_CURSOR_X
        self.scale_cursor_pos_y = DEFAULT_PILE_SELECT_CURSOR_Y - 2
        self.game_active = True

    def regist_player_vs_player(self) -> None:
        self.agents.append(PlayerAgent())
        self.agents.append(PlayerAgent())

    def regist_player_vs_computer(self) -> None:
        self.agents.append(PlayerAgent())
        self.agents.append(ComputerAgent())

    def regist_computer_vs_computer(self) -> None:
        self.agents.append(ComputerAgent())
        self.agents.append(ComputerAgent())

    def _generate_field(self) -> np.array:
        fields = np.zeros(PILE_COUNT)
        for i in range(PILE_COUNT):
            fields[i] = random.randrange(1, 21)
        return fields

    def run(self):
        while True:
            if self.game_active:
                agent_idx = (self.round + self.start_player) % 2
                if type(self.agents[agent_idx]) is PlayerAgent:
                    self._run_player_turn()
                elif type(self.agents[agent_idx]) is ComputerAgent:
                    self._run_computer_turn()
                else:
                    break
            else:
                event = self.window.getch()
                if event == KEY_F1:
                    break
            self.render()

    def _run_player_turn(self):
        turn_player_index = (self.round + self.start_player) % 2
        turn_player = self.agents[turn_player_index]

        if turn_player.scene == 0:  # 山を選択するフェーズ
            self.text = "Please Select Pile."
            event = self.window.getch()
            if event in [KEY_LEFT, KEY_RIGHT, KEY_ENTER]:
                if event == KEY_LEFT:
                    self._cursor_move_left()
                elif event == KEY_RIGHT:
                    self._cursor_move_right()
                elif event == KEY_ENTER:
                    self._select_pile()
        elif turn_player.scene == 1:  # 石の個数を選択するフェーズ
            self.text = "Please Select Stone."
            event = self.window.getch()
            if event in [KEY_UP, KEY_DOWN, KEY_ENTER]:
                if event == KEY_UP:
                    self._cursor_move_up()
                elif event == KEY_DOWN:
                    self._cursor_move_down()
                elif event == KEY_ENTER:
                    self._select_stone_quantity()
            if self._field_stone_not_remained():  # 勝利判定
                self.game_active = False
                self.game_log.append(("Player{} WIN !!".format(
                    turn_player_index + 1),
                    "PRESS F1 Key to Back Main Menu"))

        elif turn_player.scene == 2:  # ターンを進行する
            self.agents[turn_player_index].scene = 0
            self.round += 1

    def _run_computer_turn(self):
        turn_player_index = (self.round + self.start_player) % 2
        turn_player = self.agents[turn_player_index]

        after_action = turn_player.action(self.fields)
        validated_data = self._validated_computer_action(after_action)
        if validated_data[0]:
            selected_pile = validated_data[1]
            get_stone_cnt = validated_data[2]
            self.game_log.append(("Computer{}".format(turn_player_index + 1),
                                  "Get {}stone from No.{}pile.".format(
                get_stone_cnt,
                selected_pile
            )))
            self.fields[selected_pile] -= get_stone_cnt
            if self._field_stone_not_remained():
                self.game_active = False
                self.game_log.append(("Computer{} WIN !!".format(
                    turn_player_index + 1),
                    "PRESS F1 Key to Back Main Menu"))
        else:
            self.game_log.append(
                ("ERROR OCCURED IN", "COMPUTER ACTION VALIDATION"))
        self.round += 1

    def _validated_computer_action(self, after_action):
        change_flag = False
        change_pile = -1
        change_stone_cnt = -1

        for i in range(len(after_action)):
            if self.fields[i] != after_action[i]:
                if change_flag:
                    return (False, -1, -1)
                else:
                    change_flag = True
                    change_pile = i
                    change_stone_cnt = self.fields[i] - after_action[i]
        return (change_flag, change_pile, change_stone_cnt)


# カーソルの移動処理を確認する

    # 山を選択する際に用いるカーソル移動関数

    def _cursor_move_left(self):
        if self.pile_cursor_pos_x > PILE_NUMBER_LEFT_X:
            self.pile_cursor_pos_x -= 2

    def _cursor_move_right(self):
        if self.pile_cursor_pos_x < PILE_NUMBER_RIGHT_X - 2:
            self.pile_cursor_pos_x += 2

    def _select_pile(self):
        validate_message = self._validate_select_plie()
        if validate_message[0]:
            turn_player_index = (self.round + self.start_player) % 2
            self.agents[turn_player_index].scene = 1
            self.agents[turn_player_index].selected_pile = (
                self.pile_cursor_pos_x - PILE_NUMBER_LEFT_X) // 2
        else:
            self.caution = validate_message[1]

    def _validate_select_plie(self):
        if PILE_NUMBER_LEFT_X <= self.pile_cursor_pos_x <= PILE_NUMBER_RIGHT_X:
            pile_idx = (self.pile_cursor_pos_x - PILE_NUMBER_LEFT_X) // 2
            if self.fields[pile_idx] > 0:
                return (True, "OK")
            else:
                return (False, "Please Select Pile that Remain the Stone.")
        else:
            return (False, "[Error]Select Pile Number is Out of Range")

    # 石の個数を選択する際に用いるカーソル移動関数
    def _cursor_move_up(self):
        if self.scale_cursor_pos_y > SCALE_NUMBER_TOP_Y:
            self.scale_cursor_pos_y -= 1

    def _cursor_move_down(self):
        if self.scale_cursor_pos_y < SCALE_NUMBER_BOTTOM_Y - 1:
            self.scale_cursor_pos_y += 1

    def _select_stone_quantity(self):
        validate_message = self._validate_select_stone()
        if validate_message[0]:
            turn_player_index = (self.round + self.start_player) % 2
            turn_player_number = turn_player_index + 1
            pile_index = self.agents[turn_player_index].selected_pile
            stone_index = SCALE_NUMBER_BOTTOM_Y - self.scale_cursor_pos_y - 1
            get_stone_cnt = self.fields[pile_index] - stone_index
            self.game_log.append(("Player{}".format(turn_player_number),
                                  "Get {}stone from No.{}pile.".format(
                get_stone_cnt,
                pile_index
            )))
            self.fields[pile_index] -= get_stone_cnt
            self.agents[(self.round + self.start_player) % 2].scene = 2
        else:
            self.caution = validate_message[1]

    def _validate_select_stone(self) -> (bool, str):
        if SCALE_NUMBER_TOP_Y <= self.scale_cursor_pos_y <= SCALE_NUMBER_BOTTOM_Y:
            pile_idx = self.agents[(self.round +
                                    self.start_player) % 2].selected_pile
            stone_index = SCALE_NUMBER_BOTTOM_Y - self.scale_cursor_pos_y
            if stone_index <= self.fields[pile_idx]:
                return (True, "OK")
            else:
                return (False, "Please Select Number You Can Get at Least 1")
        return (False, "[Error]Select Count is Out of Range")

    # 勝利判定
    def _field_stone_not_remained(self):
        if np.all(self.fields == 0):
            return True
        return False

    def _regist_player(self, mode):
        if mode == 0:
            self.agents.append(PlayerAgent())
            self.agents.append(ComputerAgent())
        elif mode == 1:
            self.agents.append(PlayerAgent())
            self.agents.append(PlayerAgent())
        elif mode == 2:
            self.agents.append(ComputerAgent())
            self.agents.append(ComputerAgent())

    def render(self):
        Render.refresh_window(self.window)
        Render.draw_vertical_line(
            self.window,
            HALF_LINE_X,
            HALF_LINE_TOP_Y, HALF_LINE_BOTTOM_Y - 1
        )  # 画面全体を縦に二分する線
        Render.draw_rectangle(
            self.window,
            FIELD_TOP_Y, FIELD_LEFT_X,
            FIELD_BOTTOM_Y, FIELD_RIGHT_X
        )  # 盤面の枠線
        Render.draw_vertical_line(
            self.window,
            SCALE_LINE_X,
            SCALE_LINE_TOP_Y, SCALE_LINE_BOTTOM_Y,
            chr="|", fin="|"
        )  # 盤面 -> 左の目盛りの線
        Render.draw_horizintal_line(
            self.window,
            PILE_LINE_Y,
            PILE_LINE_LEFT_X, PILE_LINE_RIGHT_X
        )  # 盤面 -> 下の番号の線
        Render.draw_rectangle(
            self.window,
            TEXT_BOX_TOP_Y, TEXT_BOX_LEFT_X,
            TEXT_BOX_BOTTOM_Y, TEXT_BOX_RIGHT_X
        )  # テキストボックスの枠線

        self.window.addstr(TEXT_BOX_TOP_Y + 1,
                           TEXT_BOX_LEFT_X + 1,
                           "Player{}".format(
                               (self.round + self.start_player) % 2
                           ))
        self.window.addstr(TEXT_BOX_TOP_Y + 2,
                           TEXT_BOX_LEFT_X + 1,
                           self.text)

        Render.draw_rectangle(
            self.window,
            GAMELOG_BOX_TOP_Y,
            GAMELOG_BOX_LEFT_X,
            GAMELOG_BOX_BOTTOM_Y,
            GAMELOG_BOX_RIGHT_X
        )  # ログの枠線

        for i in range(0, 8):  # 盤面 -> 下の番号
            self.window.addstr(PILE_NUMBER_Y,
                               PILE_NUMBER_LEFT_X + i * 2, str(i))

        self.window.addstr(PILE_NUMBER_Y + 1,
                           self.pile_cursor_pos_x, "^")

        for i in range(0, 20):  # 盤面 -> 左の目盛り
            self.window.addstr(SCALE_NUMBER_BOTTOM_Y - i - 1,
                               SCALE_NUMBER_X, str(i + 1))

        self.window.addstr(self.scale_cursor_pos_y,
                           SCALE_NUMBER_X - 1, ">")

        matrix = self._generate_matrix_from_field()
        Render.draw_matrix(
            self.window, matrix,
            MATRIX_BOTTOM_Y, MATRIX_LEFT_X
        )  # 盤面 -> 石の描画

        Render.draw_rectangle(
            self.window,
            CAUTION_BOX_TOP_Y, CAUTION_BOX_LEFT_X,
            CAUTION_BOX_BOTTOM_Y, CAUTION_BOX_RIGHT_X
        )  # 警告ボックスの枠線

        self.window.addstr(CAUTION_BOX_TOP_Y + 1,
                           CAUTION_BOX_LEFT_X + 1,
                           self.caution
                           )

        self._render_log()

    def _render_log(self):
        cnt = 0
        for i in range(len(self.game_log)):
            if len(self.game_log) - i < 14:
                self.window.addstr(GAMELOG_TEXT_TOP_Y + cnt * 2,
                                   GAMELOG_TEXT_LEFT_X,
                                   self.game_log[i][0])
                self.window.addstr(GAMELOG_TEXT_TOP_Y + cnt * 2 + 1,
                                   GAMELOG_TEXT_LEFT_X,
                                   self.game_log[i][1])
                cnt += 1

    def _generate_matrix_from_field(self):
        matrix = np.zeros((PILE_COUNT, STONE_MAX))
        for i in range(STONE_MAX):
            for p in range(PILE_COUNT):
                if self.fields[p] > i:
                    matrix[p][i] = 1

        return matrix


# 以下テスト用クラス =================================================
class TestGameScene():
    def __init__(self):
        pass

    def run(self):
        # 枠組みの座標
        assert 0 < HALF_LINE_X < config.WINDOW_WIDTH - 1
        assert 0 < HALF_LINE_TOP_Y < config.WINDOW_HEIGHT - 1
        assert 0 < HALF_LINE_BOTTOM_Y < config.WINDOW_HEIGHT - 1

        # テキストボックスの座標
        assert 0 < TEXT_BOX_TOP_Y < config.WINDOW_HEIGHT - 1
        assert 0 < TEXT_BOX_BOTTOM_Y < config.WINDOW_HEIGHT - 1
        assert 0 < TEXT_BOX_LEFT_X < config.WINDOW_WIDTH - 1
        assert 0 < TEXT_BOX_RIGHT_X < config.WINDOW_WIDTH - 1

        # 盤面の座標
        assert 0 < FIELD_TOP_Y < config.WINDOW_HEIGHT - 1
        assert 0 < FIELD_BOTTOM_Y < config.WINDOW_HEIGHT - 1
        assert 0 < FIELD_LEFT_X < config.WINDOW_WIDTH - 1
        assert 0 < FIELD_RIGHT_X < config.WINDOW_WIDTH - 1

        # 盤面 -> 下の線の座標
        assert 0 < PILE_LINE_Y < config.WINDOW_HEIGHT - 1
        assert 0 < PILE_LINE_LEFT_X < config.WINDOW_WIDTH - 1
        assert 0 < PILE_LINE_RIGHT_X < config.WINDOW_WIDTH - 1

        # 盤面 -> 下の番号の座標
        assert 0 < PILE_NUMBER_Y < config.WINDOW_HEIGHT - 1
        assert 0 < PILE_NUMBER_LEFT_X < config.WINDOW_WIDTH - 1
        assert 0 < PILE_NUMBER_RIGHT_X < config.WINDOW_WIDTH - 1

        # 盤面 -> 目盛りの線の座標
        assert 0 < SCALE_LINE_TOP_Y < config.WINDOW_HEIGHT - 1
        assert 0 < SCALE_LINE_BOTTOM_Y < config.WINDOW_HEIGHT - 1
        assert 0 < SCALE_LINE_X < config.WINDOW_WIDTH - 1

        # 盤面 -> 目盛りの番号の座標
        assert 0 < SCALE_NUMBER_TOP_Y < config.WINDOW_HEIGHT - 1
        assert 0 < SCALE_NUMBER_BOTTOM_Y < config.WINDOW_HEIGHT - 1
        assert 0 < SCALE_NUMBER_X < config.WINDOW_WIDTH - 1

        # 盤面 -> 石のmatrixの座標
        assert 0 < MATRIX_TOP_Y < config.WINDOW_HEIGHT - 1
        assert 0 < MATRIX_BOTTOM_Y < config.WINDOW_HEIGHT - 1
        assert 0 < MATRIX_LEFT_X < config.WINDOW_WIDTH - 1
        assert 0 < MATRIX_RIGHT_X < config.WINDOW_WIDTH - 1
    # def get_key_event(self, event):
    #     if self.agent[self.round % 2] ==
    #     self.agent[self.round % 2].action()

    # class GameController():

    #     def __init__(self):
    #         self.players = []
    #         self.fields = None
    #         self.preceding = 0
    #         self.round = 0

    #         self.setup()

    #     def setup(self):
    #         print("ゲームを開始します.")

    #         print("player1をプレイする場合は[1],computerの場合は[0]を入力してください")
    #         print(">> ", end="")
    #         cmd = int(input())
    #         if cmd:
    #             self.players.append(PlayerAgent())
    #         else:
    #             self.players.append(ComputerAgent())

    #         print("player2をプレイする場合は[1],computerの場合は[0]を入力してください")
    #         print(">> ", end="")
    #         cmd = int(input())
    #         if cmd:
    #             self.players.append(PlayerAgent())
    #         else:
    #             self.players.append(ComputerAgent())

    #         print("山の数を指定してください")  # 5個まで
    #         print(">> ", end="")
    #         fields_cnt = int(input())

    #         print("石の個数を1~20の範囲でランダムに生成します")
    #         self.fields = np.zeros(fields_cnt, dtype=np.int64)
    #         for i in range(fields_cnt):
    #             self.fields[i] = random.randrange(1, 21)

    #         print("player1が先行の場合は[1], player2が先行の場合は[2]を入力してください")
    #         print(">> ", end="")
    #         self.preceding = int(input())

    #     def process(self):
    #         while True:
    #             self.round += 1
    #             turn_player = (self.round + self.preceding) % 2
    #             self.show_fields()
    #             origin_fields = np.array(self.fields)
    #             self.players[turn_player].action(self.fields)

    #             # 変更の正しさを検証する
    #             if self.validate(origin_fields, self.fields):
    #                 pass
    #             else:
    #                 print("不正な変更です")
    #                 exit()

    #             if np.all(self.fields == 0):
    #                 if turn_player == 0:
    #                     print("player1の勝ちです")
    #                 else:
    #                     print("player2の勝ちです")
    #                 exit()

    #     def show_fields(self):
    #         """
    #         func: 現状の盤面を出力する
    #         todo: フォーマット指定子で整える
    #         """

    #         print("\n====================")
    #         print("現在{}ターン目です".format(self.round))

    #         # 石の個数を出力
    #         print("個数|", end="")
    #         for i in range(len(self.fields)):
    #             print(str(self.fields[i]).rjust(2, "0"), end="|")
    #         print()

    #         # # 仕切り線
    #         # for i in range(len(self.fields)):
    #         #     print("----", end="")
    #         # print()

    #         # 山の番号を出力
    #         print("番号|", end="")
    #         for i in range(len(self.fields)):
    #             print(str(i).rjust(2, "0"), end="|")
    #         print("\n====================")

    #     def validate(self, before_fields, after_fields):

    #         flag = False
    #         for i in range(len(before_fields)):
    #             if before_fields[i] != after_fields[i]:
    #                 if flag:
    #                     return False
    #                 else:
    #                     flag = True
    #         return flag
