import random
import numpy as np

from player_agent import PlayerAgent
from computer_agent import ComputerAgent


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
        cmd = int(input())
        if cmd:
            self.players.append(PlayerAgent())
        else:
            self.players.append(ComputerAgent())

        print("player2をプレイする場合は[1],computerの場合は[0]を入力してください")
        cmd = int(input())
        if cmd:
            self.players.append(PlayerAgent())
        else:
            self.players.append(ComputerAgent())

        print("山の数を指定してください")
        fields_cnt = int(input())

        print("石の個数を1~20の範囲でランダムに生成します")
        self.fields = np.zeros(fields_cnt, dtype=np.int64)
        for i in range(fields_cnt):
            self.fields[i] = random.randrange(1, 21)

        print("player1が先行の場合は[1], player2が先行の場合は[2]を入力してください")
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

        print("現在{}ターン目です".format(self.round))

        # 石の個数を出力
        print("個数|", end="")
        for i in range(len(self.fields)):
            print(str(self.fields[i]).rjust(2, "0"), end="|")
        print()

        # 仕切り線
        for i in range(len(self.fields)):
            print("----", end="")
        print()

        # 山の番号を出力
        print("番号|", end="")
        for i in range(len(self.fields)):
            print(str(i).rjust(2, "0"), end="|")
        print()

    def validate(self, before_fields, after_fields):

        flag = False
        for i in range(len(before_fields)):
            if before_fields[i] != after_fields[i]:
                if flag:
                    return False
                else:
                    flag = True
        return flag
