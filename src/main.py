from environment import Environment

def main():
    env = Environment(10, 10, 5, 15, 10, 5)
    print(f"Start, Dirty: {env.dirty}")
    print(env)

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