import openai
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import sys
import process_system
from PIL import Image
import base64

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


def create_image_edit(image_filename, mask_filename, prompt, n=1, size="1024x1024", response_format="url"):
    data = openai.Image.create_edit(
        image=open(image_filename, "rb"),
        mask=open(mask_filename, "rb"),
        prompt=prompt,
        n=n,
        size=size,
        response_format=response_format,
        model="image-alpha-001"
    )
    image_url = str(data).split("url")[1][4:]
    image_url = "\n".join(image_url.rsplit("\n", 3)[:-3])

    return image_url[:-1]


def download_image(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)


def main():
    repo_dir = os.path.join(os.getcwd().split("\n")[0], "images")
    mask_filename = "mask.png"  # Replace with actual mask file name and path
    mask = Image.open(mask_filename).convert("RGBA")
    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)

    if len(sys.argv) < 2:
        print("Please provide a prompt or an image file name as the first argument.")
        return

    prompt = sys.argv[1]
    n = int("1")
    size = "1024x1024"
    response_format = "url"

    if len(sys.argv) == 3:
        image_filename = sys.argv[2]
        edit_filename = os.path.splitext(image_filename)[0] + "_edit.jpg"
        image_url = create_image_edit(image_filename, mask_filename, prompt, int(n), size, response_format)
        if image_url is not None:
            download_image(image_url, edit_filename)
            print("Generated image edited saved as:", edit_filename)
        else:
            print("Error generating image edited")
    elif len(sys.argv) == 4:
        image_filename = sys.argv[2]
        mask_filename = sys.argv[3]

        if os.path.isfile(mask_filename) and mask_filename.endswith(".png"):
            pass
        else:
            print("Mask file format not supported. Only PNG files are supported as masks. Must be a valid PNG file, less than 4MB, and have the same dimensions as image.")
            print("An additional image whose fully transparent areas (e.g. where alpha is zero) indicate where image should be edited.")
            return

        edit_filename = os.path.splitext(image_filename)[0] + "_masked1.jpg"
        image_url = create_image_edit(image_filename, mask_filename, prompt, int(n), size, response_format)

        if image_url is not None:
            download_image(image_url, edit_filename)
            print("Generated image edited with mask saved as:", edit_filename)
        else:
            print("Error generating image edited")
    else:
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
