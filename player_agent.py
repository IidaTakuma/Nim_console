from agent import Agent


class PlayerAgent(Agent):

    def __init__(self):
        pass

    def action(self, fields):
        while True:
            print("何番の山から石を取りますか?")
            idx = int(input())
            if fields[idx] == 0:
                print("その山には石がありません")
                continue
            if idx >= len(fields):
                print("正しい数値を選択してください")
                continue
            while True:
                print("{}番目の山から何個取りますか?".format(idx))
                print("山を選び直す場合は[q]を押してください")
                ipt = input()
                if ipt == "q":
                    break
                cnt = int(ipt)
                if cnt > fields[idx]:
                    print("数が多すぎます")
                    continue
                fields[idx] -= cnt
                print("aaa")
                return fields
