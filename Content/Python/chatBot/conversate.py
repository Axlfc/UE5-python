import bot
import colorama
import os
from datetime import datetime
import process_system


def add_message(message, initialtime):
    now = datetime.now()
    time = now.strftime("%H-%M-%S")
    date = now.strftime("%Y-%m-%d")
    repo_dir = os.path.join(os.path.abspath(__file__)[:-14].split("\n")[0], "conversations")
    if process_system.plat() == "Windows":
        x = repo_dir + "\\" + date
        filepath = x + "\\" + initialtime + ".txt"
    else:
        x = repo_dir + "/" + date
        filepath = x + "/" + initialtime + ".txt"
    if not os.path.exists(x):
        os.mkdir(x)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(time.strip() + ": " + message.strip() + "\n")


def conversate():
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    while True:
        print(colorama.Fore.RED + "Enter your text:" + colorama.Fore.CYAN)
        text = input()
        add_message(text, initial_time)
        if text == "exit" or text == "quit":
            exit(0)
        bot_answer = bot.bot(text)
        add_message(bot_answer, initial_time)
        print(colorama.Fore.GREEN + bot_answer)
        print(colorama.Fore.RESET)


def main():
    repo_dir = os.path.join(os.path.abspath(__file__)[:-14].split("\n")[0], "conversations")

    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)
    conversate()


if __name__ == '__main__':
    main()
