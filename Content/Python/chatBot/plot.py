import bot
import re
import os
import sys
import translator as translate


def pythonCheck(text):
    if re.search(r'^(for|while|if|def|try|except|else|elif|with|continue|break|#|from|import|return|pass|async|await|yield|raise|del|class|global|finally|assert)', text):
        return True
    # if it starts with a '(' then it's not python
    if re.search(r'^\(', text):
        return False
     # if it starts or ends with a '=' then it's not python
    if re.search(r'^=|=$', text):
        return False
    if re.search(r'\(|=', text):
        return True
    return False


def main():
    repo_dir = os.path.join(os.getcwd().split("\n")[0], "voiceCloning")
    lang = translate.detect(sys.argv[1])
    botanswer = bot.bot(sys.argv[1]).strip()
    original_bot_answer = botanswer
    if not lang == "en":
        botanswer = translate.text_process(botanswer, "en")
    botanswernojumplines = botanswer.replace('\n', ' ')
    botvoice = "bella.wav"

    command = "python voice_cloning.py \"" + str(botanswernojumplines) + "\"" + " \"" + botvoice + "\""
    os.system(command)
    filename = repo_dir + "\\" + "outputs" + "\\" + botanswernojumplines[:20].replace(" ", "_").replace(",", "").replace(".", "").replace("'", "").replace(":", "") + ".wav"
    print()
    print()
    print(original_bot_answer)
    voicecommand = "python playaudio.py " + filename
    os.system(voicecommand)
    os.remove(filename)


if __name__ == '__main__':
    main()
