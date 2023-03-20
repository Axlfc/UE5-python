from transformers import AutoTokenizer, OPTForCausalLM
import torch
import sys


models = ["galactica-125m", "galactica-1.3b", "galactica-6.7b", "galactica-30b", "galactica-120b"]
current_model_name = "facebook/" + models[0]


def process_bot_answer(input_text, text_length=200):
    tokenizer = AutoTokenizer.from_pretrained("facebook/galactica-125m")
    model = OPTForCausalLM.from_pretrained("facebook/galactica-125m", device_map="auto")
    # model = OPTForCausalLM.from_pretrained("facebook/galactica-125m")

    # Tokenize the prompt and generate text using the BLOOM model
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
    # input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_length=text_length, do_sample=True)

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


    print(process_bot_answer(input_text, text_length))
    # return process_bot_answer(input_text)


if __name__ == '__main__':
    main()