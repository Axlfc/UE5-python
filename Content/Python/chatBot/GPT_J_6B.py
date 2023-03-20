from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# import torch
import sys

current_model_name = "EleutherAI/gpt-j-6B"


def process_bot_answer(input_text):
    tokenizer = AutoTokenizer.from_pretrained(current_model_name)
    model = AutoModelForCausalLM.from_pretrained(current_model_name)

    return pipeline("text-generation", model=model, tokenizer=tokenizer, device=0)


def main():
    if len(sys.argv) < 2:
        print("Please provide a text prompt as the first argument.")
        return

    answer = process_bot_answer(sys.argv[1])
    print(answer)
    return answer


if __name__ == '__main__':
    main()