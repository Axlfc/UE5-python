import os
import sys
import time
import platform
from datetime import datetime
from pathlib import Path
import json
import yaml
import logging
from dotenv import load_dotenv
from File import File

content_path = Path('../../../../../UE5-python')
sys.path.append(str(content_path))

from Content.Python_dependencies.latest_openai import openai

# Constants
DEFAULT_INSTRUCTIONS = "You are a default Assistant agent."
ASSISTANTS_DATA_FILENAME = 'assistants_data.json'
DEFAULT_TIMEOUT = 120
CONTENT_NOT_FOUND = "Content not found."
AGENTS_FILENAME = 'agents.yml'
LOG_FORMAT = "%(levelname)s: %(asctime)s - %(message)s"

# Configure logging
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Load your OpenAI API key from .env file
dotenv_path = Path('../bot/.env')
load_dotenv(dotenv_path=dotenv_path)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def save_assistant_data(assistant_id, assistant_name, thread_id, file_path=ASSISTANTS_DATA_FILENAME):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data[assistant_name] = {'assistant_id': assistant_id, 'thread_id': thread_id}
    with open(file_path, 'w') as file:
        json.dump(data, file)


def load_assistant_data(assistant_name, file_path=ASSISTANTS_DATA_FILENAME):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(assistant_name, {})
    except FileNotFoundError:
        return {}


def load_assistant_id_by_name(assistant_name, file_path=ASSISTANTS_DATA_FILENAME):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(assistant_name)
    except FileNotFoundError:
        return None


def create_assistant(assistant_name, instructions, model="gpt-4-1106-preview", code=False, file_path=ASSISTANTS_DATA_FILENAME):
    assistant_data = load_assistant_data(assistant_name, file_path)
    if assistant_data and 'assistant_id' in assistant_data:
        # print(f"Using existing assistant: {assistant_data['assistant_id']}")
        return assistant_data['assistant_id']
    else:
        tools = [{"type": "code_interpreter"}] if code else []
        assistant = client.beta.assistants.create(
            name=assistant_name,
            instructions=instructions,
            tools=tools,
            model=model
        )
        # print(f"Assistant created: {assistant.id}")
        save_assistant_data(assistant.id, assistant_name, None, file_path)
        return assistant.id


def create_thread(assistant_name, assistant_id, file_path=ASSISTANTS_DATA_FILENAME):
    assistant_data = load_assistant_data(assistant_name, file_path)

    if 'thread_id' in assistant_data and assistant_data['thread_id']:
        # print(f"Using existing thread: {assistant_data['thread_id']}")
        return assistant_data['thread_id']

    # Create a new thread if no existing thread ID
    thread = client.beta.threads.create()
    # print(f"Thread created: {thread.id}")

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
    # print(f"Run initiated with ID: {run_id}")
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


def wait_for_run_completion(thread_id, run_id, timeout=DEFAULT_TIMEOUT):
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
        extracted_content = CONTENT_NOT_FOUND

    return extracted_content.split("\n")[0]


def add_message(message, initialtime):
    now = datetime.now()
    time = now.strftime("%H-%M-%S")
    date = now.strftime("%Y-%m-%d")
    repo_dir = os.path.join(os.path.abspath(__file__)[:-9].split("\n")[0], "conversations")
    if platform.system() == "Windows":
        x = repo_dir + "\\" + date
        filepath = x + "\\" + initialtime + ".txt"
    else:
        x = repo_dir + "/" + date
        filepath = x + "/" + initialtime + ".txt"
    if not os.path.exists(x):
        os.mkdir(x)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(time.strip() + ": " + message.strip() + "\n")


def update_agents_yaml(yml_file, assistant_name, instructions):
    # Read existing agents
    with open(yml_file, 'r') as file:
        agents_data = yaml.safe_load(file) or {'agents': []}

    # Append new agent if it doesn't already exist
    if not any(agent['name'] == assistant_name for agent in agents_data['agents']):
        new_agent = {
            'name': assistant_name,
            'instructions': instructions
        }
        agents_data['agents'].append(new_agent)

        # Write updated agents back to file with proper formatting
        with open(yml_file, 'w') as file:
            yaml.dump(agents_data, file, default_flow_style=False, sort_keys=False)


def setup_assistant(yml_file, assistant_name="Assistant", default_instructions=""):
    agents = load_gpt_agents(yml_file)
    instructions = search_agent_by_name(assistant_name, agents)

    if instructions:
        return assistant_name, instructions
    else:
        # If no instructions are provided, use default instructions
        instructions = default_instructions if default_instructions else DEFAULT_INSTRUCTIONS
        # Add new agent to the YAML file
        update_agents_yaml(yml_file, assistant_name, instructions)
        return assistant_name, instructions


def load_gpt_agents(yml_file):
    with open(yml_file, "r") as file:
        data = yaml.safe_load(file)
        return data.get("agents", [])


