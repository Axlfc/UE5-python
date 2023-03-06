import openai
from dotenv import load_dotenv
import os
import sys


# MODELS:
# text-curie-001
# text-babbage-001
# text-ada-001
# text-davinci-003
# text-davinci-002
# text-davinci-001
# davinci-instruct-beta
# davinci
# curie-instruct-beta
# curie
# babbage
# ada
# gpt-3.5-turbo
# gpt-3.5-turbo-0301

def bot(prompt):
    load_dotenv()
    openai.api_key = os.environ["OPENAI_API_KEY"]
    model = "gpt-3.5-turbo-0301"

    if "turbo" in model:
        completion = openai.ChatCompletion.create(
            model = model, 
            messages = [{"role": "user", "content": prompt}]
        )
        return str(completion.choices[0]).split("content")[1][6:].split("role")[0][:-1].replace('\\n', '\n')[:-7].encode('utf-8').decode('unicode_escape')
    else:
        completions = openai.Completion.create(
            engine = model,
            prompt = prompt,
            max_tokens = 1024,
            n = 1,
            temperature = 0.5,
        )

        response = completions.choices[0].text
        return response


def main():
    print(bot(sys.argv[1]))
    return bot(sys.argv[1])


if __name__ == '__main__':
    main()
