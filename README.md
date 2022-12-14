# UE5-python
🐍
Let's test this Python-Unreal Engine 5 thing for Video Game Production Management!

Project Settings -> Plugins -> Python and enable developer mode.

# chatBot

- Install it on GNU/Linux (Easiest way)

<code>sudo apt-get install -y git</code>
 
<code>git clone https://github.com/AleixMT/Linux-Auto-Customizer</code>

<code>cd Linux-Auto-Customizer</code>

<code>git checkout chatGPT_feature</code>

<code>bash src/core/install.sh -v -o chatGPT</code>

Get your openAI API key (Go to [openai webpage](https://beta.openai.com/account/api-keys) to get yours)

Create a new file (named .env) inside ~/.customizer/bin/chatGPT/Content/Python/chatBot folder containing:

OPENAI_API_KEY=your_API_key_valueblablablah

Save and close the .env file.

That's it, now after opening a new terminal just type **chatGPT** in the console.

## chatBot manual installation

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

- Edit .env file from the **chatBot** repository folder and paste your API Key to set the variable OPENAI_API_KEY

- Run conversate.py to begin to conversate with the AI locally on your terminal.

GNU/Linux & Termux (Android):

<code>python3 conversate.py</code>

Windows:

<code>python conversate.py</code>

- Use exit or quit words to end the conversation.

If you want the AI to talk to you using a concrete voice, you should try running talk.py script which is used to make the AI process an audio file of their response, for the moment voice chat works only on Windows or GNU/Linux:

- Install portaudio

GNU/Linux:

<code>sudo apt-get install -y build-essential portaudio19-dev</code>

- Install the required Python dependencies and it should work:

GNU/Linux:

<code>pip3 install git+https://github.com/openai/whisper.git jiwer gitpython gdown pathlib setuptools pyaudio soundfile pathlib numpy librosa SpeechRecognition langdetect googletrans==4.0.0-rc1</code>

Windows:

<code>pip install git+https://github.com/openai/whisper.git jiwer gitpython gdown pathlib setuptools pyaudio soundfile pathlib numpy librosa SpeechRecognition langdetect googletrans==4.0.0-rc1</code>

Run talk.py to begin to talk with the AI locally on your terminal, the voice will process and then played.

GNU/Linux:

<code>python3 talk.py</code>

Windows:

<code>python talk.py</code>

Voice processing in talk.py script isn't able to mantain a conversation (almost) real time with the ChatGPT AI due to long audio processing time, but it is definitely possible.

#### TODO (known bugs):
* Voice to text recognizement & pytorch install seems not to work in Android (Termux)


# twitterBot

Twitter stuff

# redditBot

Reddit stuff

# HoudiniFX

Test script

# Blender

Nothing yet
