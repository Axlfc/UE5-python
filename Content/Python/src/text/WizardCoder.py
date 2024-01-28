from flask import Flask, request, jsonify
from llama_cpp import Llama
import logging

logging.basicConfig(level=logging.INFO)

model_path = "C:\\Users\\AxelFC\\.cache\\lm-studio\\models\\TheBloke\\WizardCoder-33B-V1.1-GGUF\\wizardcoder-33b-v1.1.Q4_K_M.gguf"

try:
    llm = Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=32,
        n_gpu_layers=0
    )
except Exception as e:
    logging.error(f"Failed to initialize Llama model: {e}")
    llm = None

app = Flask(__name__)


@app.route('/generate', methods=['POST'])
def generate_text():
    if not llm:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    max_tokens = data.get('max_tokens', 20000)

    generation_kwargs = {
        "max_tokens": max_tokens,
        "stop": ["</s>"],
        "echo": False,
        "top_k": 1
    }

    try:
        response = llm(text, **generation_kwargs)
        generated_text = response["choices"][0]["text"]
        return jsonify({'generated_text': generated_text})
    except Exception as e:
        logging.error(f"Error during text generation: {e}")
        return jsonify({'error': 'Failed to generate text'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=1234)
