import os
import time
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


book_writer_context = "You are an AI that writes books and an expert in creating well-structured humanized outlines. " \
          "You can use other books of the same genre for inspiration or create your own writing style. " \
          "The book should be divided into chapters and each chapter into paragraphs. " \
          "You can handle specific commands: " \
          "\"!w {chapter_number} {paragraph_number}\": Write a paragraph for the specified chapter and paragraph number. " \
          "\"!t\": Write the title for the book. " \
          "\"!s\": Only a list with the structure of the book chapter names in a table format. " \
          "The system may use the command \"!c\" if you haven't met the required word count. " \
          "This means you should continue writing the same paragraph while ensuring that new content is added and there is no repetition. " \
          "The user will provide you with information about the topic and other details about the book. " \
          "Type \"Ready\" when you have received this information from the user."
book_writer_context_spanish = " " \
          "Eres una IA que escribe libros y una experta en crear esquemas humanizados bien estructurados. " \
          "Puedes manejar comandos específicos: " \
          "\"!w {numero_capitulo} {numero_parrafo}\": Escriba un párrafo para el capítulo y el número de párrafo especificados. " \
          "Debes continuar escribiendo el mismo párrafo mientras te aseguras de que se agregue contenido nuevo y no haya repeticiones." \
          "\"!t\": Escribe el título del libro. " \
          "El usuario le proporcionará información sobre el tema y otros detalles sobre el libro. " \
          "Escribe \"Listo\" cuando haya recibido esta información por parte del usuario."

initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

book_content = []
book_outline = []

# Global book context
book_context = {
    "title": "",
    "synopsis": "",
    "total_chapters": 0,
    "paragraphs_per_chapter": 0
}


# Check if it's the last paragraph of the current chapter
def is_last_paragraph_of_chapter(current_chapter, current_paragraph):
    return current_paragraph == book_context["paragraphs_per_chapter"]


# Check if it's the last chapter of the book
def is_last_chapter(current_chapter):
    return current_chapter == book_context["total_chapters"]


def add_message(message, initialtime):
    if message:
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        repo_dir = os.path.join(os.path.abspath(__file__)[:-14].split("\n")[0], "conversations")
        if platform.system() == "Windows":
            x = repo_dir + "\\" + date
            filepath = x + "\\" + initialtime + ".txt"
        else:
            x = repo_dir + "/" + date
            filepath = x + "/" + initialtime + ".txt"
        os.makedirs(x, exist_ok=True)

        with open(filepath, "a", encoding="utf-8") as f:
            f.write(message.strip() + "\n")


def handle_response(text, is_title):
    answer = predict(text)

    if answer.strip():
        save(text, answer)

    if not is_title:
        add_message(answer, initial_time)


def clear_memory():
    conversation.memory.clear()


def print_memory():
    memory_content = str(memory.buffer)

    memory_content.replace(book_writer_context, '')

    print(memory_content)


def initialize_conversation():
    save(book_writer_context, "")


def get_last_two_paragraphs(current_chapter, current_paragraph):
    # Filter paragraphs from the current and previous chapter
    relevant_paragraphs = [p for p in book_content if p[0] in [current_chapter, current_chapter - 1]]

    # Sort the paragraphs first by chapter, then by their order of addition
    relevant_paragraphs.sort(key=lambda x: (x[0], book_content.index(x)))

    # Select the last two paragraphs
    last_two = relevant_paragraphs[-2:] if len(relevant_paragraphs) >= 2 else relevant_paragraphs

    # Return the paragraph texts, concatenated
    return "\n\n".join([p[1] for p in last_two])


def update_memory_with_paragraph(chapter, paragraph, paragraph_text, chapter_title):
    chapter_context = f" Chapter {chapter}: {chapter_title}, Paragraph {paragraph}. "
    full_context = book_writer_context + "\n\nBook name: " + book_context['title'] + chapter_context + \
                   get_last_two_paragraphs(chapter, paragraph) + "\n\n" + paragraph_text

    # print("PREVIOUS MEMORY:\n")
    # print_memory()

    clear_memory()
    save(full_context, "")


