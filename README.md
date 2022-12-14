# UE5-python
🐍
Let's test this Python-Unreal Engine 5 thing for Video Game Production Management!

Project Settings -> Plugins -> Python and enable developer mode.

# chatBot
For running it on Windows or Android (Termux App) follow the section Manual Installation down on this post. 

- Install it on GNU/Linux (Easiest way)

<code>sudo apt-get install -y git python3 build-essential portaudio19-dev</code>
 
<code>git clone https://github.com/AleixMT/Linux-Auto-Customizer</code>

<code>cd Linux-Auto-Customizer</code>

<code>git checkout chatGPT_feature</code>

<code>bash src/core/install.sh -v -o chatGPT</code>

Get your openAI API key (Go to [openai webpage](https://beta.openai.com/account/api-keys) to get yours)

Change 'your_API_key_value' to the one you got from openai webpage before running the next command:

<code>echo "OPENAI_API_KEY=your_API_key_value" > ~/.customizer/bin/chatGPT/Content/Python/chatBot/.env</code>

<code>bash</code>

That's it, now just type **chatGPT** in the console and magic happens.

Use 'exit' or 'quit' words to end the conversation.

<code>chatGPT</code>

<center><img src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4b5d17paxtu21mc9rdo2.jpg" width=200px></img></center>

You can use **talkGPT** (but not yet in Android) to talk to the console and the AI will respond using a custom voice too.

<code>talkGPT</code>

#### TODO (known bugs):
* Voice to text recognizement & pytorch install seems not to work in Android (Termux)
* real-time history for conversate.py and talk.py

Also you can generate code using the function **codeGPT** to generate code when commentaries are passed to it.

Example:

<code>codeGPT "# Python3  # A code to store a list of dictionaries of fruits and vegetables"</code>

A string can also be passed to chatGPT and talkGPT and it will only run that line. Put the text in between matching "" quotes.

<code>chatGPT "Kant vs. Nietzsche. Give me a well formatted table containing relationships of similarity and opposite thoughts on the deepest issues of their careers and thoughts on philosophy topic, in a json format so I can import it to python. With that json file, tell me proportionally in what they agree in a percentage, and form that percentages, only show me one which resumes all the other percentages to I only have a total percentage of agreement they had overall they careers and explain to me why it's overall pertentage is what it is. Specify more information on the topics they disagree and show quotes of them
to prove it"</code>

<code>talkGPT "Tell me any playing card"</code>


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

## talkGPT

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

## codeGPT

If you only want the AI to generate code for you, use the script code.py and pass some commented code to it and it will reply creating code for you!

GNU/Linux & Termux (Android):

<code>python3 code.py "# Python3  # A code to store a list of dictionaries of fruits and vegetables"</code>

Windows:

<code>python code.py "# Python3  # A code to store a list of dictionaries of fruits and vegetables"</code>

<center><img src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ht3n6gzwq3r9w9721dq3.png"></img></center>

There are more scripts inside the chatBot folder, you can check them out too.

# twitterBot

Twitter stuff
(API bot)
(Scraping engine)

# redditBot

Reddit stuff
(API bot)
(Scraping engine)

#### TODO:
* Convince Reddit to un-ban me 😉

# HoudiniFX

Test script with hython3.9.exe from Houdinit's folder.
<code>hython3.9.exe houdini.py</code>

# Blender

Nothing yet
