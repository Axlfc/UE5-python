from transformers import GPTNeoForCausalLM, GPT2Tokenizer

def main():
    model_name = "EleutherAI/gpt-neo-1.3B"
    # "facebook/opt-6.7b"
    # "facebook/opt-2.7b"
    # "facebook/opt-1.3b"
    # facebook/opt-350m"

    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPTNeoForCausalLM.from_pretrained(model_name)
    input_text = "I want to generate some text using GPT-Neo."
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
