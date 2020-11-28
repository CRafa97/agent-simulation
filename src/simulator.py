from environment import *
from agents import *
import random as rnd

from copy import deepcopy

def main():
    print("Simulation Report")
    run()

def run():
    envs = [gen_env(None) for _ in range(10)]
    for agent in [Reactive(), Proactive()]:
        print(f"Testing -- {agent.name}")
        results = {i: None for i in range(10)}
        for i, env in enumerate(envs):
            c_agent = deepcopy(agent)
            env.set_rnd_agent(c_agent)
            copy = deepcopy(env)
            d = {"Despedido": 0, "Casa Limpia": 0, "Trash": [] }
            for j in range(30):
                for tn in range(100*env.t):
                    env.agent.next(env)
                    env.next()
                    if (tn + 1) % env.t == 0:
                        env.remake()
                    if env.trash_pc() >= 0.6:
                        d["Despedido"] += 1
                        break
                    elif env.is_clean():
                        d["Casa Limpia"] += 1
                        break
                    else:
                        pass
                d["Trash"].append(env.dirty)
                env = copy
            d["Trash"] = round(sum(d["Trash"])/len(d["Trash"]), 2)
            results[i] = d
            print(f"Done {i+1} -- {env.N}x{env.M}, t={envs[i].t}, Trash:{envs[i].trash_pc()}%, Objs:{len(env.blocking)}, Kids:{len(env.cradles)}")
        print()
        print(f"Info for {agent.name}")
        for i in range(10):
            print(f"{i+1}: {results[i]}")
        print()
        print()

def gen_env(agent):
    N = rnd.randint(5, 12)
    M = rnd.randint(5, 12)
    t = rnd.randint(5, 8)
    dp = rnd.randint(15, 35)
    bp = rnd.randint(10, 15)
    childn = rnd.randint(2, 6)

    return Environment(N, M, t, dp, bp, childn, agent)

if __name__ == "__main__":
    main()