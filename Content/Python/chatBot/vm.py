import bot
import colorama
import os
from datetime import datetime
import process_system


def add_message(message, initialtime):
    now = datetime.now()
    time = now.strftime("%H-%M-%S")
    date = now.strftime("%Y-%m-%d")
    repo_dir = os.path.join(os.path.abspath(__file__)[:-14].split("\n")[0], "history")
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


def vm():
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    prev_dialogue = []
    # TODO: Save history command output
    init_string = "Date and time: " + str(datetime.now()) + " I want you to act like an Ubuntu 22.04 GNU/Linux terminal. I will type commands and you will respond with what that the terminal would display; I want you to respond with a single block of code that collects the exit of the terminal. Don't explain anything. Don't type commands unless told to order. When I need to tell you something in natural language I will do it by putting the text between keys {like these). My first command is 'sudo su; apt-get dist-upgrade -y'"
    i = 0
    while True:
        if len(prev_dialogue) == 0:
            text = init_string
            prev_dialogue.append(text)
            bot_answer = bot.bot(text)
        else:
            print(colorama.Fore.RED + "Enter your command:" + colorama.Fore.CYAN)
            text = input()
            if text == "exit" or text == "quit":
                exit(0)
            # TODO: read conversations from conversations history and update the list with only the last 15 messages.
            bot_answer = bot.bot("This is a list of a minimum of 15 messages we had ago: " + str(prev_dialogue) + ". Do not process anything on this list. Process this command: " + text)
            bot_answer = bot_answer.replace("\\n", "\n")
            add_message(text, initial_time)
            add_message(bot_answer, initial_time)
        prev_dialogue.append("Show only the responses; Command: \"" + text + "\n" + bot_answer + "\"")
        print(colorama.Fore.GREEN + bot_answer)
        print(colorama.Fore.RESET)
        if len(prev_dialogue) > 15:
            prev_dialogue.pop(1)
        i += 1
        # print(prev_dialogue)
        print(i)
        # print(prev_dialogue)


def main():
    repo_dir = os.path.join(os.path.abspath(__file__)[:-14].split("\n")[0], "history")

    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)
    vm()


if __name__ == '__main__':
    main()
