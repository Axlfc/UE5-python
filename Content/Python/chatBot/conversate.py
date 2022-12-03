import bot
import colorama

def main():
    while True:
        print("Enter your text:")
        text = input()
        if text == "exit" or text == "quit":
            exit(0)
        print(colorama.Fore.YELLOW + bot.bot(text))
        print(colorama.Fore.RESET)


if __name__ == '__main__':
    main()