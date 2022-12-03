import bot
import colorama
import os


def save_log():
    pass


def conversate():
    while True:
        print("Enter your text:")
        text = input()
        if text == "exit" or text == "quit":
            exit(0)
        print(colorama.Fore.YELLOW + bot.bot(text))
        print(colorama.Fore.RESET)


def main():
    repo_dir = os.path.join(os.getcwd().split("\n")[0], "conversations")

    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)
    conversate()


if __name__ == '__main__':
    main()
