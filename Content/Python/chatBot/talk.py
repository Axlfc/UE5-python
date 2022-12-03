import os
import colorama


def main():
    while True:
        print("Enter your text:")
        text = input()
        if text == "exit" or text == "quit":
            exit(0)
        command = "python plot.py \"" + str(text) + "\""
        print(colorama.Fore.YELLOW)
        os.system(command)
        print(colorama.Fore.RESET)


if __name__ == '__main__':
    main()