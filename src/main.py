from environment import Environment
from agents import Reactive

def main():
    agent1 = Reactive()
    t = 5
    env = Environment(10, 10, t, 10, 15, 5, agent1)
    print(f"Start, Dirty: {env.dirty}")
    print(env)

    for i in range(10):
        print(f"Turn {i + 1}, Dirty: {env.dirty}")
        agent1.next(env)
        env.next()

        if (i + 1) % env.t == 0:
            print("SHUFFLE ENV")
            env.remake()

        print(env)
        print("-----------------------------------------")

if __name__ == "__main__":
    main()