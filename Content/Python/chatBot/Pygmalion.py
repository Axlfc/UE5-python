from transformers import GPT2LMHeadModel, GPT2Tokenizer

def main():
    model_name = "PygmalionAI/pygmalion-6b"
    # "PygmalionAI/pygmalion-6b"
    # "PygmalionAI/pygmalion-2.7b"
    # "PygmalionAI/pygmalion-1.3b"
    # "PygmalionAI/pygmalion-350m"

    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    input_text = "I want to generate some text using Pygmalion."
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    sample_outputs = model.generate(
        input_ids,
        do_sample=True,
        max_length=50,
        top_k=50,
        top_p=0.95,
        temperature=1.0,
        num_return_sequences=1
    )

    output_text = tokenizer.decode(sample_outputs[0], skip_special_tokens=True)
    print(output_text)


if __name__ == '__main__':
    main()
