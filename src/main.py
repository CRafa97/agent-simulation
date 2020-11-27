from environment import Environment
from agents import Reactive

from simulator import Simulator

def main():
    agent1 = Reactive()
    t = 5
    env = Environment(10, 10, t, 10, 15, 3, agent1)
    print(f"Start, Dirty: {env.dirty}")
    print(env)

    for i in range(100*t):
        print(f"Turn {i + 1}, Dirty: {env.dirty}")
        agent1.next(env)
        env.next()

        if (i + 1) % env.t == 0:
            print("SHUFFLE ENV")
            env.remake()
        
        if env.is_clean():
            print("WIN")
            break
        elif env.trash_pc() >= 0.6:
            print("LOSE")
            break

        print(env.dirty)
        print(env.children)
        print(list((c.child, c.with_child) for c in env.cradles))

        print(env)
        print("-----------------------------------------")

if __name__ == "__main__":
    # main()
    s = Simulator()
    s.run()