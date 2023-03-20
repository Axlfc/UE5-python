from bs4 import BeautifulSoup
import requests
import sys


current_page = "https://huggingface.co/" + sys.argv[1] + "/tree/main"


# Description: This function gives back a request to an url of a webpage and returns the HTML content
# Arguments: url of the webpage
def get_webpage(url):
    # Hacer una solicitud GET a la página web
    url = url
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')


def main():
    soup = get_webpage(current_page)
    items = soup.find_all('a')

    test_list = []
    for i in items:
        text = i.text
        if (".bin" in text and "pytorch" in text) or ("GB" in text or "MB" in text):
            test_list.append(str(text))

    print("Test LIST:\t", test_list)

    odd_i = []
    even_i = []
    for i in range(0, len(test_list)):
        if i % 2:
            even_i.append(test_list[i])
        else:
            odd_i.append(test_list[i])

    n = float(0)
    for size in even_i:
        print("SIZE =\t", size)
        n += float(size.split("\n")[0].split(" ")[0])

    print("The " + sys.argv[1].split("/")[1] + " model disk size is " + str(n) + " GB")


if __name__ == '__main__':
    main()
