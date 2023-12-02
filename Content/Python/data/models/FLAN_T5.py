import sys
from transformers import T5Tokenizer, T5ForConditionalGeneration
# pip install -q transformers accelerate sentencepiece


models = ["flan-t5-small", "flan-t5-base", "flan-t5-large", "flan-t5-xl", "flan-t5-xxl"]
current_model_name = "google/" + models[0]


def generate(input_text, tokenizer, model):
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
    outputs = model.generate(input_ids, max_length=200, bos_token_id=0)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result


def process_bot_answer(input_text):
    tokenizer = T5Tokenizer.from_pretrained(current_model_name)
    model = T5ForConditionalGeneration.from_pretrained(current_model_name, device_map="auto")

    return generate(input_text, tokenizer, model)


def main():
    if len(sys.argv) < 2:
        print("Please provide a text prompt as the first argument.")
        return

    input_text = sys.argv[1]

    answer = process_bot_answer(input_text)
    print(answer)
    return answer


if __name__ == '__main__':
    main()
