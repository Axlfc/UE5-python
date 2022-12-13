import openai
from dotenv import load_dotenv
import os
import sys

# code-cushman-001


def code(prompt):
    load_dotenv()
    openai.api_key = os.environ["OPENAI_API_KEY"]

    completions = openai.Completion.create(
        engine="code-davinci-002",
        prompt=prompt,
        max_tokens=256,
        n=1,
        temperature=0.5,
    )

    response = completions.choices[0].text
    return response


def main():
    print(code(sys.argv[1]))
    return code(sys.argv[1])


if __name__ == '__main__':
    main()