def search_agent_by_name(name, agents):
    for agente in agents:
        if agente["name"] == name:
            return agente["instructions"]
    return ""


def setup_all_agents(agents_path):
    agents = load_gpt_agents(agents_path)
    for agent in agents:
        assistant_name, instructions = setup_assistant(agents_path, agent['name'])
        try:
            assistant_id = create_assistant(assistant_name, instructions, code=True)
            logger.info(f"{assistant_name} Assistant loaded.")
            thread_id = create_thread(assistant_name, assistant_id)
            # You can add other operations here if needed
        except Exception as e:
            logger.error(f"Error while setting up {assistant_name}: {e}")


def ask_boss_loop(boss_agent):
    processed_message_ids = []
    while True:
        user_input = input("Enter your question (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        boss_agent.send_message(user_input)
        run_id = boss_agent.run_assistant()
        if boss_agent.wait_for_run_completion(run_id):
            responses = boss_agent.get_responses()
            for response in responses:
                # Process and display response
                print("OKAY, HELLO!\t", response)
                pass
        else:
            print("Run did not complete successfully.")


def ask_user_loop(thread_id, assistant_id, processed_message_ids):
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    while True:
        user_question = input("Enter your question (or type 'exit' to quit): ")
        if user_question.lower() == 'exit':
            break

        add_message_to_thread(thread_id, user_question)
        add_message("User: " + user_question, initial_time)  # Registrar pregunta del usuario

        run_id = run_assistant(thread_id, assistant_id)
        if run_id:
            if wait_for_run_completion(thread_id, run_id):
                responses = get_assistant_responses(thread_id)
                for response in responses:
                    if response.role == "assistant" and response.id not in processed_message_ids:
                        content = extract_value_from_response(response.content)
                        if content != CONTENT_NOT_FOUND:
                            processed_message_ids.append(response.id)
                            first_line_of_content = content.split("\n")[0]
                            add_message("Assistant: " + first_line_of_content,
                                        initial_time)  # Registrar respuesta del asistente
                            print(first_line_of_content)
                            break  # Salir del ciclo una vez que se ha mostrado la última respuesta
            else:
                print("Run did not complete successfully.")
        else:
            print("Run initiation failed.")

        print("----\n")


def enable_knowledge_retrieval(assistant_id, file_ids):
    try:
        client.beta.assistants.update(
            assistant_id=assistant_id,
            tools=[{"type": "retrieval"}],
            file_ids=file_ids
        )
    except Exception as e:
        logger.error(f"Error enabling knowledge retrieval: {e}")


def attach_file_to_thread(thread_id, file_id, message_content):
    try:
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_content,
            file_ids=[file_id]
        )
    except Exception as e:
        logger.error(f"Error attaching file to thread: {e}")


def check_conversations():
    repo_dir = Path(__file__).resolve().parent / "conversations"
    repo_dir.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)


def ask(nombre_asistente, instrucciones_asistente=DEFAULT_INSTRUCTIONS):
    check_conversations()
    agents_path = Path(AGENTS_FILENAME)
    # agents = load_gpt_agents(agents_path)

    assistant_name, instructions = setup_assistant(agents_path, nombre_asistente, instrucciones_asistente)
    try:
        assistant_id = create_assistant(assistant_name, instructions, code=True)
        thread_id = create_thread(assistant_name, assistant_id)
        ask_user_loop(thread_id, assistant_id, [])
    except Exception as e:
        logger.error(f"Error while setting up {assistant_name}: {e}")


class Agent:
    def __init__(self, name, instructions, model="gpt-4-1106-preview", code=False):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.code = code
        self.assistant_id = create_assistant(self.name, self.instructions)
        self.thread_id = create_thread(self.name, self.assistant_id)

    def get_responses(self):
        messages = client.beta.threads.messages.list(thread_id=self.thread_id)
        return messages.data

    def wait_for_run_completion(self, run_id, timeout=DEFAULT_TIMEOUT):
        start_time = time.time()
        while time.time() - start_time < timeout:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run_id
            )
            if run_status.status == "completed":
                return True
            elif run_status.status in ["failed", "cancelled", "expired"]:
                return False
            time.sleep(5)
        return False

    def run_assistant(self):
        run_response = client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id
        )
        return run_response.id

    def send_message(self, content, role="user"):
        return client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role=role,
            content=content
        )


def main():
    nombre_asistente = "Boss"
    instrucciones_asistente = "As the 'Boss' agent, your role is to manage and oversee various projects, " \
                              "coordinating between different GPT agents ('emissor' and 'receptor') " \
                              "to achieve specific goals. You are responsible for project allocation, " \
                              "monitoring progress, and ensuring efficient communication."

    #  ask(nombre_asistente, instrucciones_asistente)

    boss_agent = Agent(nombre_asistente, instrucciones_asistente, code=True)
    ask_boss_loop(boss_agent)


if __name__ == "__main__":
    main()
