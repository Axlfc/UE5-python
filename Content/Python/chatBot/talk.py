import os
import colorama
import speech_recognition as sr  # pip install SpeechRecognition
import process_system
from datetime import datetime
import subprocess


def start_listening_microphone_input(r):
    with sr.Microphone() as source:
        return r.listen(source)


def convert_speech_to_text(r):
    try:
        if process_system.plat() == "Windows":
            text = r.recognize_google(start_listening_microphone_input(r))
        elif process_system.plat() == "Linux":
            text = r.recognize_google(start_listening_microphone_input(r))
            if subprocess.check_output(['uname', '-o']).strip() == b'Android':
                print("hola")
                c = False
                while True:
                    "Entered Termux voice recognition now"
                    text = subprocess.Popen("termux-speech-to-text", stdout=subprocess.PIPE)
                    c = text.stdout.readline()
                    res = c.replace("\n", "")
                    print(colorama.Fore.CYAN)
                    print("-" * 30)
                    if res == 'stop':
                        break
                        sys.exit()
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print(f"Error processing request: {e}")


def main():
    python = process_system.main()
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    while True:
        print(colorama.Fore.RED + "Say something:" + colorama.Fore.CYAN)
        r = sr.Recognizer()

        if process_system.plat() == "Windows":
            # r.wait_for_silence(source, timeout=float("inf"))
            start_listening_microphone_input(r)
        elif process_system.plat() == "Linux":
            if subprocess.check_output(['uname', '-o']).strip() == b'Android':
                pass
            else:
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


if __name__ == '__main__':
    main()
