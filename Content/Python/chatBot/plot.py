import bot
import os
import sys
import translator as translate
import process_system

def main():
    python = process_system.main()
    repo_dir = os.path.join(os.getcwd().split("\n")[0], "voiceCloning")
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
    print()
    print(original_bot_answer)
    voicecommand = python + " playaudio.py " + filename
    os.system(voicecommand)
    os.remove(filename)


if __name__ == '__main__':
    main()
