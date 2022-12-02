import bot
import os
import sys


def main():
    repo_dir = os.path.join(os.getcwd().split("\n")[0], "voiceCloning")
    botanswer = bot.bot(sys.argv[1]).strip()
    botanswernojumplines = botanswer.replace('\n', ' ')
    botvoice = "bella.wav"

    command = "python voice_cloning.py \"" + str(botanswernojumplines) + "\"" + " \"" + botvoice + "\""
    os.system(command)
    filename = repo_dir + "\\" + "outputs" + "\\" + botanswernojumplines[:20].replace(" ", "_").replace(",", "").replace(".", "").replace("'", "").replace(":", "") + ".wav"
    print()
    print()
    print(botanswer)
    voicecommand = "python playaudio.py " + filename
    os.system(voicecommand)
    os.remove(filename)


if __name__ == '__main__':
    main()
