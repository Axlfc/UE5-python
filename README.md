# UE5-python
🐍
Let's test this Python-Unreal Engine 5 thing for Video Game Production Management!

Project Settings -> Plugins -> Python and enable developer mode.

# chatBot


- Install Python3 and Git

GNU/Linux:

<code>sudo apt-get install -y python3 git</code>

Termux (Android):

<code>pkg install -y root-repo</code>

<code>pkg update -y</code>

<code>pkg upgrade -y</code>

<code>apt install -y git build-essential python3</code>

- Install Python dependencies

GNU/Linux:

<code>pip3 install openai python-dotenv transformers colorama</code>

Windows:

<code>pip install openai python-dotenv transformers colorama</code>

Termux (Android):

<code>MATHLIB="m" pip3 install numpy openai</code>

<code>pip3 install wheel setuptools python-dotenv colorama</code>

- Clone git repository

<code>git clone https://github.com/Axlfc/UE5-python</code>

- Navigate to Content/Python/chatBot repository directory

- Log into openAI web page and get your API key.

- Edit .env file from the repository folder and paste your API Key to set the variable OPENAI_API_KEY

- Run conversate.py to begin to conversate with the AI locally on your terminal.

GNU/Linux & Termux (Android):

<code>python3 conversate.py</code>

Windows:

<code>python conversate.py</code>

- Use exit or quit words to end the conversation.

# twitterBot
