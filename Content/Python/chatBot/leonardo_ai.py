import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import sys

load_dotenv()
authorization_string = "Bearer " + os.environ["LEONARDO_AI_API_KEY"]


def get_user_info():
    url = "https://cloud.leonardo.ai/api/rest/v1/me"

    headers = {
        "accept": "application/json",
        "authorization": authorization_string
    }

    response = requests.get(url, headers=headers)

    return response.text


def generate_image(prompt, n=1, size_x=512, size_y=512):
    model_ids = {"Leonardo Creative": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
        "Leonardo Select": "cd2b2a15-9760-4174-a5ff-4d2925057376",
        "Leonardo Signature": "291be633-cb24-434f-898f-e662799936ad"
    }

    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer aaa"
    }

    data = {
        "prompt": prompt,
        "modelId": model_ids["Leonardo Creative"],
        "width": size_y,
        "height": size_x,
        "negative_prompt": "ugly",
        "sd_version": "v1_5",
        "num_images": n,
        "num_inference_steps": 40,
        "guidance_scale": 7,
        "presetStyle": "NONE",
        "tiling": False,
        "public": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data)).json()

    '''if response_format == "url":
        return response['data'][0]['url']
    elif response_format == "b64_json":
        return response['data'][0]['base64']
    '''
    return response


def download_image(url, text):
    print("Generated image url: ", url)
    current_date = datetime.now().strftime("%Y-%m-%d")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images", current_date)
    os.makedirs(images_dir, exist_ok=True)

    filename = os.path.basename(text)
    print(filename)

    file_path = os.path.join(images_dir, filename) + ".jpg"

    response = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(response.content)
    print("Downloaded image to:", file_path)


def main():
    mask_filename = "mask.png"  # Replace with actual mask file name and path
    # mask = Image.open(mask_filename).convert("RGBA")

    if len(sys.argv) < 2:
        print("Please provide a prompt or an image file name as the first argument.")
        print("Usage: python leonardo_ai.py \"<text_prompt>\"")
        return

    prompt = sys.argv[1]
    n = int("1")
    size_x = 512
    size_y = 512

    if len(sys.argv) == 2:
        first_argument = sys.argv[1]
        if not os.path.isfile(first_argument):
            image_url = generate_image(prompt, n, size_x, size_y)
            print("Generated image URL:", image_url)
            # download_image(image_url, prompt)


if __name__ == '__main__':
    main()
