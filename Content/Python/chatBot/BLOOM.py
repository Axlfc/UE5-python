import transformers
from transformers import BloomForCausalLM, BloomTokenizerFast


def main():
    # https://towardsdatascience.com/getting-started-with-bloom-9e3295459b65
    # Load the BLOOM model and tokenizer
    model = BloomForCausalLM.from_pretrained("bigscience/bloom-1b3")
    tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom-1b3")

    # Define the prompt and desired length of generated text
    prompt = "Once upon a time"
    result_length = 50

    # Tokenize the prompt and generate text using the BLOOM model
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=result_length)

    # Decode the generated text and print it
    generated_text = tokenizer.decode(outputs[0])
    print(generated_text)
    # Greedy Search
    # print(tokenizer.decode(model.generate(inputs["input_ids"], max_length=result_length)[0]))

    # Beam Search
    # print(tokenizer.decode(model.generate(inputs["input_ids"], max_length=result_length, num_beams=2, no_repeat_ngram_size=2, early_stopping=True)[0]))

    # Sampling Top-k + Top-p
    # print(tokenizer.decode(model.generate(inputs["input_ids"], max_length=result_length, do_sample=True, top_k=50, top_p=0.9)[0]))


if __name__ == '__main__':
    main()