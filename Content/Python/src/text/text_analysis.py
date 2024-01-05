import os
import sys
from pathlib import Path
import platform

from selenium.common import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# os.environ['MOZ_HEADLESS'] = '1'

if platform.system() == "Windows":
    firefox_profile_path = os.path.expanduser("~") + os.sep + 'AppData' + os.sep + 'Local' + os.sep + 'Mozilla' + os.sep + 'Firefox' + os.sep + 'Profiles' + os.sep + 'inmersprofile.default-release'
else:
    firefox_profile_path = os.path.expanduser("~") + "/snap/firefox/common/.mozilla/firefox/inmersprofile.default-release"

# Create a FirefoxOptions object with your profile path
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--profile')
firefox_options.add_argument(firefox_profile_path)

# Create a new Firefox driver with your options
try:
    driver = webdriver.Firefox(options=firefox_options)
except Exception as e:
    print(f"ERROR!:\t{e}")
    driver.quit()


def get_text_chunks(text, max_length):
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        # If adding the paragraph exceeds max_length, handle the current chunk
        if len(current_chunk) + len(paragraph) + 1 > max_length:
            if current_chunk:  # Ensure the current chunk is not empty
                chunks.append(current_chunk.strip())
                current_chunk = ""
            # If the paragraph itself is too long, split it and add as a new chunk
            while len(paragraph) > max_length:
                chunks.append(paragraph[:max_length])
                paragraph = paragraph[max_length:]

        current_chunk += paragraph + '\n'

    # Handle the last chunk
    if current_chunk:
        if len(current_chunk.strip()) < max_length / 2 and chunks:
            # If the last chunk is less than half the max_length, and there are previous chunks
            # Merge it with the last chunk, if the total length doesn't exceed max_length
            if len(chunks[-1]) + len(current_chunk) <= max_length:
                chunks[-1] += '\n' + current_chunk.strip()
            else:
                chunks.append(current_chunk.strip())
        else:
            chunks.append(current_chunk.strip())

    return chunks


def calculate_weighted_average(percentages, lengths):
    if not percentages or sum(lengths) == 0:
        return "No data to calculate"

    weighted_sum = sum(p * l for p, l in zip(percentages, lengths))
    total_length = sum(lengths)
    return weighted_sum / total_length


def analyze_text_with_selenium(text, driver):
    # Navigate to the website
    driver.get("https://www.zerogpt.com/")

    try:
        # Find the textarea and clear it
        textarea = driver.find_element(By.ID, "textArea")
        textarea.clear()

        # Handle any pop-ups or overlays here
        # Example: Close a cookie consent pop-up if it exists
        '''# Wait for and click 'Reject All' on the popup
        reject_all_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'REJECT ALL')]"))
        )
        reject_all_button.click()

        # Wait for and click 'Save & Exit' on the popup
        save_exit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'SAVE & EXIT')]"))
        )
        save_exit_button.click()'''

        # Wait for the textarea to be loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "textArea"))
        )

        # Type the text into the textarea
        textarea.send_keys(text)

        # Scroll to the 'scoreButton' and click it
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "scoreButton"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        driver.execute_script("arguments[0].click();", submit_button)

        try:
            # Wait for the AI GPT percentage to load
            ai_gpt_percentage_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "percentage-div"))
            )
            full_text = ai_gpt_percentage_element.text

            # Process the text to extract the percentage and "AI GPT*" text
            # This might need to be adjusted based on the actual format of the text you receive
            ai_gpt_percentage = ' '.join(full_text.split('\n'))  # Adjust this line as needed based on the actual format
            percentage_value = ''.join(filter(lambda x: x.isdigit() or x == '.', ai_gpt_percentage))

            if percentage_value:
                return float(percentage_value), len(text)
            else:
                return 0.0, len(text)

        except NoSuchElementException:
            print("Element not found on the page.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0.0, 0
        try:
            # Find all highlighted elements
            highlighted_elements = driver.find_elements(By.CLASS_NAME, "highlight")

            # Extract and print highlighted texts in italics
            for element in highlighted_elements:
                highlight_text = element.text
                # Print in italics (ANSI escape code)
                print(f"\x1B[3m{highlight_text}\x1B[23m")

        except NoSuchElementException:
            print("No highlighted elements found on the page.")
        except Exception as e:
            print(f"An error occurred while extracting highlights: {e}")
    except NoSuchElementException:
        print("Element not found on the page.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        #  input_file_name = input("Please provide the name of the text file to analyze.")
        file_name = Path('text.txt')

    total_percentages = []
    total_lengths = []

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text_to_analyze = file.read()
        # Split the text into chunks and analyze each chunk
        chunks = get_text_chunks(text_to_analyze, 15000)

        for chunk in chunks:
            percentage, length = analyze_text_with_selenium(chunk, driver)
            if percentage is not None:
                total_percentages.append(float(percentage))
                total_lengths.append(length)

        # Calculate the final weighted average percentage
        final_percentage = calculate_weighted_average(total_percentages, total_lengths)
        print(f"Final AI GPT Percentage (Weighted Average): {final_percentage}%")
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
