import os
from datetime import datetime
import platform
from dotenv import load_dotenv
from pathlib import Path

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


book_writer_context_english = "You are an AI that writes books and an expert in creating well-structured humanized outlines. " \
          "You can use other books of the same genre for inspiration or create your own writing style. " \
          "The book should be divided into chapters and each chapter into paragraphs. " \
          "You can handle specific commands: " \
          "\"!w {chapter_number} {paragraph_number}\": Write a paragraph for the specified chapter and paragraph number. " \
          "\"!t\": Write the title for the book. " \
          "\"!s\": List the structure of the book in a table format. Create a well-structured outline so that paragraphs are connected and enjoyable to read. " \
          "The system may use the command \"!c\" if you haven't met the required word count. " \
          "This means you should continue writing the same paragraph while ensuring that new content is added and there is no repetition. " \
          "The user will provide you with information about the topic and other details about the book. " \
          "Type \"Ready\" when you have received this information from the user."
book_writer_context = " " \
          "Eres una IA que escribe libros y una experta en crear esquemas humanizados bien estructurados. " \
          "Puedes manejar comandos específicos: " \
          "\"!w {numero_capitulo} {numero_parrafo}\": Escriba un párrafo para el capítulo y el número de párrafo especificados. " \
          "Debes continuar escribiendo el mismo párrafo mientras te aseguras de que se agregue contenido nuevo y no haya repeticiones." \
          "\"!t\": Escribe el título del libro. " \
          "El usuario le proporcionará información sobre el tema y otros detalles sobre el libro. " \
          "Escribe \"Listo\" cuando haya recibido esta información por parte del usuario."

initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

book_content = []


def add_message(message, initialtime):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    repo_dir = os.path.join(os.path.abspath(__file__)[:-14].split("\n")[0], "conversations")
    if platform.system() == "Windows":
        x = repo_dir + "\\" + date
        filepath = x + "\\" + initialtime + ".txt"
    else:
        x = repo_dir + "/" + date
        filepath = x + "/" + initialtime + ".txt"
    if not os.path.exists(x):
        os.mkdir(x)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(message.strip() + "\n")


def handle_response(text, is_title):
    answer = conversation.predict(input=text)

    if answer.strip():
        memory.save_context({"input": text}, {"output": answer})

    if not is_title:
        add_message(answer, initial_time)


def clear_memory():
    conversation.memory.clear()


def initialize_conversation():
    # Set the initial context for the book
    conversation.predict(input=book_writer_context)
    memory.save_context({"input": book_writer_context}, {"output": ""})


def initialize_title():
    title = input("Escribe el título del libro:\t")
    command = "!t " + title
    answer = conversation.predict(input=command)
    memory.save_context({"input": answer}, {"output": ""})


def get_last_two_paragraphs(current_chapter, current_paragraph):
    # Filter paragraphs from the current and previous chapter
    relevant_paragraphs = [p for p in book_content if p[0] in [current_chapter, current_chapter - 1]]

    # Sort the paragraphs first by chapter, then by their order of addition
    relevant_paragraphs.sort(key=lambda x: (x[0], book_content.index(x)))

    # Select the last two paragraphs
    last_two = relevant_paragraphs[-2:] if len(relevant_paragraphs) >= 2 else relevant_paragraphs

    # Return the paragraph texts, concatenated
    return "\n\n".join([p[1] for p in last_two])


def update_memory_with_paragraph(chapter, paragraph, paragraph_text):
    # Construct the full context with the latest two paragraphs
    full_context = book_writer_context + "\n\n" + get_last_two_paragraphs(chapter, paragraph) + "\n\n" + paragraph_text

    # Clear the old memory and save the new context
    memory.clear()
    memory.save_context({"input": full_context}, {"output": ""})


def generate_paragraph(chapter, paragraph):
    prompt = f"!w {chapter} {paragraph}"
    paragraph_text = conversation.predict(input=prompt)

    # Add new paragraph to book content
    book_content.append((chapter, paragraph_text))

    update_memory_with_paragraph(chapter, paragraph, paragraph_text)
    return paragraph_text


def main():
    initialize_conversation()

    initialize_title()

    number_of_chapters = int(input("Escribe el número de capítulos:\t"))
    number_of_paragraphs_per_chapter = int(input("Escribe el número de párrafos por capítulo:\t"))

    for chapter in range(1, number_of_chapters + 1):
        add_message("Chapter " + str(chapter) + ":\n", initial_time)
        for paragraph in range(1, number_of_paragraphs_per_chapter + 1):
            paragraph_text = generate_paragraph(chapter, paragraph)
            add_message(paragraph_text, initial_time)

    #  handle_response(title, True)

    #  create_new_book_prompt_lines(number_of_chapters, number_of_paragraphs_per_chapter)


if __name__ == '__main__':

    main()
