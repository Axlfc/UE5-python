import whisper  # pip install git+https://github.com/openai/whisper.git jiwer
import sys
from os import path
from langdetect import detect, DetectorFactory  # pip install langdetect
from googletrans import Translator  # pip install googletrans==4.0.0-rc1

# We need ffmpeg installed in the system (win: choco install ffmpeg / linux: sudo apt install ffmpeg)


langs = {
    "Amárico":  "am",
    "Árabe":	"ar",
    "Vasco":	"eu",
    "Bengalí":	"bn",
    "Inglés (Reino Unido)":	"en-GB",
    "Portugués (Brasil)":	"pt-BR",
    "Búlgaro":	"bg",
    "Catalán":	"ca",
    "Cheroqui":	"chr",
    "Croata":	"h",
    "Checo":	"cs",
    "Danés":	"da",
    "Neerlandés":	"nl",
    "Inglés (EE.UU.)":	"en",
    "Estonio":	"et",
    "Filipino":	"fil",
    "Finés":	"fi",
    "Francés":	"fr",
    "Alemán":	"de",
    "Griego":	"el",
    "Guyaratí":	"gu",
    "Hebreo":	"iw",
    "Hindi":	"hi",
    "Húngaro":	"hu",
    "Islandés":	"is",
    "Indonesio":	"id",
    "Italiano":	"it",
    "Japonés":	"ja",
    "Canarés":	"kn",
    "Coreano":	"ko",
    "Letón":	"lv",
    "Lituano":	"lt",
    "Malay":	"ms",
    "Malabar":	"ml",
    "Maratí":	"mr",
    "Noruego":	"no",
    "Polaco":	"pl",
    "Portugués (Portugal)":	"pt-PT",
    "Rumano":	"ro",
    "Ruso":	"ru",
    "Serbio":	"sr",
    "chino (PRC)":	"zh-CN",
    "Eslovaco":	"sk",
    "Esloveno":	"sl",
    "Español":	"es",
    "Suajili":	"sw",
    "Sueco":	"sv",
    "Tamil":	"ta",
    "Telugu":	"te",
    "Tailandés":	"th",
    "Chino (Taiwán)":	"zh-TW",
    "Turco":	"tr",
    "Urdu":	"ur",
    "Ucraniano":	"uk",
    "Vietnamita":	"vi",
    "Galés":	"cy"
}


def audio_process(audiopath):
    model = whisper.load_model("medium")  # tiny, base, small, medium, large

    # detect the spoken language
    _, probs = model.detect_language(whisper.log_mel_spectrogram(whisper.pad_or_trim(whisper.load_audio(audiopath))).to(model.device))
    lang = {max(probs, key=probs.get)}
    print("Detected language:\t", lang)
    lang = str(lang).strip("{").strip("}").replace("'", "")
    result = model.transcribe(audiopath, fp16=False, language=lang)

    return result["text"]


def text_process(text, destlang):
    DetectorFactory.seed = 0
    translator = Translator()
    lang = detect(text)
    result = translator.translate(text, src=lang, dest=destlang).text
    return result


def main():
    # StdIn processing
    if not sys.stdin.isatty():
        print("ERROR: translator.py needs two arguments, a text or an audio file, and an output language name code.")
        exit(1)

    # Argument processing
    if len(sys.argv) == 1:
        print("ERROR: translator.py needs two arguments, a text or an audio file, and an output language name code.")
        exit(2)

    if len(sys.argv) == 2:
        # default to English
        lang = "en"
        if path.exists(sys.argv[1]):
            print(audio_process(sys.argv[1]))
        else:
            # We are translating a language
            print(text_process(sys.argv[1], lang))
    elif len(sys.argv) == 3:
        lang = sys.argv[2]
        if path.exists(sys.argv[1]):
            print(text_process(audio_process(sys.argv[1]), lang))
        else:
            # We are translating a language
            print(text_process(sys.argv[1], lang))


if __name__ == '__main__':
    main()
