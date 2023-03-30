import os
import sys
import time
import colorama
import platform
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service

os.environ['MOZ_HEADLESS'] = '1'

if platform.system() == "Windows":
    firefox_profile_path = os.path.expanduser("~") + os.sep + 'AppData' + os.sep + 'Local' + os.sep + 'Mozilla' + os.sep + 'Firefox' + os.sep + 'Profiles' + os.sep + 'inmersprofile.default-release'
else:
    firefox_profile_path = os.path.expanduser("~") + "/snap/firefox/common/.mozilla/firefox/inmersprofile.default-release"

if not os.path.exists(firefox_profile_path):
    os.mkdir(firefox_profile_path)

# Create a FirefoxOptions object with your profile path
firefox_options = webdriver.FirefoxOptions()

firefox_options.add_argument('--profile')

firefox_options.add_argument(firefox_profile_path)

service = Service(log_path=os.devnull)

# Create a new Firefox driver with your options
try:
    driver = webdriver.Firefox(options=firefox_options, service=service)
except:
    driver.quit()


# Load the Inmers web app
driver.get("https://inmers.com")

# Wait for the page to load
time.sleep(4)


def add_message(message, initialtime):
    now = datetime.now()
    time = now.strftime("%H-%M-%S")
    date = now.strftime("%Y-%m-%d")
    repo_dir = os.path.join(os.path.abspath(__file__)[:-10].split("\n")[0], "conversations")

    if platform.system() == "Windows":
        x = repo_dir + "\\" + date
        filepath = x + "\\" + initialtime + ".txt"
    else:
        x = repo_dir + "/" + date
        filepath = x + "/" + initialtime + ".txt"
    if not os.path.exists(x):
        os.mkdir(x)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(time.strip() + ": " + message.strip() + "\n")


def inmers():
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    while True:
        try:
            # Find the chat input box and send a message
            input_box = driver.find_element(By.CSS_SELECTOR, 'textarea')
            print(colorama.Fore.RED + "Enter your text:" + colorama.Fore.CYAN)
            message = input()
            add_message(message, initial_time)
            if message == "exit" or message == "quit":
                driver.quit()
                exit(0)

            input_box.send_keys(message + Keys.RETURN)

            time.sleep(8)

            # Wait for the bot to respond
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.mwai-text p')))
            all_responses = driver.find_elements(By.CSS_SELECTOR, 'div.mwai-reply')

            bot_text_responses = []

            for xd in all_responses:
                if xd.text not in bot_text_responses and "Inmers" in xd.text and xd.text != "Inmers\nHola, mi nombre es Inmers y soy una Inteligencia Artificial muy avanzada. ¿En que te puedo ayudar?":
                    bot_text_responses.append(xd.text)

            index = len(bot_text_responses) - 1

            if bot_text_responses[index] == "":
                pass
            else:
                add_message(bot_text_responses[index].strip("Inmers\n"), initial_time)
                print(colorama.Fore.GREEN + bot_text_responses[index].strip("Inmers\n"))
                print(colorama.Fore.RESET)
        except:
            print("CLOSING...")
            driver.quit()
            exit(1)


def main():
    repo_dir = os.path.join(os.path.abspath(__file__)[:-10].split("\n")[0], "conversations")

    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

    if len(sys.argv) == 2:
        try:
            input_box = driver.find_element(By.CSS_SELECTOR, 'textarea')
            message = sys.argv[1]
            add_message(message, initial_time)
            if message == "exit" or message == "quit":
                driver.quit()
                exit(0)

            input_box.send_keys(message + Keys.RETURN)

            time.sleep(8)

            # Wait for the bot to respond
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.mwai-text p')))
            all_responses = driver.find_elements(By.CSS_SELECTOR, 'div.mwai-reply')

            bot_text_responses = []

            for xd in all_responses:
                if xd.text not in bot_text_responses and "Inmers" in xd.text and xd.text != "Inmers\nHola, mi nombre es Inmers y soy una Inteligencia Artificial muy avanzada. ¿En que te puedo ayudar?":
                    bot_text_responses.append(xd.text)

            index = len(bot_text_responses) - 1

            if bot_text_responses[index] == "":
                pass
            else:
                add_message(bot_text_responses[index].strip("Inmers\n"), initial_time)
                print(colorama.Fore.GREEN + bot_text_responses[index].strip("Inmers\n"))
                print(colorama.Fore.RESET)
        except:
            print("CLOSING...")
            driver.quit()
            exit(1)
    else:
        inmers()


if __name__ == '__main__':
    main()
