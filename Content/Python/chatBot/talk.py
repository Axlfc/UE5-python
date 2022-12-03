import os
import colorama
import speech_recognition as sr


def start_listening_microphone_input(r):
    with sr.Microphone() as source:
        print("Say something:")
        return r.listen(source)


def convert_speech_to_text(r):
    try:
        text = r.recognize_google(start_listening_microphone_input(r))
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print(f"Error processing request: {e}")


def main():
    while True:
        r = sr.Recognizer()
        # r.wait_for_silence(source, timeout=float("inf"))
        start_listening_microphone_input(r)
        text = convert_speech_to_text(r)
        print("You said: " + text)
        if text == "exit" or text == "quit":
            exit(0)
        command = "python plot.py \"" + str(text) + "\""
        print(colorama.Fore.YELLOW)
        os.system(command)
        print(colorama.Fore.RESET)


if __name__ == '__main__':
    main()
