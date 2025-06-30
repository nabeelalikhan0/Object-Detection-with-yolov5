from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

driver = webdriver.Chrome()
driver.get("https://www.blackbox.ai")

def BlackBoxAI(query):

    while True:
            # query = input("Enter:\t")
            elem = driver.find_element(By.TAG_NAME,"textarea")
            elem.clear()
            elem.send_keys(query)
            elem.send_keys(Keys.RETURN)
            sleep(4)
            # sleep(10)
            answer = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "prose"))
            )
            return answer[-1].text
            assert "quit" or "exit" or "q" in query
            # print(answer[-1].text)
    else:print("Please Eneter Something")
    driver.close()

if __name__ == "__main__":
    query = input("Enter:\t")
    BlackBoxAI(query)