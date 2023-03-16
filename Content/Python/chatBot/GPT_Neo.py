from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from transformers import pipeline
import sys
import torch


def process_bot_answer(input_text, text_length=50):
    model_name = "EleutherAI/gpt-neo-125M"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)

    model = GPTNeoForCausalLM.from_pretrained(model_name)
    model.to('cuda')
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
    # input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cpu")
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')

    # A 3000 value will produce a buffer overflow so we need to prevent that.

    sample_outputs = model.generate(
        input_ids,
        do_sample=True,
        max_length=text_length,
        top_k=50,
        top_p=0.95,
        temperature=0.9,
        num_return_sequences=1,
        pad_token_id=generator.tokenizer.eos_token_id
    )

    output_text = tokenizer.decode(sample_outputs[0], skip_special_tokens=True)

    output_list = output_text.split("\n")

    for phrase in output_list:
        if not output_list[-1].endswith("."):
            output_list.pop()
        phrase = phrase[2:]

    output_list.pop(0)

    text = ""
    for phrase in output_list:
        text += " " + phrase

    # Clean up resources
    del model
    del tokenizer
    torch.cuda.empty_cache()

    return text.lstrip()


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

    print(process_bot_answer(input_text, text_length))
    return(process_bot_answer(input_text, text_length))


if __name__ == '__main__':
    main()
