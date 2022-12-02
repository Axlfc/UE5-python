import playaudio as play
import bot
import sys
sys.path.append("..")
import voice_cloning as voice


def main():
    botanswer = bot.bot(sys.argv[1])
    botvoice = "C:\\Users\\AxelFC\\Desktop\\bella.wav"
    print(botanswer)
    # TODO: Call to voice_cloning to output the bot response, play it and then remove the .wav file.


if __name__ == '__main__':
    main()
