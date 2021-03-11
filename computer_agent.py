import random
from agent import Agent


class ComputerAgent(Agent):

    def __init__(self):
        pass

    def action(self, fields):
        """
        func: 必勝条件を満たすなら必勝手を打つ，そうでないならランダムに動作する
        """
        xor_sum = self.calc_xor_sum(fields)
        if xor_sum == 0:
            # 必勝手がない
            idx = -1
            while True:
                idx = random.randrange(0, len(fields))
                if fields[idx] != 0:
                    break

            cnt = random.randrange(1, fields[idx] + 1)
            fields[idx] -= cnt
            print("コンピュータは{}の山から{}個石を取った".format(idx, cnt))
        else:
            # 必勝手がある
            idx = -1
            maxi = 0
            for i, f in enumerate(fields):
                if maxi < f:
                    maxi = f
                    idx = i

            xor_sum ^= fields[idx]
            fields[idx] = xor_sum
            print("コンピュータは{}の山から{}個石を取った".format(idx, maxi - fields[idx]))
        return fields

    def calc_xor_sum(self, fields):
        ret = 0
        for f in fields:
            ret ^= f
        return ret
