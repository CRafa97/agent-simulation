from environment import Environment

def main():
    env = Environment(10, 10, 5, 15, 10, 3)
    print("Start")
    print(env)

    for i in range(50):
        print(f"Turn {i}")
        env.next()
        print(env)
        print("-----------------------------------------")

if __name__ == "__main__":
    main()