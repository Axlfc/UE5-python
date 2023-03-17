'''import galai as gal
import torch

model = gal.load_model("mini", num_gpus=torch.cuda.available_devices())
result = model.generate("Literature review on hardware accelerators", tokens=200)

print(result)'''


from transformers import AutoModelForCausalLM, AutoTokenizer
import sys
import torch


def process_bot_answer(input_text, text_length=50):
    model = AutoModelForCausalLM.from_pretrained("facebook/galactica-125m")
    tokenizer = AutoTokenizer.from_pretrained("facebook/galactica-125m")

    # Tokenize the prompt and generate text using the BLOOM model
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=text_length)

    # Decode the generated text and print it
    generated_text = tokenizer.decode(outputs[0])

    '''# Greedy Search
        #print(tokenizer.decode(model.generate(inputs["input_ids"], max_length=result_length, no_repeat_ngram_size=2)[0]))

        # Beam Search
        #print(tokenizer.decode(model.generate(inputs["input_ids"], max_length=result_length, num_beams=2, no_repeat_ngram_size=2, early_stopping=True)[0]))

        # Sampling Top-k + Top-p
        # print(tokenizer.decode(model.generate(inputs["input_ids"], max_length=result_length, do_sample=True, top_k=50, top_p=0.9)[0]))'''

    # Clean up resources
    del model
    del tokenizer
    torch.cuda.empty_cache()

    return generated_text


def main():
    if len(sys.argv) < 2:
        print("Please provide a text prompt as the first argument.")
        return

    if len(sys.argv) == 2:
        input_text = sys.argv[1]
        # Using default model as language_model
    elif len(sys.argv) == 3:
        input_text = sys.argv[1]
        text_length = int(sys.argv[2])

    # print(process_bot_answer(input_text, text_length))
    return(process_bot_answer(input_text, text_length))


if __name__ == '__main__':
    main()