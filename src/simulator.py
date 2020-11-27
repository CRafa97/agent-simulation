from environment import *
from agents import *
import random as rnd

from copy import deepcopy

class Simulator:
    def __init__(self):
        pass

    def run(self):
        results = {i: None for i in range(10)}
        for i in range(10):
            env = self.gen_env(Reactive())
            copy = deepcopy(env)
            d = {"Despido": 0, "Limpiado": 0, "Trash": [] }
            for j in range(30):
                for tn in range(100*env.t):
                    env.agent.next(env)
                    env.next()

                    if (tn + 1) % env.t == 0:
                        env.remake()

                    #check lose
                    if env.trash_pc() >= 0.6:
                        d["Despido"] += 1
                        d["Trash"].append(env.dirty)
                        env = copy
                        break
                    elif env.is_clean():
                        d["Limpiado"] += 1
                        env = copy
                        break
                d["Trash"].append(env.dirty)
                env = copy
            d["Trash"] = sum(d["Trash"])/len(d["Trash"])
            results[i] = d
            print(f"Done {i+1}")

        for i in range(10):
            print(f"{i+1}: {results[i]}")

    def gen_env(self, agent):
        N = rnd.randint(5, 12)
        M = rnd.randint(5, 12)
        t = rnd.randint(5, 10)
        dp = rnd.randint(15, 30)
        bp = rnd.randint(10, 20)
        childn = rnd.randint(3, 6)

        return Environment(N, M, t, dp, bp, childn, agent)
