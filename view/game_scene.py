from computer_agent import ComputerAgent
from player_agent import PlayerAgent
import random
import curses
import time
import numpy as np

from display import Display

SLEEP_SEC = 7


class GameScene(Display):
    def __init__(self, window_size_y, window_size_x):
        self.window_size_y = window_size_y
        self.window_size_x = window_size_x
        self.window = np.empty((window_size_y, window_size_x), dtype=str)

    def view(self, matrix, game_log):
        self.set_window_flame()

        # 左右の仕切り
        self.set_vertical_line(15, 0, self.window_size_y - 1)

        # 右半分の上下の仕切り
        self.set_horizintal_line(17, 15, self.window_size_x - 1)

        # 盤面の枠
        self.set_rectangle(3, 2, 26, 13)

        # 盤面の下線
        self.set_horizintal_line(24, 3, 12)

        # 盤面のした線の目盛り
        for i in range(0, 8):
            self.window[25][i + 4] = str(i)

        # 山の記録
        self.set_matrix(matrix, 23, 4)

        # ゲームログ
        self.set_game_log(game_log)

        # 出力
        self.draw_window()

    def set_game_log(self, game_log):
        for i, l in enumerate(game_log):
            for j, t in enumerate(l[0]):
                self.window[i * 3 + 1][j + 16] = t
            for j, c in enumerate(l[1]):
                self.window[i * 3 + 2][j + 16] = c

    def select_pile(self):
        return cmd

    def select_quantity(self):
        return cmd


if __name__ == "__main__":
    matrix = np.zeros((7, 8))
    game_log = [["{}ターン目".format(i), "ログ{}行目".format(i)] for i in range(5)]
    print(game_log)
    game_scene = GameScene(30, 25)
    game_scene.view(matrix, game_log)


class GameController():

    def __init__(self):
        self.players = []
        self.fields = None
        self.preceding = 0
        self.round = 0

        self.setup()

    def setup(self):
        print("ゲームを開始します.")

        print("player1をプレイする場合は[1],computerの場合は[0]を入力してください")
        print(">> ", end="")
        cmd = int(input())
        if cmd:
            self.players.append(PlayerAgent())
        else:
            self.players.append(ComputerAgent())

        print("player2をプレイする場合は[1],computerの場合は[0]を入力してください")
        print(">> ", end="")
        cmd = int(input())
        if cmd:
            self.players.append(PlayerAgent())
        else:
            self.players.append(ComputerAgent())

        print("山の数を指定してください")  # 5個まで
        print(">> ", end="")
        fields_cnt = int(input())

        print("石の個数を1~20の範囲でランダムに生成します")
        self.fields = np.zeros(fields_cnt, dtype=np.int64)
        for i in range(fields_cnt):
            self.fields[i] = random.randrange(1, 21)

        print("player1が先行の場合は[1], player2が先行の場合は[2]を入力してください")
        print(">> ", end="")
        self.preceding = int(input())

    def process(self):
        while True:
            self.round += 1
            turn_player = (self.round + self.preceding) % 2
            self.show_fields()
            origin_fields = np.array(self.fields)
            self.players[turn_player].action(self.fields)

            # 変更の正しさを検証する
            if self.validate(origin_fields, self.fields):
                pass
            else:
                print("不正な変更です")
                exit()

            if np.all(self.fields == 0):
                if turn_player == 0:
                    print("player1の勝ちです")
                else:
                    print("player2の勝ちです")
                exit()

    def show_fields(self):
        """
        func: 現状の盤面を出力する
        todo: フォーマット指定子で整える
        """

        print("\n====================")
        print("現在{}ターン目です".format(self.round))

        # 石の個数を出力
        print("個数|", end="")
        for i in range(len(self.fields)):
            print(str(self.fields[i]).rjust(2, "0"), end="|")
        print()

        # # 仕切り線
        # for i in range(len(self.fields)):
        #     print("----", end="")
        # print()

        # 山の番号を出力
        print("番号|", end="")
        for i in range(len(self.fields)):
            print(str(i).rjust(2, "0"), end="|")
        print("\n====================")

    def validate(self, before_fields, after_fields):

        flag = False
        for i in range(len(before_fields)):
            if before_fields[i] != after_fields[i]:
                if flag:
                    return False
                else:
                    flag = True
        return flag
