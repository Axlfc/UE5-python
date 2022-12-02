import bot
import os
import sys


def main():
    repo_dir = os.path.join(os.getcwd().split("\n")[0], "voiceCloning")

    botanswer = bot.bot(sys.argv[1]).strip()
    botvoice = "bella.wav"

    command = "python voice_cloning.py \"" + str(botanswer) + "\"" + " \"" + botvoice + "\""
    os.system(command)
    filename = repo_dir + "\\" + "outputs" + "\\" + botanswer[:20].replace(" ", "_").replace(",", "").replace(".", "").replace("'", "").replace(":", "") + ".wav"
    print()
    print()
    print(botanswer)
    # TODO: Play audio file
    voicecommand = "python playaudio.py " + filename
    os.system(voicecommand)
    # TODO: Remove audio file
    os.remove(filename)


if __name__ == '__main__':
    main()
