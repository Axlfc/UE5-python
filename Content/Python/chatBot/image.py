import openai
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import sys
import process_system

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_image(prompt, n=1, size="1024x1024", response_format="url"):
    url = "https://api.openai.com/v1/images/generations"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {openai.api_key}"}
    data = {
        "model": "image-alpha-001",
        "prompt": prompt,
        "n": n,
        "size": size,
        "response_format": response_format
    }
    response = requests.post(url, headers=headers, data=json.dumps(data)).json()

    if response_format == "url":
        return response['data'][0]['url']
    elif response_format == "b64_json":
        return response['data'][0]['base64']

    return None


def download_image(url, filename):

    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)


def main():
    repo_dir = os.path.join(os.getcwd().split("\n")[0], "images")
    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)
    prompt = sys.argv[1]
    n = 1
    size = "1024x1024"
    response_format = "url"

    image_url = generate_image(prompt, n, size, response_format)
    print("Generated image URL:", image_url)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if process_system.plat() == "Windows":
        filename = repo_dir + "\\" + current_time + "_" + prompt[:20].replace(" ", "_").replace(",", "").replace(".", "").replace("'", "").replace(":", "").replace("\"", "") + ".jpg"
    else:
        filename = repo_dir + "/" + current_time + "_" + prompt[:20].replace(" ", "_").replace(",", "").replace(".", "").replace("'", "").replace(":", "").replace("\"", "") + ".jpg"

    download_image(image_url, filename)
    print("Downloaded image to:", filename)

if __name__ == '__main__':
    main()