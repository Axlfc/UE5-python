from dotenv import load_dotenv
import os
import sys

from pathlib import Path

content_path = Path('../../../../../UE5-python')
sys.path.append(str(content_path))

from Content.Python_dependencies.old_openai import openai as old_openai
from Content.Python_dependencies.latest_openai import openai as latest_openai

# Description: Show list of all available models
# Argument 1: The name of the selected invalid string of the model
def show_error(model_name):
    print("The selected model \"" + model_name + "\" is not a valid model.")
    print("Available text language models:\n")
    for mo in all_language_models_available:
        print("\t- " + mo)
    exit(1)


# Description: Give back the name of the model, if the model is not expected, show an error
# Argument 1: List containing all the model names
# Argument 2: List containing all non-openai models
# Argument 3: The name of the selected string of the model
def selected_language_model(all_lang_models, other_lang_models, model_name):
    if model_name not in other_lang_models:
        return model_name
    else:
        if model_name not in all_lang_models:
            show_error(model_name)
        else:
            return model_name


all_language_models_available = ["text-curie-001",
                                 "text-babbage-001",
                                 "text-ada-001",
                                 "text-davinci-003",
                                 "text-davinci-002",
                                 "text-davinci-001",
                                 "davinci-instruct-beta",
                                 "davinci",
                                 "curie-instruct-beta",
                                 "curie",
                                 "babbage",
                                 "ada",
                                 "gpt-3.5-turbo",
                                 "gpt-3.5-turbo-0301",
                                 "gpt-4", 
                                 "gpt-4-0314", 
                                 "gpt-4-32k", 
                                 "gpt-4-32k-0314",
                                 "BLOOM",
                                 "FLAN-T5",
                                 "GALACTICA",
                                 "GPT-Neo",
                                 "mT5",
                                 "OPT",
                                 "Pygmalion",
                                 "T5",
                                 "santacoder"]
non_openai_models = ["BLOOM",
                     "FLAN-T5",
                     "GALACTICA",
                     "GPT-Neo",
                     "mT5",
                     "OPT",
                     "Pygmalion",
                     "T5",
                     "santacoder"]
#  last_openai_model = "gpt-3.5-turbo-0301"
last_openai_model = "gpt-4"


# Description: The
# Argument 1: The text prompt of the user
# Argument 2: A language model name
def bot(prompt, lang_model=last_openai_model):
    model = selected_language_model(all_language_models_available, non_openai_models, lang_model)
    if model in all_language_models_available and model not in non_openai_models:
        load_dotenv()

        old_openai.api_key = os.environ["OPENAI_API_KEY"]

        if "gpt-3.5-turbo" in model:
            completion = latest_openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return str(completion.choices[0]).split("content")[1][4:].split("role")[0][:-1].replace('\n', '\n')[
                   :-7].encode('utf-8').decode('unicode_escape')
        elif "gpt-4" in model:
            #  Here we will enter when langchain and openai libraries work together in further updates
            client = latest_openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model
            )
            return chat_completion.choices[0].message.content
        else:
            completions = old_openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                temperature=0.5,
            )

            response = completions.choices[0].text
            return response
    elif model in non_openai_models:
        if model == "GPT-Neo":
            import GPT_Neo
            return GPT_Neo.process_bot_answer(prompt)
        elif model == "BLOOM":
            import BLOOM
            return BLOOM.process_bot_answer(prompt)
        elif model == "FLAN-T5":
            import FLAN_T5
            return FLAN_T5.process_bot_answer(prompt)
        elif model == "GALACTICA":
            import GALACTICA
            return GALACTICA.process_bot_answer(prompt)
        elif model == "OPT":
            import OPT
            return OPT.process_bot_answer(prompt)
        elif model == "Pygmalion":
            import Pygmalion
            return Pygmalion.process_bot_answer(prompt)
        elif model == "santacoder":
            import santacoder
            return santacoder.process_bot_answer(prompt)
    else:
        show_error(model)


def main():
    if len(sys.argv) < 2:
        print("Please provide a text prompt as the first argument.")
        return

    if len(sys.argv) == 2:
        user_prompt = sys.argv[1]
        # Using default model as language_model
        language_model = last_openai_model
    elif len(sys.argv) == 3:
        if sys.argv[2] in all_language_models_available:
            user_prompt = sys.argv[1]
            language_model = sys.argv[2]
        elif sys.argv[2] and sys.argv[1] in all_language_models_available:
            user_prompt = sys.argv[1]
            language_model = sys.argv[2]
        else:
            show_error(sys.argv[2])

    # print(bot(user_prompt, language_model))
    return bot(user_prompt, language_model)


if __name__ == '__main__':
    main()
