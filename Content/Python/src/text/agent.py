import os
import sys
import time
import platform
from datetime import datetime
from pathlib import Path
import json

import requests
import yaml
import logging
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from File import File

# Global flag to determine which model to use
USE_OPENAI = True

content_path = Path('../../../../../UE5-python')
sys.path.append(str(content_path))

from Content.Python_dependencies.latest_openai import openai


# Constants
MODEL = "gpt-4-1106-preview"

ASSISTANTS_DATA_FILENAME = 'assistants_data.json'
DEFAULT_TIMEOUT = 120
CONTENT_NOT_FOUND = "Content not found."
AGENTS_FILENAME = 'agents.yml'
LOG_FORMAT = "%(levelname)s: %(asctime)s - %(message)s"
DEFAULT_INSTRUCTIONS = "You are a default Assistant agent."
BOSS_INSTRUCTIONS = "As the 'Boss' agent, your role is to manage and oversee various projects, " \
                              "coordinating between different GPT agents ('emissor' and 'receptor') " \
                              "to achieve specific goals. You are responsible for project allocation, " \
                              "monitoring progress, and ensuring efficient communication."

# Configure logging
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Load your OpenAI API key from .env file
dotenv_path = Path('../bot/.env')
load_dotenv(dotenv_path=dotenv_path)
# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class AbstractAgent(ABC):
    def __init__(self, name, instructions, model=MODEL, code=False, use_openai=True):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.code = code
        self.assistant_id = self.create_assistant(code=code)
        self.thread_id = self.create_thread()
        self.save_assistant_data()  # Save the data after both IDs are assigned
        self.processed_message_ids = []
        self.use_openai = use_openai  # Flag to determine which model to use

    @abstractmethod
    def get_all_responses(self):
        print(f"Fetching simulated responses for thread {self.thread_id}")
        #messages = client.beta.threads.messages.list(thread_id=self.thread_id)
        #return messages.data
        return [{"id": "mock_resp_id", "content": "Mock response content"}]

    @abstractmethod
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

    @abstractmethod
    def run_assistant(self):
        if self.use_openai:
            # Existing OpenAI logic
            print(f"Simulating running assistant for thread {self.thread_id} and assistant {self.assistant_id} with name {self.name}")
            '''run_response = client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id
            )'''
            #return run_response.id

            return "mock_run_id_" + self.thread_id
        else:
            # Refactored logic for local server
            # Assuming there is an endpoint /run_assistant or similar in your local setup
            try:
                response = requests.post(
                    self.client["base_url"] + "/run_assistant",
                    json={"thread_id": self.thread_id, "assistant_id": self.assistant_id},
                    headers={"Authorization": f"Bearer {self.client['api_key']}"}
                )
                run_response = response.json()
                return run_response.get("run_id", "mock_run_id")
            except Exception as e:
                logger.error(f"Error in run_assistant: {e}")
                return "mock_run_id"

    @abstractmethod
    def send_message(self, content, role="user", recipient="assistant"):
        print(f"Simulated sending message: '{content}' from {role} to {recipient} in thread {self.thread_id}")
        '''message = client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role=role,
            content=content
        )'''
        #add_message(content, datetime.now().strftime("%m-%d-%Y_%H-%M-%S"), sender=role, recipient=recipient)
        #return message.id
        return "mock_message_id"

    @abstractmethod
    def load_assistant_data(self):
        try:
            with open(ASSISTANTS_DATA_FILENAME, 'r') as file:
                data = json.load(file)
                return data.get(self.name, {})
        except FileNotFoundError:
            return {}

    @abstractmethod
    def save_assistant_data(self):
        try:
            with open(ASSISTANTS_DATA_FILENAME, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data[self.name] = {'assistant_id': self.assistant_id, 'thread_id': self.thread_id}
        with open(ASSISTANTS_DATA_FILENAME, 'w') as file:
            json.dump(data, file)

    @abstractmethod
    def create_assistant(self, code=False):
        assistant_data = self.load_assistant_data()
        if assistant_data and 'assistant_id' in assistant_data:
            return assistant_data['assistant_id']
        else:
            if self.use_openai:
                tools = [{"type": "code_interpreter"}] if code else []
                try:
                    assistant = client.beta.assistants.create(
                        name=self.name,
                        instructions=self.instructions,
                        tools=tools,
                        model=self.model
                    )
                    self.assistant_id = assistant.id
                except Exception as e:
                    logger.error(f"Error in create_assistant: {e}")
                    return None
            else:
                # Skip OpenAI assistant creation for local agents
                self.assistant_id = "mock_assistant_id_for_" + self.name
            return self.assistant_id

    @abstractmethod
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

    @abstractmethod
    def ask(self, initial_time, nombre_asistente, instrucciones_asistente=DEFAULT_INSTRUCTIONS):
        check_conversations()
        agents_path = Path(AGENTS_FILENAME)
        # agents = load_gpt_agents(agents_path)

        assistant_name, instructions = setup_assistant(agents_path, nombre_asistente, instrucciones_asistente)
        try:
            assistant_id = self.create_assistant(code=True)
            thread_id = self.create_thread()
            self.ask_user_loop(initial_time, thread_id, assistant_id, self.processed_message_ids)
        except Exception as e:
            logger.error(f"Error while setting up {assistant_name}: {e}")

    @abstractmethod
    def create_thread(self):
        assistant_data = self.load_assistant_data()
        if 'thread_id' in assistant_data and assistant_data['thread_id']:
            return assistant_data['thread_id']
        else:
            thread = client.beta.threads.create()
            self.thread_id = thread.id
            return self.thread_id

    @abstractmethod
    def ask_user_loop(self, initial_time, thread_id, assistant_id, processed_message_ids):
        while True:
            user_question = input("Enter your question (or type 'exit' to quit): ")
            if user_question.lower() == 'exit':
                break

            self.send_message(user_question, "user")
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

    @abstractmethod
    def agent_to_agent_communication(self, initial_time, sender_agent, receiver_agent, message, processed_message_ids):
        sender_agent.send_message(message)
        run_id = sender_agent.run_assistant()

        if sender_agent.wait_for_run_completion(run_id):
            responses = sender_agent.get_all_responses()
            for response in responses:
                if response.id not in processed_message_ids:
                    # Assuming response.content is a list of MessageContentText objects
                    response_texts = [resp.text.value for resp in response.content if
                                      hasattr(resp, 'text') and hasattr(resp.text, 'value')]
                    response_content = " ".join(response_texts)  # Concatenate all texts
                    print(f"{sender_agent.name} to {receiver_agent.name}: {response_content}")
                    processed_message_ids.append(response.id)
                    add_message(response_content, initial_time, sender=sender_agent.name,
                                     recipient=receiver_agent.name)

                    return response_content
        else:
            print(f"{sender_agent.name} run did not complete successfully.")
            return None


class OpenAIAgent(AbstractAgent):
    def __init__(self, name, instructions, model=MODEL, code=False, use_openai=True):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        super().__init__(name, instructions, model, code, use_openai)
        self.assistant_id = self.create_assistant(code=code)
        self.thread_id = self.create_thread()
        self.save_assistant_data()


class LocalAgent(AbstractAgent):
    def __init__(self, name, instructions, model=MODEL, code=True, use_openai=False):
        self.client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
        super().__init__(name, instructions, model, code, use_openai)
        self.assistant_id = self.create_assistant(code=code)
        self.thread_id = self.create_thread()
        self.save_assistant_data()

    def process_input_alternative(self, input_data):
        # Logic for processing input with the alternative model
        if not self.use_openai:
            try:
                history = [
                    {"role": "system", "content": "You are an intelligent assistant."},
                    {"role": "user", "content": input_data}
                ]

                completion = self.client.chat.completions.create(
                    model="local-model",  # Use the appropriate model name for the local server
                    messages=history,
                    temperature=0.7,
                    stream=True,
                )

                new_message = {"role": "assistant", "content": ""}
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        new_message["content"] += chunk.choices[0].delta.content

                return new_message
            except Exception as e:
                logger.error(f"Error in process_input_alternative: {e}")
                return {"error": str(e)}

    def ask(self, initial_time, nombre_asistente, instrucciones_asistente=DEFAULT_INSTRUCTIONS):
        return super().ask(initial_time, nombre_asistente, instrucciones_asistente)

    def agent_to_agent_communication(self, initial_time, sender_agent, receiver_agent, message, processed_message_ids):
        return super().agent_to_agent_communication(initial_time, sender_agent, receiver_agent, message,
                                                    processed_message_ids)

    def ask_user_loop(self, initial_time, thread_id, assistant_id, processed_message_ids):
        return super().ask_user_loop(initial_time, thread_id, assistant_id, processed_message_ids)

    def create_assistant(self, code=False):
        return super().create_assistant(code)

    def create_thread(self):
        return super().create_thread()

    def get_all_responses(self):
        return super().get_all_responses()

    def load_assistant_data(self):
        return super().load_assistant_data()

    def run_assistant(self):
        return super().run_assistant()

    def save_assistant_data(self):
        return super().save_assistant_data()

    def send_message(self, content, role="user", recipient="local"):
        return super().send_message(content, role=role, recipient=recipient)

    def setup_all_agents(self, agents_path):
        return super().setup_all_agents(agents_path)

    def wait_for_run_completion(self, run_id, timeout=DEFAULT_TIMEOUT):
        return super().wait_for_run_completion(run_id, timeout)

    def process_input(self, input_data):
        # Implement the specific logic for processing input using the LocalAgent
        try:
            history = [
                {"role": "system", "content": "You are an intelligent assistant."},
                {"role": "user", "content": input_data}
            ]

            completion = self.client.chat.completions.create(
                model=MODEL,  # Replace with the actual model name if necessary
                messages=history,
                temperature=0.7,
                stream=True,
            )

            new_message = {"role": "assistant", "content": ""}
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    new_message["content"] += chunk.choices[0].delta.content

            return new_message
        except Exception as e:
            logger.error(f"Error in process_input: {e}")
            return {"error": str(e)}


class BossAgent(AbstractAgent):
    def __init__(self, name, instructions, model=MODEL, code=False, use_openai=True):
        super().__init__(name, instructions, model, code, use_openai)
        # Project stages and respective agent mappings
        #self.project_stages = {}
        #self.project_stages = {'Stage 1: Idea Generation and Conceptualization': {'agent': 'Creative Consultant', 'instructions': "Assist with brainstorming initial concepts, defining the book's genre, and formulating the core message or theme."}, 'Stage 2: Detailed Research': {'agent': 'Research Specialist', 'instructions': "Conduct in-depth research to provide a strong factual foundation for the book's content, including interviews, archival research, and data collection."}, 'Stage 3: Outline and Structure Development': {'agent': 'Plot Strategist', 'instructions': 'Help create a detailed chapter outline, define plot structure, and plan character development to guide the manuscript writing process.'}, 'Stage 4: Writing the First Draft': {'agent': 'Writing Coach', 'instructions': "Provide support in drafting the manuscript, helping to maintain writing discipline and idea flow, and overcoming writer's block."}, 'Stage 5: Revisions and Developmental Editing': {'agent': 'Developmental Editor', 'instructions': 'Review the first draft for improvements in story structure, pacing, character arcs, and narrative consistency, offering substantial editorial feedback.'}, 'Stage 6: Refinement and Copyediting': {'agent': 'Copy Editor', 'instructions': 'Perform sentence-level editing to improve readability, correct grammar, and ensure style consistency across the manuscript.'}, 'Stage 7: Proofreading': {'agent': 'Proofreading Expert', 'instructions': 'Conduct a final meticulous review of the manuscript to catch any typos, spelling errors, and formatting inconsistencies before publishing.'}, 'Stage 8: Book Design and Production': {'agent': 'Book Designer', 'instructions': 'Design the book cover, develop interior formatting, and prepare the manuscript for print and digital publishing platforms.'}, 'Stage 9: Marketing and Promotion': {'agent': 'Marketing Manager', 'instructions': 'Create and implement a marketing plan that includes pre-launch buzz-building, launch strategy, and post-launch promotion to reach the target audience.'}, 'Stage 10: Publication': {'agent': 'Publishing Advisor', 'instructions': 'Guide through the selection of publishing options, such as traditional, independent, or self-publishing, including navigating distribution channels and platforms.'}, 'Stage 11: Post-Publication Support and Engagement': {'agent': 'Community Relations Specialist', 'instructions': "Manage the book's post-release presence, including reader engagement, social media interaction, book tours, and speaking engagements."}}
        self.project_stages = {'Stage 1: Idea Generation and Conceptualization': {
            'agent': 'Creative Consultant',
            'instructions': "Assist with brainstorming initial concepts, defining the book's genre, and formulating the core message or theme."},
            'Stage 2: Detailed Research': {
                'agent': 'Research Specialist',
                'instructions': "Conduct in-depth research to provide a strong factual foundation for the book's content, including interviews, archival research, and data collection."
            }}
        # Maintain the status of the current project
        self.current_project = None
        self.current_stage = None
        self.current_task = None
        self.stage_progress = {}
        self.agent_registry = {}

    def ask(self, initial_time, nombre_asistente, instrucciones_asistente=DEFAULT_INSTRUCTIONS):
        return super().ask(initial_time, nombre_asistente, instrucciones_asistente)

    def ask_user_loop(self, initial_time, thread_id, assistant_id, processed_message_ids):
        return super().ask_user_loop(initial_time, thread_id, assistant_id, processed_message_ids)

    def ask_boss_loop(self, boss_agent, processed_message_ids):
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

    def agent_to_agent_communication(self, initial_time, sender_agent, receiver_agent, message, processed_message_ids):
        return super().agent_to_agent_communication(initial_time, sender_agent, receiver_agent, message,
                                                    processed_message_ids)

    def wait_for_run_completion(self, run_id, timeout=DEFAULT_TIMEOUT):
        return super().wait_for_run_completion(run_id, timeout)

    def run_assistant(self):
        return super().run_assistant()

    def send_message(self, content, role="user", recipient="assistant"):
        return super().send_message(content, role=role, recipient=recipient)

    def load_assistant_data(self):
        return super().load_assistant_data()

    def save_assistant_data(self):
        return super().save_assistant_data()

    def create_assistant(self, code=False):
        return super().create_assistant(code)

    def setup_all_agents(self, agents_path):
        return super().setup_all_agents(agents_path)

    def create_thread(self):
        return super().create_thread()

    def parse_agent_info(self, task_description):
        boss_response = self.recommend_agent_for_task(task_description)

        if boss_response:
            # Initialize empty variables
            agent_name = ""
            agent_instructions = ""

            try:
                if "Agent Name:" in boss_response and "Instructions:" in boss_response:
                    agent_name_start = boss_response.find("Agent Name;") + len("Agent Name;")
                    agent_instructions_start = boss_response.find("Instructions:")

                    agent_name = boss_response[agent_name_start:agent_instructions_start].strip().replace(":", "")
                    agent_instructions = boss_response[agent_instructions_start + len("Instructions:"):].strip()

                    return agent_name, agent_instructions
                else:
                    print("Response format not recognized.")
            except Exception as e:
                print(f"Error parsing response: {e}")
        else:
            print("No response received from the Boss agent.")

    def get_response_by_id(self, message_id):
        # Retrieve all messages and find the one with the given ID
        all_responses = self.get_all_responses()
        for response in all_responses:
            if response.id == message_id:
                # Assuming the response content is a string with the agent's name
                return extract_value_from_response(response.content)
        return None  # or some default value or error handling

    def get_all_responses(self):
        return super().get_all_responses()

    def retrieve_single_agent_name_and_instructions_of_task(self, task):
        task_description = "Please recommend only an agent for " + task +". Write back only the name and context instructions of the agent."
        new_agent_name, new_agent_instructions = self.parse_agent_info(task_description)

        if new_agent_name and new_agent_instructions:
            return new_agent_name, new_agent_instructions
        else:
            print("Failed to parse agent information.")

    def recommend_agent_for_task(self, task_description):
        # Send a message to the Boss agent
        self.send_message(task_description, role="user")
        run_id = self.run_assistant()

        # Wait for the assistant run to complete
        if self.wait_for_run_completion(run_id):
            responses = self.get_all_responses()
            for response in responses:
                if response.id not in self.processed_message_ids:
                    # Process the response content
                    response_texts = [resp.text.value for resp in response.content if
                                      hasattr(resp, 'text') and hasattr(resp.text, 'value')]
                    response_content = " ".join(response_texts)  # Concatenate all texts

                    # Update processed message IDs to avoid reprocessing the same message
                    self.processed_message_ids.append(response.id)

                    # Return the response content which is the name of the recommended agent
                    return response_content

        else:
            print("Run did not complete successfully.")
            return None

    def recommend_agents_for_task(self, task_description):
        # Send a message to the Boss agent
        self.send_message(task_description, role="user")
        run_id = self.run_assistant()

        recommended_agents = []
        if self.wait_for_run_completion(run_id):
            responses = self.get_all_responses()
            for response in responses:
                if response.id not in self.processed_message_ids:
                    # Assuming response content is a list of agent recommendations
                    response_texts = [resp.text.value for resp in response.content if
                                      hasattr(resp, 'text') and hasattr(resp.text, 'value')]
                    for text in response_texts:
                        if "Agent Name:" in text and "Instructions:" in text:
                            agent_name_start = text.find("Agent Name:") + len("Agent Name:")
                            agent_instructions_start = text.find("Instructions:")
                            agent_name = text[agent_name_start:agent_instructions_start].strip().replace(":", "")
                            agent_instructions = text[agent_instructions_start + len("Instructions:"):].strip()
                            recommended_agents.append((agent_name, agent_instructions))

                    self.processed_message_ids.append(response.id)
        return recommended_agents

    def manage_multiple_agents_task(self, task):
        agents = {}
        task_description = "Please recommend two or more agents for " + task + ". Write back only the name and context instructions of each agent."
        # Retrieve a list of agents for a given task
        agents_info = self.recommend_agents_for_task(task_description)
        for agent_name, instructions in agents_info:
            # Store agent information in the dictionary
            agents[agent_name] = instructions
            # Instantiate the agent
            # agent = AbstractAgent(agent_name, instructions, code=True)  # Replace with actual instantiation logic
            # Send instructions to the agent and handle their responses
        return agents

    def select_agent_for_stage(self, stage):
        # Logic to select the most suitable agent based on the current stage
        agent_candidates = self.project_stages.get(stage, [])
        # Example logic to select an agent (can be more sophisticated based on specific criteria)
        if agent_candidates:
            selected_agent = agent_candidates[0]  # Placeholder for actual selection logic
            return selected_agent
        return None

    def instantiate_agents(self, agents_info):
        for agent_name, instructions in agents_info.items():
            if agent_name not in self.agent_registry:
                # Dynamically create an agent
                new_agent = AbstractAgent(agent_name, instructions, code=True)
                self.agent_registry[agent_name] = new_agent
                # Log agent creation
                logger.info(f"Instantiated agent {agent_name}")

    def instantiate_agents_for_task(self, task):
        # Get recommendations for the task
        task_description = f"Please recommend agents for {task}. " \
                           f"Write back only the name and instructions of each agent. " \
                           f"If only one agent is necessary for the task, only recommend a single agent and its instructions"
        agents_info = self.recommend_agents_for_task(task_description)

        instantiated_agents = {}

        # Iterate through each recommended agent
        for agent_name, instructions in agents_info:
            if agent_name not in self.agent_registry:
                # Instantiate and store the agent if it doesn't exist
                #  TODO: store or ask boss about agent_name instructions
                new_agent = AbstractAgent(agent_name, instructions, code=True)
                self.agent_registry[agent_name] = new_agent
                logger.info(f"Instantiated agent: {agent_name}")
            else:
                logger.info(f"Agent {agent_name} already exists.")

            # Add to the list of instantiated agents
            instantiated_agents[agent_name] = self.agent_registry[agent_name]

        return instantiated_agents

    def assign_task(self, task_description, stage):
        print(f"Assigning task '{task_description}' for stage '{stage}'")
        '''# Instantiate agents for the given task
        agents = self.instantiate_agents_for_task(stage)

        if len(agents) == 1:
            # Assign task to the single agent
            agent_name = next(iter(agents))
            agents[agent_name].send_message(f"Task Assignment: {task_description} (Write finished task when finished: [task_name]", role="boss")
            logger.info(f"Assigned task '{task_description}' to {agent_name}")
        else:
            # Assign tasks to multiple agents and specify inter-agent communication if needed
            for agent_name, agent in agents.items():
                # Assign task
                agent.send_message(f"Task Assignment for {stage}: {task_description}", role="assistant")
                # Inform about necessary communication with other agents
                other_agents = [name for name in agents if name != agent_name]
                agent.send_message(f"Coordinate with: {', '.join(other_agents)}", role="assistant")
                logger.info(f"Assigned task '{task_description}' to {agent_name} with coordination instructions")'''

    def get_agent_description(self, agent_name, yml_file=AGENTS_FILENAME):
        """Retrieve the description for a given agent from the YAML file."""
        with open(yml_file, "r") as file:
            agents_data = yaml.safe_load(file)
            for agent in agents_data.get("agents", []):
                if agent["name"] == agent_name:
                    return agent.get("instructions", "No description available.")
        return "Agent not found."

    def get_or_request_agent_description(self, agent_name):
        # Step 1: Check for existing description
        description = self.get_agent_description(agent_name)
        if description not in ["Agent not found.", "No description available."]:
            return description

        # Step 2: Request description from the 'Boss' agent
        print(f"Requesting description for a new agent: {agent_name}")
        self.send_message(f"Please provide a description for a new agent named {agent_name}.")
        run_id = self.run_assistant()

        if self.wait_for_run_completion(run_id):
            responses = self.get_all_responses()
            for response in responses:
                if response.role == "assistant":
                    new_description = extract_value_from_response(response.content)
                    # Step 3: Save the new description
                    update_agents_yaml(AGENTS_FILENAME, agent_name, new_description)
                    return new_description

        return "Failed to obtain a description from the Boss agent."

    def generate_project_stages(self, project_description):
        """
        Asks the Boss agent to generate project stages and suitable agents for each stage.
        :param project_description: A description or name of the project.
        """
        print("GENERATE PROJECT TRIGGERED")
        # Ask the Boss agent for project stages and agents
        print("Running generate_project_stages for:", project_description)
        self.send_message(f"Generate project stages and agents for: {project_description}", role="user")
        run_id = self.run_assistant()

        print(f"ASSISTANT {self.name} RUNNING")

        if self.wait_for_run_completion(run_id):
            print("WAITING FOR RUN TO COMPLETE")
            responses = self.get_all_responses()
            for response in responses:
                print("Response ID:", response.id)  # Debugging statement
                if response.id not in self.processed_message_ids:
                    print("Processing response:", response.content)  # Debugging statement
                    stages_and_agents = self.interpret_project_stages_response(response.content)
                    #  self.interpret_project_stages_response(response.content)

                    #  Save stages and agents to memory of Boss
                    self.project_stages = stages_and_agents

                    # Update processed message IDs to avoid reprocessing the same message
                    self.processed_message_ids.append(response.id)
                    break  # Once we have processed the response, we can exit the loop

    def interpret_project_stages_response(self, response_content):
        """
        Interprets the response content to extract project stages and corresponding agents.
        :param response_content: The content of the response from the Boss agent.
        :return: A dictionary of project stages and their corresponding agents.
        """
        stages_and_agents = {}

        # Ensure response_content is a list and not empty
        try:
            first_item = response_content[0]

            # Check if first_item is an instance of MessageContentText and has a text attribute
            if hasattr(first_item, 'text') and hasattr(first_item.text, 'value'):
                response_text = first_item.text.value
        except Exception as e:
            logger.error(f"{e}")
            raise ValueError

        # Splitting the response by "Stage" which precedes each stage
        stages = response_text.split("Stage ")[1:]  # Ensure proper splitting

        for stage in stages:
            lines = stage.split("\n")
            if len(lines) >= 3:
                # Extracting stage name, agent name, and instructions
                stage_name = f"Stage {lines[0].strip()}"
                agent_name = lines[1].split("**Agent:**")[1].strip()
                instructions = lines[2].split("**Instructions:**")[1].strip()

                # Print each extracted part for debugging
                print(f"Stage Name: {stage_name}, Agent Name: {agent_name}, Instructions: {instructions}")

                stages_and_agents[stage_name] = {"agent": agent_name, "instructions": instructions}

        # Print the final dictionary before returning
        print("Stages and Agents:", stages_and_agents)
        return stages_and_agents

    def manage_workflow(self, project_description):
        for stage, task_description in project_description.items():
            self.assign_task(task_description, stage)
            all_tasks_completed = False

            while not all_tasks_completed:
                # Check for task completion from all agents
                completed_tasks = []
                for response in self.get_all_responses():
                    task_desc = self.check_task_completion(response.content)
                    if task_desc:
                        completed_tasks.append(task_desc)

                # Verify if all tasks for the stage are completed
                all_tasks_completed = len(completed_tasks) == len(self.agent_registry)
                if not all_tasks_completed:
                    # Handle dependencies, adjustments, and agent coordination
                    pass

            logger.info(f"All tasks for stage '{stage}' completed.")

    def update_progress(self, stage, task, status):
        if stage not in self.stage_progress:
            self.stage_progress[stage] = {}
        self.stage_progress[stage][task] = status

    def check_task_completion(self, response):
        if "Finished task" in response:
            task_desc = response.split("Finished task: ")[1]
            return task_desc
        return None

    def manage_stage(self, stage, instructions):
        print(f"Managing stage: {stage} with instructions: {instructions}")

        # Manage a particular stage of the project
        '''agent_name = self.select_agent_for_stage(stage)
        if not agent_name:
            print(f"No agent found for stage: {stage}")
            return None

        # Instantiate the agent (you need to have a mechanism to do this, e.g., a factory method)
        agent = AbstractAgent(agent_name, instructions, code=True)  # Replace this with actual instantiation

        # Send instructions to the agent and wait for completion
        agent.send_message(instructions)
        run_id = agent.run_assistant()
        if agent.wait_for_run_completion(run_id):
            responses = agent.get_all_responses()
            # Assuming last response is the final report
            final_report = responses[-1] if responses else None
            return final_report
        else:
            print(f"Stage {stage} did not complete successfully.")
            return None'''

    def simulate_project_stages(self):
        for stage, stage_info in self.project_stages.items():
            agent_name = stage_info['agent']
            instructions = stage_info['instructions']
            print(f"\nStage: {stage}")
            print(f"Agent: {agent_name}")
            print(f"Instructions: {instructions}")

            # Simulate sending task to agent
            self.assign_task(instructions, stage)
            # Wait for completion or simulate response
            # This part can be expanded based on how you manage agent responses
            print(f"Task for {stage} assigned to {agent_name}.")

            # Check for task completion (you can implement this as per your system's logic)
            if self.check_task_completion(stage):
                print(f"Task for {stage} completed by {agent_name}.")
            else:
                print(f"Task for {stage} is still ongoing.")

    def run_project(self, project_description):
        print(f"Starting project: {project_description}")

        # Start a new project
        '''self.current_project = project_description
        print(f"Starting project: {project_description}")

        # Iterate over each stage in the project
        for stage, instructions in project_description.items():
            print(f"Managing stage: {stage}")
            report = self.manage_stage(stage, instructions)
            if report:
                print(f"Stage {stage} completed. Report: {report}")
            else:
                print(f"Stage {stage} failed or incomplete.")
                break  # Exit if any stage fails

        print("Project completed")'''


class AgentFactory:
    def create_agent(self, agent_type, name, instructions, model=MODEL, code=False, use_openai=True):
        if agent_type == "local":
            print("CREATING LOCAL AGENT")
            return LocalAgent(name, instructions, model, code, use_openai)
        elif agent_type == "boss":
            return BossAgent(name, instructions, model, code, use_openai)
        # TODO: elif agent_type == "assistant":
            # return AbstractAgent(name, instructions, model, code, use_openai)
        elif agent_type == "openai":
            return OpenAIAgent(name, instructions, model, code)
        else:
            raise ValueError("Unknown agent type")


def add_message(message, initial_time, sender="user", recipient="assistant"):
    now = datetime.now()
    time_str = now.strftime("%H-%M-%S")
    date = now.strftime("%Y-%m-%d")
    repo_dir = os.path.join(os.path.abspath(__file__)[:-9].split("\n")[0], "conversations")
    directory = repo_dir + "\\" if platform.system() == "Windows" else repo_dir + "/"
    filepath = f"{directory}{date}/{initial_time}.txt"

    if not os.path.exists(directory + date):
        os.makedirs(directory + date)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"{time_str} - From {sender} to {recipient}: {message.strip()}\n")


