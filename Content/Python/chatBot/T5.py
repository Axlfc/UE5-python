import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer


def main():
    # Load the T5 model and tokenizer
    model = T5ForConditionalGeneration.from_pretrained('t5-base')
    tokenizer = T5Tokenizer.from_pretrained('t5-base')

    # Define your prompt text
    prompt = 'The quick brown fox'

    # Generate the text
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(input_ids=input_ids, max_length=100, do_sample=True)

    # Decode the generated text and print it
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(generated_text)


if __name__ == '__main__':
    main()