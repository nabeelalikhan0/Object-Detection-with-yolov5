from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# === Configure Chrome to use your existing profile ===
options = Options()

# Replace YOUR_USERNAME with your actual Windows username
options.add_argument(r"user-data-dir=C:\Users\YOUR_USERNAME\AppData\Local\Google\Chrome\User Data")
options.add_argument("profile-directory=Default")  # or use 'Profile 1', 'Profile 2', etc.

# === Launch Chrome with your profile ===
driver = webdriver.Chrome(options=options)
driver.get("https://www.blackbox.ai")

def BlackBoxAI(query):
    try:
        # Enter the prompt
        textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "textarea"))
        )
        textarea.click()
        textarea.clear()
        textarea.send_keys(query)
        textarea.send_keys(Keys.RETURN)

        # Wait for response
        answer = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "prose"))
        )
        return answer[-1].text

    except Exception as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    query = input("Enter your query:\t")
    response = BlackBoxAI(query)
    if response:
        print("\nBlackBoxAI Response:\n", response)
