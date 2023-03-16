import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def main():
    tokenizer = AutoTokenizer.from_pretrained("flax-community/flan-t5-small")
    model = AutoModelForCausalLM.from_pretrained("flax-community/flan-t5-small")

    input_text = "The quick brown fox jumps over the lazy dog"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Generate text using beam search
    beam_output = model.generate(input_ids, max_length=50, num_beams=5, early_stopping=True)

    # Decode the output and print the generated text
    generated_text = tokenizer.decode(beam_output[0], skip_special_tokens=True)
    print(generated_text)


if __name__ == '__main__':
    main()