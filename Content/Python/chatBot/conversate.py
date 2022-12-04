import bot
import colorama
import os
from datetime import datetime


def add_message(message, initialtime):
    now = datetime.now()
    time = now.strftime("%H-%M-%S")
    date = now.strftime("%m-%d-%Y")
    repo_dir = os.path.join(os.getcwd().split("\n")[0], "conversations")
    x = repo_dir + "\\" + date
    filepath = x + "\\" + initialtime + ".txt"
    if not os.path.exists(x):
        os.mkdir(x)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(time.strip() + ": " + message.strip() + "\n")
        # print("We should be adding the text: ", time + ":\t" + message + " to the file.")


def conversate():
    chat_log = []
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    while True:
        print("Enter your text:")
        text = input()
        add_message(text, initial_time)
        if text == "exit" or text == "quit":
            exit(0)
        bot_answer = bot.bot(text)
        add_message(bot_answer, initial_time)
        print(colorama.Fore.YELLOW + bot_answer)
        print(colorama.Fore.RESET)
        print(chat_log)


def main():
    repo_dir = os.path.join(os.getcwd().split("\n")[0], "conversations")

    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)
    conversate()


if __name__ == '__main__':
    main()
