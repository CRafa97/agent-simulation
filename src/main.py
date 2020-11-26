from environment import Environment
from actors.agents import Reactive

def main():
    agent1 = Reactive()
    env = Environment(10, 10, 5, 15, 10, 5, agent1)
    print(f"Start, Dirty: {env.dirty}")
    print(env)

    raise Exception()

    for i in range(30):
        print(f"Turn {i + 1}, Dirty: {env.dirty}")
        env.next()
        
        if (i + 1) % env.t == 0:
            print("SHUFFLE ENV")
            env.remake()


        print(env)
        print("-----------------------------------------")

if __name__ == "__main__":
    main()