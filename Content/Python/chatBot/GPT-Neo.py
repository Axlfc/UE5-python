from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from transformers import pipeline
import sys


def main():
    model_name = "EleutherAI/gpt-neo-125M"
    # "EleutherAI/gpt-neo-1.3B"
    # "EleutherAI/gpt-neo-2.7B"
    # "EleutherAI/gpt-neo-125M"

    # A 3000 value will produce a buffer overflow so we need to prevent that.

    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPTNeoForCausalLM.from_pretrained(model_name)
    input_text = sys.argv[1]
    text_length = int(sys.argv[2])
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')

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
    # output_text = generator(input_text, max_length=text_length, do_sample=True, temperature=0.9, pad_token_id=generator.tokenizer.eos_token_id)
    # output_list = []
    output_text = tokenizer.decode(sample_outputs[0], skip_special_tokens=True)

    output_list = output_text.split("\n")

    for phrase in output_list:
        if not output_list[-1].endswith("."):
            output_list.pop()

    text = ""
    for phrase in output_list:
        text += " " + phrase

    print(text)
    # return output_text


if __name__ == '__main__':
    main()
