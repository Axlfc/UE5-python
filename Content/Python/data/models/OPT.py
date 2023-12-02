from transformers import pipeline, set_seed
import sys

models = ["opt-125m", "opt-350m", "opt-1.3b", "opt-2.7b", "opt-6.7b", "opt-13b", "opt-30b", "opt-66b"]
current_model_name = "facebook/" + models[0]


def process_bot_answer(input_text, seed=None):
    if seed is None:
        generator = pipeline('text-generation', model=current_model_name)
    else:
        set_seed(seed)
        generator = pipeline('text-generation', model=current_model_name, do_sample=True)
    return generator(input_text)[0]["generated_text"]


def main():
    if len(sys.argv) < 2:
        print("Please provide a text prompt as the first argument or a text prompt and a seed.")
        return

    if len(sys.argv) == 2:
        answer = process_bot_answer(sys.argv[1])
    elif len(sys.argv) == 3:
        answer = process_bot_answer(sys.argv[1], int(sys.argv[2]))

    print(answer)
    return answer


if __name__ == '__main__':
    main()
