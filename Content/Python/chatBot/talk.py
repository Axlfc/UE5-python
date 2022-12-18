import os
import colorama
import speech_recognition as sr  # pip install SpeechRecognition
import process_system
from datetime import datetime
import subprocess
import sys
import magic  # pip install python-magic
import translator as translate
import subprocess


def start_listening_microphone_input(r):
    # Use the device with index 0 as the input device
    with sr.Microphone(device_index=0) as source:
        return r.listen(source)

    # Use the device with the specified name as the input device
    with sr.Microphone(device_name="My Microphone") as source:
        return r.listen(source)

    # List the available input devices and choose the one you want to use
    print("Available input devices:")
    for i, device_name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{i}: {device_name}")

    device_index = int(input("Enter the index of the device you want to use: "))

    # Use the selected device as the input device
    with sr.Microphone(device_index=device_index) as source:
        return r.listen(source)


def convert_speech_to_text(r):
    try:
        text = r.recognize_google(start_listening_microphone_input(r))
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print(f"Error processing request: {e}")
    except OSError:
        print("Wait, Termux??")


def talk():
    python = process_system.main()
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    while True:
        print(colorama.Fore.RED + "Say something:" + colorama.Fore.CYAN)
        r = sr.Recognizer()

        # r.wait_for_silence(source, timeout=float("inf"))
        start_listening_microphone_input(r)
        text = convert_speech_to_text(r)

        if text:
            print("Converting your voice to text...")

        if text == "exit" or text == "quit":
            exit(0)
        elif type(text) == "NoneType" or str(text) == "None" or text == "none" or text == "":
            pass
        else:
            print("You said: " + colorama.Fore.RED + str(text))
            command = python + " plot.py \"" + str(text) + "\"" + " \"" + initial_time + "\""
            print(colorama.Fore.YELLOW)
            os.system(command)
            print(colorama.Fore.RESET)


def main():
    if len(sys.argv) > 1:
        python = process_system.main()
        initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        try:
            if sys.argv[1].split(".")[1] == "wav":
                lang = translate.detect(sys.argv[1])
                command = [python, "translator.py", sys.argv[1], lang]
                text = subprocess.check_output(command).decode("utf-8")
                print("You said: " + colorama.Fore.RED + str(text))
        except:
            text = sys.argv[1]

        if text == "exit" or text == "quit":
            exit(0)
        elif type(text) == "NoneType" or str(text) == "None" or text == "none" or text == "":
            pass
        else:
            command = python + " plot.py \"" + str(text) + "\"" + " \"" + initial_time + "\""
            print(colorama.Fore.YELLOW)
            os.system(command)
            print(colorama.Fore.RESET)
    else:
        talk()


if __name__ == '__main__':
    main()
