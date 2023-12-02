from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import sys

models = ["pygmalion-350m", "pygmalion-1.3b", "pygmalion-2.7b", "pygmalion-6b"]
current_model_name = "PygmalionAI/" + models[0]


def generate(article, length=256):
    generator = pipeline('text-generation', model=current_model_name)
    outputs = generator(article, do_sample=True, max_length=length, num_return_sequences=5)

    return [s["generated_text"] for s in outputs]


def process_bot_answer(input_text):
    candidates = generate(input_text)

    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForSequenceClassification.from_pretrained("ChaiML/gpt2_base_retry_and_continue_12m_reward_model")
    # model = AutoModelForSequenceClassification.from_pretrained(current_model_name)
    tokenizer.pad_token_id = 50256
    tokenizer.truncation_side = "left"
    tokenizer.padding_side = "right"
    tokens = tokenizer(candidates, return_tensors='pt', return_attention_mask=True, padding='longest', truncation=True,
                       max_length=256)
    reward = model(**tokens).logits[:, 1]
    idx = reward.argmax()

    chosen_reply = candidates[idx][len(input_text):]

    return chosen_reply


def main():
    if len(sys.argv) < 2:
        print("Please provide a text prompt as the first argument.")
        return

    if len(sys.argv) == 2:
        # Using default model as language_model
        print(process_bot_answer(sys.argv[1]))
        return process_bot_answer(sys.argv[1])
    elif len(sys.argv) == 3:
        print(process_bot_answer(sys.argv[1], int(sys.argv[2])))
        return process_bot_answer(sys.argv[1], int(sys.argv[2]))


if __name__ == '__main__':
    main()
