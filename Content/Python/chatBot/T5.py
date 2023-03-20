from transformers import MT5Model, T5Tokenizer
import sys
# pip3 install sentencepiece requests_html

models = ["t5-small", "t5-base", "t5-large", "t5-3b", "t5-11b"]
current_model_name = models[0]


def generate(article, summary, tokenizer, model):
    inputs = tokenizer(article, return_tensors="pt")
    labels = tokenizer(text_target=summary, return_tensors="pt")

    outputs = model(input_ids=inputs["input_ids"], decoder_input_ids=labels["input_ids"])

    hidden_states = outputs.last_hidden_state

    return outputs


def process_bot_answer(input_text, summary_text):
    model = MT5Model.from_pretrained(current_model_name)
    tokenizer = T5Tokenizer.from_pretrained(current_model_name)

    return generate(input_text, summary_text, tokenizer, model)


def main():
    if len(sys.argv) < 3:
        print("Please provide a text prompt as the first argument and a summary as the second.")
        return

    answer = process_bot_answer(sys.argv[1], sys.argv[2])
    print(answer)
    return answer


if __name__ == '__main__':
    main()