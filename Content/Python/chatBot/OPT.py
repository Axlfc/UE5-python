from transformers import AutoTokenizer, AutoModelForCausalLM


def main():
    model_name = "facebook/opt-6.7b"
    # "facebook/opt-6.7b"
    # "facebook/opt-2.7b"
    # "facebook/opt-1.3b"
    # facebook/opt-350m"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    input_text = "I want to generate some text using OPT 6.7b."
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    sample_outputs = model.generate(
        input_ids,
        do_sample=True,
        max_length=50,
        top_k=0,
        temperature=0.7,
        num_return_sequences=1
    )

    output_text = tokenizer.decode(sample_outputs[0], skip_special_tokens=True)
    print(output_text)


if __name__ == '__main__':
    main()
