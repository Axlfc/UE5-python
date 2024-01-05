import sys
import time
from pathlib import Path
import json

content_path = Path('../../../../../UE5-python')
sys.path.append(str(content_path))

from Content.Python_dependencies.latest_openai import openai

from dotenv import load_dotenv
import os

# Load your OpenAI API key from .env file
dotenv_path = Path('../bot/.env')
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)


def save_assistant_data(assistant_id, assistant_name, thread_id, file_path='assistants_data.json'):
    # Load existing data
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    # Update data with new assistant and thread
    data[assistant_name] = {'assistant_id': assistant_id, 'thread_id': thread_id}

    # Save updated data
    with open(file_path, 'w') as file:
        json.dump(data, file)


def load_assistant_data(assistant_name, file_path='assistants_data.json'):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(assistant_name, {})
    except FileNotFoundError:
        return {}


def load_assistant_id_by_name(assistant_name, file_path='assistants_data.json'):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(assistant_name)
    except FileNotFoundError:
        return None


def create_assistant(assistant_name, instructions, model="gpt-4-1106-preview", code=False, file_path='assistants_data.json'):
    existing_assistant_id = load_assistant_id_by_name(assistant_name, file_path)
    if existing_assistant_id:
        print(f"Using existing assistant: {existing_assistant_id}")
        return existing_assistant_id
    else:
        tools = [{"type": "code_interpreter"}] if code else []
        assistant = client.beta.assistants.create(
            name=assistant_name,
            instructions=instructions,
            tools=tools,
            model=model
        )
        print(f"Assistant created: {assistant.id}")
        return assistant.id


def create_thread(assistant_name, assistant_id, file_path='assistants_data.json'):
    assistant_data = load_assistant_data(assistant_name, file_path)

    if 'thread_id' in assistant_data and assistant_data['thread_id']:
        print(f"Using existing thread: {assistant_data['thread_id']}")
        return assistant_data['thread_id']

    # Create a new thread if no existing thread ID
    thread = client.beta.threads.create()
    print(f"Thread created: {thread.id}")

    # Update the assistant data with the new thread ID
    save_assistant_data(assistant_id, assistant_name, thread.id, file_path)
    return thread.id


def add_message_to_thread(thread_id, content, role="user"):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role=role,
        content=content
    )
    return message


def run_assistant(thread_id, assistant_id):
    run_response = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    run_id = run_response.id  # Capture the run ID correctly
    print(f"Run initiated with ID: {run_id}")
    return run_id


def retrieve_run_status(thread_id, run_id):
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )
    return run_status


def get_assistant_responses(thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data  # Return the list of messages directly


def wait_for_run_completion(thread_id, run_id, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        run_status = retrieve_run_status(thread_id, run_id)
        if run_status.status == "completed":
            return True
        elif run_status.status in ["failed", "cancelled", "expired"]:
            return False
        time.sleep(5)  # Wait for 5 seconds before checking again
    return False  # Timeout


def extract_value_from_response(response):
    # Convert the response object to a string
    response_str = str(response)

    # Find the start and end indices of the 'value' content
    start_index = response_str.find("value='") + len("value='")
    end_index = response_str.find("'), type='text'")

    # Extract the content between these indices
    if start_index != -1 and end_index != -1:
        extracted_content = response_str[start_index:end_index]
    else:
        extracted_content = "Content not found."

    return extracted_content


def check_assistant(name, instructions):
    pass


def main():
    assistant_name = "Math Tutor"
    instructions = "You are a personal math tutor. Write and run code to answer math questions."
    assistant_id = create_assistant(assistant_name, instructions, code=True)
    print(f"{assistant_name} Assistant loaded.")

    thread_id = create_thread(assistant_name, assistant_id)
    print(f"Thread created/loaded: {thread_id}")

    while True:
        user_question = input("Enter your question (or type 'exit' to quit): ")
        if user_question.lower() == 'exit':
            break

        add_message_to_thread(thread_id, user_question)
        print("User question added to thread.")

        run_id = run_assistant(thread_id, assistant_id)
        if run_id:  # Ensure run_id is not None or empty
            if wait_for_run_completion(thread_id, run_id):
                responses = get_assistant_responses(thread_id)
                for response in responses:
                    if response.role == "assistant":
                        content = extract_value_from_response(response.content)
                        print(f"Assistant: {content}")
            else:
                print("Run did not complete successfully.")
        else:
            print("Run initiation failed.")

        print("----\n")


if __name__ == "__main__":
    main()
