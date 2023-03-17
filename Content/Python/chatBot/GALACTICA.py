from transformers import AutoTokenizer, OPTForCausalLM
import torch
import sys


def process_bot_answer(input_text):
    tokenizer = AutoTokenizer.from_pretrained("facebook/galactica-125m")
    model = OPTForCausalLM.from_pretrained("facebook/galactica-125m", device_map="auto")
    # model = OPTForCausalLM.from_pretrained("facebook/galactica-125m")

    # Tokenize the prompt and generate text using the BLOOM model
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
    # input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_length=200, do_sample=True)

    # Decode the generated text and print it
    generated_text = tokenizer.decode(outputs[0])

    # Clean up resources
    del model
    del tokenizer
    torch.cuda.empty_cache()

    return generated_text


def main():
    if len(sys.argv) < 2:
        print("Please provide a text prompt as the first argument.")
        return

    input_text = sys.argv[1]


    print(process_bot_answer(input_text))
    # return process_bot_answer(input_text)


if __name__ == '__main__':
    main()