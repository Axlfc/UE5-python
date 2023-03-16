from transformers import MT5ForConditionalGeneration, MT5Tokenizer


def main():
    # Load the mT5 model and tokenizer
    model_name = 'google/mt5-small'
    tokenizer = MT5Tokenizer.from_pretrained(model_name)
    model = MT5ForConditionalGeneration.from_pretrained(model_name)

    # Set the input prompt and generate text
    prompt = "translate English to French: Hello, how are you?"
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=128, num_beams=4, early_stopping=True)

    # Decode the output and print the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(generated_text)


if __name__ == '__main__':
    main()