def generate_paragraph(chapter, paragraph, chapter_titles):
    chapter_title = chapter_titles[chapter - 1]  # Adjust index for 0-based list
    print(f"MEMORY in CHAPTER {chapter} PARAGRAPH {paragraph}:")
    print_memory()
    paragraph_text = predict(f"!w {chapter} {paragraph}\n\n(Please give only the text of a newly generated paragraph as the answer and avoid repeating any text already written before.)")

    # Add new paragraph to book content
    book_content.append((chapter, paragraph_text))
    update_memory_with_paragraph(chapter, paragraph, paragraph_text, chapter_title)
    return paragraph_text


def predict(prompt):
    if prompt:  # Check if the prompt is not None or empty
        return conversation.predict(input=prompt)
    else:
        return ""


def save(input_text, output_text: str = ""):
    memory.save_context({"input": input_text}, {"output": output_text})


def update_book_context():
    global book_context
    # You can expand this function to capture more details or modify the existing context
    book_context["title"] = input("Enter the book title:\t")
    book_context["synopsis"] = input("Enter the book synopsis or general ideas:\t")
    book_context["total_chapters"] = int(input("Escribe el número de capítulos:\t"))
    book_context["paragraphs_per_chapter"] = int(input("Escribe el número de párrafos por capítulo:\t"))


def save_full_context_to_memory():
    my_string = "!t " + book_context["title"] + ", "
    if book_context["synopsis"]:
        my_string += "synopsis: " + book_context["synopsis"] + "."
    save(my_string, "")


def generate_book_outline():
    global book_outline
    book_outline = []  # Reset the list in case this function is called multiple times
    my_prompt = f"!s {book_context['total_chapters']} chapters\n\nPlease list the chapter titles in the following format:\n'Chapter 1: [Title]', 'Chapter 2: [Title]', etc."
    return predict(my_prompt)


def process_outline(outline):
    # Split the text by lines and filter out irrelevant lines
    lines = outline.split("\n")
    chapter_titles = [line.strip() for line in lines if line.lower().startswith("chapter") and ":" in line]
    return chapter_titles


def save_outline(outline):
    # Define the file name and path for saving the outline
    outline_file_name = "book_outline.txt"
    outline_file_path = os.path.join(os.path.dirname(__file__), outline_file_name)

    # Write the outline to a file
    with open(outline_file_path, "w", encoding="utf-8") as file:
        file.write(outline)


def read_chapter_titles():
    outline_file_name = "book_outline.txt"
    outline_file_path = os.path.join(os.path.dirname(__file__), outline_file_name)
    chapter_titles = []

    with open(outline_file_path, "r", encoding="utf-8") as file:
        for line in file:
            chapter_titles.append(line.strip())

    return chapter_titles


def create_main_outline():
    initialize_conversation()

    update_book_context()

    save_full_context_to_memory()

    raw_outline = generate_book_outline()

    time.sleep(.2)

    processed_outline = process_outline(raw_outline)

    save_outline("\n".join(processed_outline))

    return read_chapter_titles()


def is_valid_response(response):
    invalid_start_phrases = ["I'm", "Sure!", "Sure", "Sorry", "I apologize,", "I apologize", "Apologies", "Unfortunately"]
    return not any(response.startswith(phrase) for phrase in invalid_start_phrases)


def main():
    chapter_titles = create_main_outline()

    for chapter in range(1, book_context["total_chapters"] + 1):
        if is_last_chapter(chapter):
            save("\n\nThis is the last chapter of the book.")

        for paragraph in range(1, book_context["paragraphs_per_chapter"] + 1):
            # Special handling for the end of a chapter or the book
            if is_last_paragraph_of_chapter(chapter, paragraph):
                # Handle end of chapter
                save(f"\n\nThis is the last paragraph of the chapter {chapter}.")

            paragraph_text = generate_paragraph(chapter, paragraph, chapter_titles)
            add_message(paragraph_text, initial_time)


if __name__ == '__main__':
    main()
