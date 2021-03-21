import random
from agent.agent import Agent


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
            # 必勝手がある場合，全ての山で必勝手の可能性を試す
            for i, f in enumerate(fields):
                if f == 0:
                    continue

                xor_sum_tmp = xor_sum ^ f
                remove = f - xor_sum_tmp
                if remove <= f and remove > 0:
                    print("コンピュータは{}の山から{}個石を取った".format(i, remove))
                    fields[i] -= remove
                    break
        return fields

    def calc_xor_sum(self, fields):
        ret = 0
        for f in fields:
            ret ^= f
        return ret
