import sys
import torch
from transformers import AutoTokenizer, T5ForConditionalGeneration
# pip install -q transformers accelerate sentencepiece safetensors bitsandbytes


def generate(input_text, tokenizer, model):
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
    outputs = model.generate(input_ids, max_length=200, bos_token_id=0)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Clean up resources
    del model
    del tokenizer
    torch.cuda.empty_cache()

    return result


def process_bot_answer(input_text):

    model = T5ForConditionalGeneration.from_pretrained("google/flan-ul2",
                                                       load_in_8bit=True, device_map="auto",
                                                       cache_dir="/tmp/model_cache/")
    tokenizer = AutoTokenizer.from_pretrained("google/flan-ul2")

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
