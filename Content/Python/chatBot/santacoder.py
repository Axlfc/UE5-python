from transformers import AutoModelForCausalLM, AutoTokenizer
import sys
import torch

checkpoint = "bigcode/santacoder"
device = "cuda"  # for GPU usage or "cpu" for CPU usage


def cleanup_resources(model, tokenizer):
    # Clean up resources
    del model
    del tokenizer
    torch.cuda.empty_cache()


def load_other_checkpoints(model_name):
    return AutoModelForCausalLM.from_pretrained(
        model_name,
        revision="no-fim",  # name of branch or commit hash
        trust_remote_code=True
    )


def process_bot_answer(input_text, text_length=50):
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = load_other_checkpoints(checkpoint).to(device)

    inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)

    '''
    # Fill-in-the-middle uses special tokens to identify the prefix/middle/suffix part of the input and output:
    input_text = "<fim-prefix>def print_hello_world():\n    <fim-suffix>\n    print('Hello world!')<fim-middle>"
    inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
    '''
    attention_mask = torch.ones(inputs.shape, dtype=torch.long, device=device)
    outputs = model.generate(inputs, attention_mask=attention_mask, pad_token_id=tokenizer.eos_token_id, max_length=int(text_length))

    cleanup_resources(model, tokenizer)

    return tokenizer.decode(outputs[0])


def main():
    if len(sys.argv) < 2:
        print("Please provide a text prompt as the first argument.")
        return

    if len(sys.argv) == 2:
        input_text = sys.argv[1]
        # Using default model as language_model
    elif len(sys.argv) == 3:
        input_text = sys.argv[1]
        text_length = int(sys.argv[2])

    print(process_bot_answer(input_text, text_length))
    return (process_bot_answer(input_text, text_length))


if __name__ == '__main__':
    main()
