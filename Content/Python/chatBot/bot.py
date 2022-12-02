import openai
from dotenv import load_dotenv
import os
import sys


def bot(prompt):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        temperature=0.5,
    )

    response = completions.choices[0].text
    return response


def main():
    load_dotenv()
    print(bot(sys.argv[1]))


if __name__ == '__main__':
    main()
