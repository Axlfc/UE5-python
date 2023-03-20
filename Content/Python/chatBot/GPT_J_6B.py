from transformers import GPTJForCausalLM, GPT2Tokenizer


def main():
    model = GPTJForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")
    tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-j-6B")

    input_text = "I want to generate some text using GPT-J 6B."
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    sample_output = model.generate(
        input_ids,
        do_sample=True,
        max_length=50,
        top_p=0.92,
        top_k=0,
        temperature=1.0,
        num_return_sequences=1
    )

    output_text = tokenizer.decode(sample_output[0], skip_special_tokens=True)
    print(output_text)


if __name__ == '__main__':
    main()