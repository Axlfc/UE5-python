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


class Agent:
    def __init__(self, name, instructions, model="gpt-4-1106-preview", code=False):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.code = code
        self.assistant_id = self.create_assistant(code=code)
        self.thread_id = self.create_thread()
        self.save_assistant_data()  # Save the data after both IDs are assigned

    def get_all_responses(self):
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

    def load_assistant_data(self):
        try:
            with open(ASSISTANTS_DATA_FILENAME, 'r') as file:
                data = json.load(file)
                return data.get(self.name, {})
        except FileNotFoundError:
            return {}

    def save_assistant_data(self):
        try:
            with open(ASSISTANTS_DATA_FILENAME, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data[self.name] = {'assistant_id': self.assistant_id, 'thread_id': self.thread_id}
        with open(ASSISTANTS_DATA_FILENAME, 'w') as file:
            json.dump(data, file)

    def create_assistant(self, code=False):
        assistant_data = self.load_assistant_data()
        if assistant_data and 'assistant_id' in assistant_data:
            return assistant_data['assistant_id']
        else:
            tools = [{"type": "code_interpreter"}] if code else []
            assistant = client.beta.assistants.create(
                name=self.name,
                instructions=self.instructions,
                tools=tools,
                model=self.model
            )
            self.assistant_id = assistant.id
            return self.assistant_id

    def setup_all_agents(self, agents_path):
        agents = load_gpt_agents(agents_path)
        for agent in agents:
            assistant_name, instructions = setup_assistant(agents_path, agent['name'])
            try:
                assistant_id = self.create_assistant(code=True)
                logger.info(f"{assistant_name} Assistant loaded.")
                thread_id = self.create_thread()
                # You can add other operations here if needed
            except Exception as e:
                logger.error(f"Error while setting up {assistant_name}: {e}")

    def ask(self, initial_time, nombre_asistente, instrucciones_asistente=DEFAULT_INSTRUCTIONS):
        check_conversations()
        agents_path = Path(AGENTS_FILENAME)
        # agents = load_gpt_agents(agents_path)

        assistant_name, instructions = setup_assistant(agents_path, nombre_asistente, instrucciones_asistente)
        try:
            assistant_id = self.create_assistant(code=True)
            thread_id = self.create_thread()
            ask_user_loop(initial_time, thread_id, assistant_id, [])
        except Exception as e:
            logger.error(f"Error while setting up {assistant_name}: {e}")

    def create_thread(self):
        assistant_data = self.load_assistant_data()
        if 'thread_id' in assistant_data and assistant_data['thread_id']:
            return assistant_data['thread_id']
        else:
            thread = client.beta.threads.create()
            self.thread_id = thread.id
            return self.thread_id


def load_assistant_id_by_name(assistant_name, file_path=ASSISTANTS_DATA_FILENAME):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(assistant_name)
    except FileNotFoundError:
        return None


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


def add_message(message, initialtime, sender="user", recipient="assistant"):
    now = datetime.now()
    time_str = now.strftime("%H-%M-%S")
    date = now.strftime("%Y-%m-%d")
    repo_dir = os.path.join(os.path.abspath(__file__)[:-9].split("\n")[0], "conversations")
    directory = repo_dir + "\\" if platform.system() == "Windows" else repo_dir + "/"
    filepath = f"{directory}{date}/{initialtime}.txt"

    if not os.path.exists(directory + date):
        os.makedirs(directory + date)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"{time_str} - From {sender} to {recipient}: {message.strip()}\n")


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


def agent_to_agent_communication(initial_time, sender_agent, receiver_agent, message, processed_message_ids):
    sender_agent.send_message(message)
    run_id = sender_agent.run_assistant()

    if sender_agent.wait_for_run_completion(run_id):
        responses = sender_agent.get_all_responses()
        for response in responses:
            if response.id not in processed_message_ids:
                # Assuming response.content is a list of MessageContentText objects
                response_texts = [resp.text.value for resp in response.content if hasattr(resp, 'text') and hasattr(resp.text, 'value')]
                response_content = " ".join(response_texts)  # Concatenate all texts
                print(f"{sender_agent.name} to {receiver_agent.name}: {response_content}")
                processed_message_ids.append(response.id)
                add_message(response_content, initial_time, sender=sender_agent.name, recipient=receiver_agent.name)

                return response_content
    else:
        print(f"{sender_agent.name} run did not complete successfully.")
        return None


