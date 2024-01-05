import openai
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

content_path = Path('../../../../../UE5-python')
sys.path.append(str(content_path))

from Content.Python.src.bot import bot


def code(prompt, lang_model=bot.last_openai_model, text_length=256):
    model = bot.selected_language_model(bot.all_language_models_available, bot.non_openai_models, lang_model)

    if model in bot.non_openai_models:
        if model == "santacoder":
            import santacoder
            return santacoder.process_bot_answer(prompt, text_length)
    elif model in bot.all_language_models_available and model not in bot.non_openai_models:
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]

        completions = openai.Completion.create(
            engine="code-davinci-002",
            prompt=prompt,
            max_tokens=text_length,
            n=1,
            temperature=0.5,
        )

        response = completions.choices[0].text
        return response

    else:
        bot.show_error(model)


def main():
    if len(sys.argv) < 2:
        print("Please provide a text prompt as the first argument.")
        return
    max_length = None
    language_model = bot.last_openai_model

    if len(sys.argv) == 2:
        user_prompt = sys.argv[1]
        # Using default model as language_model

    elif len(sys.argv) == 3:
        if sys.argv[2] in bot.all_language_models_available:
            user_prompt = sys.argv[1]
            language_model = sys.argv[2]
        elif sys.argv[2] and sys.argv[1] in bot.all_language_models_available:
            user_prompt = sys.argv[1]
            language_model = sys.argv[2]
        elif int(sys.argv[2]):
            user_prompt = sys.argv[1]
            max_length = sys.argv[2]
        else:
            bot.show_error(sys.argv[2])
    elif len(sys.argv) == 4:
        if sys.argv[2] in bot.all_language_models_available:
            user_prompt = sys.argv[1]
            language_model = sys.argv[2]
            max_length = sys.argv[3]
        elif sys.argv[2] and sys.argv[1] in bot.all_language_models_available:
            user_prompt = sys.argv[1]
            language_model = sys.argv[2]
            max_length = sys.argv[3]
        else:
            bot.show_error(sys.argv[2])

    if max_length is not None:
        print(code(user_prompt, language_model, int(max_length)))
        return code(user_prompt, language_model, int(max_length))
    else:
        print(code(user_prompt, language_model))
        return code(user_prompt, language_model)


if __name__ == '__main__':
    main()