def load_assistant_id_by_name(assistant_name, file_path=ASSISTANTS_DATA_FILENAME):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(assistant_name)
    except FileNotFoundError:
        return None


def run_assistant(thread_id, assistant_id):
    run_response = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    run_id = run_response.id
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


def update_agents_yaml(yml_file, agent_name, instructions):
    # Read existing agents
    with open(yml_file, 'r') as file:
        agents_data = yaml.safe_load(file) or {'agents': []}

    # Append new agent if it doesn't already exist
    if not any(agent['name'] == agent_name for agent in agents_data['agents']):
        new_agent = {
            'name': agent_name,
            'instructions': instructions
        }
        agents_data['agents'].append(new_agent)

        # Write updated agents back to file with proper formatting
        with open(yml_file, 'w') as file:
            yaml.dump(agents_data, file, default_flow_style=False, sort_keys=False)


def setup_assistant(yml_file, assistant_name="Assistant", default_instructions=""):
    instructions = search_agent_by_name(assistant_name, load_gpt_agents(yml_file))

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


def set_up_agent(factory, agent_role, agent_name, instructions, use_openai=True):
    return factory.create_agent(agent_role, agent_name, instructions, use_openai)


def main():
    agent_factory = AgentFactory()

    #  boss_agent_role = "boss"
    #  boss_agent_name = "Boss"

    #  boss_agent = set_up_agent(agent_factory, boss_agent_role, boss_agent_name, BOSS_INSTRUCTIONS, use_openai=True)

    #  processed_message_ids = []
    #  boss_agent.ask_boss_loop(boss_agent, processed_message_ids)

    # agents_for_task = boss_agent.manage_multiple_agents_task("book writing")

    '''for agent_name, instructions in agents_for_task.items():
        print(f"Agent Name: {agent_name}\nInstructions: {instructions}\n")'''

    #  boss_agent.generate_project_stages("book writing")

    #  boss_agent.simulate_project_stages()

    # Example: Creating an agent that uses a non-OpenAI model
    alternative_agent = set_up_agent(agent_factory, "local", "Wizard", DEFAULT_INSTRUCTIONS, False)

    main_chat_loop(alternative_agent.client)

    # Process input (can be text or a file path)
    # input_data = "text.txt"  # or some text input
    # response = alternative_agent.process_input(input_data)
    # print(response)


def main_chat_loop(client):
    history = [
        {"role": "system", "content": DEFAULT_INSTRUCTIONS},
        {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
    ]

    while True:
        new_message = process_chat_completions(client, history)
        history.append(new_message)

        # Uncomment to see chat history
        # import json
        # gray_color = "\033[90m"
        # reset_color = "\033[0m"
        # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
        # print(json.dumps(history, indent=2))
        # print(f"\n{'-'*55}\n{reset_color}")

        print()
        user_input = input("> ")
        if user_input.strip():
            history.append({"role": "user", "content": user_input})


def process_chat_completions(client, history):
    completion = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    return new_message


if __name__ == "__main__":
    main()
