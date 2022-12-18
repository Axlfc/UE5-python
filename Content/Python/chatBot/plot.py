import bot
import os
import sys
import translator as translate
import process_system
import conversate
import colorama
import voice_cloning as voice


def main():
    python = process_system.main()
    repo_dir = os.path.join(os.getcwd().split("\n")[0], "voiceCloning")
    if not os.path.exists(repo_dir):
        voice.initialize_voice_repo(repo_dir)
    conversate.add_message(sys.argv[1], sys.argv[2])
    lang = translate.detect(sys.argv[1])
    botanswer = bot.bot(sys.argv[1]).strip()
    original_bot_answer = botanswer

    if not lang == "en":
        botanswer = translate.text_process(botanswer, "en")
    botanswernojumplines = botanswer.replace('\n', ' ')
    botvoice = "bella.wav"

    command = python + " voice_cloning.py \"" + str(botanswernojumplines) + "\"" + " \"" + botvoice + "\""
    os.system(command)
    if process_system.plat() == "Windows":
        filename = repo_dir + "\\" + "outputs" + "\\" + botanswernojumplines[:20].replace(" ", "_").replace(",", "").replace(".", "").replace("'", "").replace(":", "") + ".wav"
    else:
        filename = repo_dir + "/" + "outputs" + "/" + botanswernojumplines[:20].replace(" ", "_").replace(",", "").replace(".", "").replace("'", "").replace(":", "") + ".wav"

    print()
    print(colorama.Fore.GREEN)
    print(original_bot_answer + colorama.Fore.RESET)
    conversate.add_message(original_bot_answer, sys.argv[2])
    voicecommand = python + " playaudio.py " + filename
    os.system(voicecommand)
    os.remove(filename)


if __name__ == '__main__':
    main()