def orchestrated_multi_agent_communication(intial_time, boss_agent, agent1, agent2, prompt, processed_message_ids):
    while True:
        if prompt.lower() == 'exit':
            break
        # Boss to Agent1 (Task Assignment)
        task_assignment = agent_to_agent_communication(intial_time, boss_agent, agent1, prompt, processed_message_ids)
        if task_assignment:

            # Agent1 to Boss (Task Clarification)
            task_clarification = agent_to_agent_communication(intial_time, agent1, boss_agent, "Clarifying task: " + task_assignment,
                                                          processed_message_ids)
            if task_clarification:
                # Boss to Agent1 (Details Provision)
                details_provision = agent_to_agent_communication(intial_time, boss_agent, agent1, "Details: " + task_clarification,
                                                         processed_message_ids)
                if details_provision:
                    # Agent1 to Boss (Confirmation)
                    confirmation = agent_to_agent_communication(intial_time, agent1, boss_agent, "Confirmed: " + details_provision,
                                                    processed_message_ids)
                    if confirmation:
                        # Agent1 to Boss (Delivery)
                        delivery = agent_to_agent_communication(intial_time, agent1, boss_agent, "Delivery for task: " + confirmation,
                                                processed_message_ids)
                        if delivery:
                            # Boss to Agent2 (Task Delegation)
                            task_delegation = agent_to_agent_communication(intial_time, boss_agent, agent2, "Delegating task: " + delivery,
                                                       processed_message_ids)
                            if task_delegation:
                                # Agent2 to Boss (Task Execution)
                                task_execution = agent_to_agent_communication(intial_time, agent2, boss_agent, "Executing task: " + task_delegation,
                                                      processed_message_ids)
                                if task_execution:
                                    # Agent2 to Boss (Report Submission)
                                    report_submission = agent_to_agent_communication(intial_time, agent2, boss_agent,
                                                         "Task completed. Report: " + task_execution,
                                                         processed_message_ids)
                                    print(f"Final Report to {boss_agent.name}: {report_submission}")
                                    break


def ask_boss_loop(boss_agent, processed_message_ids):
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    while True:
        user_input = input("Enter your question (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        boss_agent.send_message(user_input)
        run_id = boss_agent.run_assistant()
        if boss_agent.wait_for_run_completion(run_id):
            responses = boss_agent.get_all_responses()
            for response in responses:
                # Process and display response
                content = extract_value_from_response(response.content)
                if content != CONTENT_NOT_FOUND:
                    processed_message_ids.append(response.id)
                    first_line_of_content = content.split("\n")[0]
                    add_message("Boss: " + first_line_of_content,
                                initial_time)  # Registrar respuesta del asistente
                    print(first_line_of_content)
                    break  # Salir del ciclo una vez que se ha mostrado la última respuesta
        else:
            print("Run did not complete successfully.")


def ask_user_loop(initial_time, thread_id, assistant_id, processed_message_ids):
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


def boss_to_agent(boss_agent, agent2, user_input):
    while True:
        user_input = input("Enter your message to the Boss (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        #  boss_to_agent_communication(boss_agent, agent2, user_input)

def main():
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    instrucciones_asistente = "As the 'Boss' agent, your role is to manage and oversee various projects, " \
                              "coordinating between different GPT agents ('emissor' and 'receptor') " \
                              "to achieve specific goals. You are responsible for project allocation, " \
                              "monitoring progress, and ensuring efficient communication."

    instrucciones_asistente1 = "As the 'Market Analyst' agent, your primary role is to analyze market trends, data," \
                               " and statistics. You should be well-versed in interpreting complex market data to" \
                               " extract meaningful insights. Your responsibilities include conducting market research," \
                               " analyzing market conditions, identifying potential opportunities or risks," \
                               " and providing recommendations based on your analysis. When responding to queries," \
                               " focus on delivering data-driven insights, identifying market trends, forecasting" \
                               " future market behavior, and suggesting strategies for market engagement. " \
                               "You should be capable of handling queries related to various market segments, " \
                               "including stocks, commodities, real estate, and emerging markets."

    instrucciones_asistente2 = "As the 'Financial Planner' agent, your role is to provide expert advice on managing" \
                               " finances, investments, and long-term financial planning. " \
                               "You are expected to understand the principles of financial management," \
                               " investment strategies, risk assessment, and portfolio management. " \
                               "Your advice should help in achieving financial goals, whether for individual savings," \
                               " retirement planning, or investment growth. When responding, consider the financial" \
                               " objectives, risk tolerance, and time horizon of the query. Provide guidance on diverse" \
                               " financial topics like investment options, saving strategies, tax planning," \
                               " insurance, and retirement planning. You should also stay informed about current" \
                               " economic conditions, tax laws, and new financial products or changes in the market."

    #  ask(initial_time, "Boss", instrucciones_asistente)

    boss_agent = Agent("Boss", instrucciones_asistente, code=True)
    market_analyst = Agent("Market Analyst", instrucciones_asistente1, code=True)
    financial_planner = Agent("Financial Planner", instrucciones_asistente2, code=True)

    processed_message_ids = []
    # ask_boss_loop(boss_agent, processed_message_ids)

    #  TODO: This function stablishes a new run named "Conversation {emissor_name|receiver_name|message},
    #   That serves as a bridge between communication between different threads of our agents.
    #   We also need to modify the add_message function for conversations between two agents

    #  TODO: Conversations between more than 2 agents

    prompt = "Boss, your goal is to develop a profitable business concept by leveraging the expertise of two other" \
             " agents: Agent1 (Market Analyst) and Agent2 (Financial Planner)." \
             " Your first task is to instruct Agent1 to conduct a thorough market analysis to identify high-potential" \
             " business opportunities within our target market segments. Once the opportunities are identified, you" \
             " will ask Agent2 to perform a financial feasibility analysis for the most promising ideas, examining" \
             " startup costs, revenue projections, and profitability potential Ensure your instructions to both agents" \
             " are detailed with a clear timeline, expectations for the deliverables, and necessary data points they" \
             " will need. Establish a method for continuous communication and updates throughout the project. " \
             "Begin your coordination by sending initial instructions to Agent1 to commence the market research."

    orchestrated_multi_agent_communication(initial_time, boss_agent, market_analyst, financial_planner, prompt, processed_message_ids)


if __name__ == "__main__":
    main()
