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

    if int(n) > 1:
        url_list = []
        # Here we have to save all the urls into a list.

        print("Multi image handling.")
        return

    if response_format == "url":
        return response['data'][0]['url']
    elif response_format == "b64_json":
        return response['data'][0]['base64']

    return None


def generate_image_variation(image_filename, n=1, size="1024x1024", response_format="url"):
    data = openai.Image.create_variation(
        image=open(image_filename, "rb"),
        n=n,
        size=size,
        response_format=response_format,
        model="image-alpha-001"
    )
    if int(n) > 1:
        url_list = []
        # Here we have to save all the urls into a list.

        print("Multi image handling.")
        return

    if n == 1:
        image_url = str(data).split("url")[1][4:]
        image_url = "\n".join(image_url.rsplit("\n", 3)[:-3])
        return image_url[:-1]
    else:
        print("We want to detect all urls and return a list of them.")


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


def download_images(url_list, filename):
    for url in url_list:
        response = requests.get(url)
        with open(filename, "wb") as f:
            f.write(response.content)


def main():
    repo_dir = os.path.join(os.getcwd().split("\n")[0], "images")
    mask_filename = "mask.png"  # Replace with actual mask file name and path
    # mask = Image.open(mask_filename).convert("RGBA")
    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)

    if len(sys.argv) < 2:
        print("Please provide a prompt or an image file name as the first argument.")
        return

    prompt = sys.argv[1]
    n = int("1")
    size = "1024x1024"
    response_format = "url"

    if len(sys.argv) == 2:
        print("ONE ARGUMENT")
        first_argument = sys.argv[1]
        if not os.path.isfile(first_argument):
            image_url = generate_image(prompt, n, size, response_format)
            print("Generated image URL:", image_url)

            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            if process_system.plat() == "Windows":
                filename = repo_dir + "\\" + current_time + "_" + prompt[:20].replace(" ", "_").replace(",", "").replace(".", "").replace("'", "").replace(":", "").replace("\"", "") + ".jpg"
            else:
                filename = repo_dir + "/" + current_time + "_" + prompt[:20].replace(" ", "_").replace(",", "").replace(".", "").replace("'", "").replace(":", "").replace("\"", "") + ".jpg"

            download_image(image_url, filename)
            print("Downloaded image to:", filename)
        else:
            print("ONE IMAGE")
            variation_filename = os.path.splitext(first_argument)[0] + "_var" + str(n) + ".jpg"
            image_url = generate_image_variation(first_argument)
            download_image(image_url, variation_filename)
            print("Downloaded image to:", variation_filename)
    elif len(sys.argv) == 3:
        print("Two arguments")
        first_argument = sys.argv[1]
        second_argument_value = sys.argv[2]
        print("Second argument: ", second_argument_value)
        if os.path.isfile(second_argument_value):
            print("TEXT + IMG")
            image_filename = sys.argv[2]
            edit_filename = os.path.splitext(image_filename)[0] + "_edit.jpg"
            image_url = create_image_edit(image_filename, mask_filename, prompt, int(n), size, response_format)

            if image_url is not None:
                download_image(image_url, edit_filename)
                print("Generated image edited saved as:", edit_filename)
            else:
                print("Error generating image edited")
        else:
            n = second_argument_value

            if os.path.isfile(first_argument):
                print("IMAGE + INTEGER")
                print()
                print("Call variation images")

                variation_filename = os.path.splitext(first_argument)[0] + "_var" + str(n) + ".jpg"
                image_url = generate_image_variation(first_argument, int(n))
                download_image(image_url, variation_filename)
                print("Downloaded images to:", variation_filename)
            else:
                print("TEXT + INTEGER :)")
                print()
                print("Call generate images")
                image_url = generate_image(prompt, n, size, response_format)
                print("Generated image URL:", image_url)

                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                if process_system.plat() == "Windows":
                    filename = repo_dir + "\\" + current_time + "_" + prompt[:20].replace(" ", "_").replace(",",
                                                                                                            "").replace(
                        ".", "").replace("'", "").replace(":", "").replace("\"", "") + ".jpg"
                else:
                    filename = repo_dir + "/" + current_time + "_" + prompt[:20].replace(" ", "_").replace(",",
                                                                                                           "").replace(
                        ".", "").replace("'", "").replace(":", "").replace("\"", "") + ".jpg"

                download_image(image_url, filename)
                print("Downloaded images to:", filename)
    elif len(sys.argv) == 4:
        print("THREE ARGUMENTS")
        second_argument_value = sys.argv[2]
        third_argument = sys.argv[3]

        if os.path.isfile(third_argument):
            print("THIRD ARGUMENT IS A MASK.")
            if os.path.isfile(third_argument) and third_argument.endswith(".png"):
                print("")
                edit_filename = os.path.splitext(second_argument_value)[0] + "_masked.jpg"
                image_url = create_image_edit(second_argument_value, third_argument, prompt, int(n), size, response_format)
                download_image(image_url, edit_filename)
                print("Generated masked image saved as:", edit_filename)
            else:
                print(
                    "Mask file format not supported. Only PNG files are supported as masks. Must be a valid PNG file, less than 4MB, and have the same dimensions as image.")
                print(
                    "An additional image whose fully transparent areas (e.g. where alpha is zero) indicate where image should be edited.")
                return
        else:
            print("THIRD ARGUMENT IS AN INTEGER")
            image_filename = sys.argv[2]
            n = sys.argv[3]
            variation_filename = os.path.splitext(image_filename)[0] + "_var" + n + ".jpg"
            generate_image_variation(variation_filename, int(n))

        '''

        if image_url is not None:
            download_image(image_url, edit_filename)
            print("Generated image edited with mask saved as:", edit_filename)
        else:
            print("Error generating image edited")'''
    elif len(sys.argv) == 5:
        print("FOUR AGRUMENTS")
        pass
    elif len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
        # Only one argument and it's a file, run generate_image_variation
        image_filename = sys.argv[1]
        variation_url = generate_image_variation(image_filename)
        if variation_url is not None:
            variation_filename = os.path.splitext(image_filename)[0] + "_variation.jpg"
            download_image(variation_url, variation_filename)
            print("Generated image variation saved as:", variation_filename)
        else:
            print("Error generating image variation")


if __name__ == '__main__':
    main()
