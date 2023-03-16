import torch
from transformers import FlaxAutoModelForCausalLM, FlaxAutoTokenizer


def main():
    # Load the FLAN-UL2 model and tokenizer
    model_name = "flax-community/flan-ul2-cos-e1-py2"
    model = FlaxAutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = FlaxAutoTokenizer.from_pretrained(model_name)

    # Generate text with the model
    prompt = "The quick brown fox jumps over the lazy dog."
    input_ids = tokenizer.encode(prompt, return_tensors="jax")
    output_ids = model.generate(input_ids, max_length=50)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    print(output_text)


if __name__ == '__main__':
    main()