import colorama
import os
from datetime import datetime
import sys
from pathlib import Path

from dotenv import load_dotenv

content_path = Path('../../../../../UE5-python')
sys.path.append(str(content_path))

from Content.Python.src.bot import bot
from Content.Python.src.core import process_system


dotenv_path = Path('../bot/.env')
load_dotenv(dotenv_path=dotenv_path)



# openai_key = os.environ["OPENAI_API_KEY"]

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

system_template = SystemMessagePromptTemplate.from_template("You are an AI assistant.")
user_template = HumanMessagePromptTemplate.from_template("{user_prompt}")
template = ChatPromptTemplate.from_messages([system_template, user_template])

# Initialize LangChain components
llm = ChatOpenAI()
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)
chain = LLMChain(llm=llm, memory=memory, prompt=template, verbose=False)


# Description:
# Argument 1:
# Argument 2:
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


# Description:
def conversate(model=bot.last_openai_model):
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    while True:
        print(colorama.Fore.RED + "Enter your text:" + colorama.Fore.CYAN)
        text = input()
        add_message(text, initial_time)
        if text == "exit" or text == "quit":
            exit(0)
        if model in bot.non_openai_models:
            bot_answer = bot.bot(text, model)
        else:
            response = conversation.predict(input=text)  # Predict using chain with memory
            bot_answer = response

            # Save to memory only if the AI response is not empty

            if bot_answer.strip():
                memory.save_context({"input": text}, {"output": bot_answer})

        add_message(bot_answer, initial_time)
        print(colorama.Fore.GREEN + bot_answer)
        print(colorama.Fore.RESET)


def main():
    repo_dir = os.path.join(os.path.abspath(__file__)[:-14].split("\n")[0], "conversations")
    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)

    '''if len(sys.argv) < 2:
        print("Please provide a text prompt as the first argument.")
        return'''
    if len(sys.argv) == 2:
        # If the 1st argument is a valid language model from bot.non_openai_models...
        initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        text = sys.argv[1]
        add_message(text, initial_time)
        if text == "exit" or text == "quit":
            exit(0)

        if text in bot.non_openai_models:
            conversate(text)
        else:
            bot_answer = bot.bot(text)
        add_message(bot_answer, initial_time)
        print(colorama.Fore.GREEN + bot_answer)
        print(colorama.Fore.RESET)
    elif len(sys.argv) == 3:
        initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        text = sys.argv[1]
        model_name = sys.argv[2]
        add_message(text, initial_time)
        if text == "exit" or text == "quit":
            exit(0)

        bot_answer = bot.bot(text, model_name)
        add_message(bot_answer, initial_time)
        print(colorama.Fore.GREEN + bot_answer)
        print(colorama.Fore.RESET)
    else:
        conversate()


if __name__ == '__main__':
    main()
