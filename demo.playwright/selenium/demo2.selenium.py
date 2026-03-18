from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

URL = "https://seleniumbase.io/demo_page"

def main():
    options = Options()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(URL)
        driver.implicitly_wait(5)

        print("Page Title:", driver.title)

        text_input = driver.find_element(By.ID, "myTextInput")
        text_input.clear()

        # ✅ FIXED (no emoji)
        text_input.send_keys("Hello Aakash")

        checkbox = driver.find_element(By.ID, "checkBox1")
        checkbox.click()

        button = driver.find_element(By.ID, "myButton")
        button.click()

        print("Actions performed successfully ✅")
        time.sleep(3)

    except Exception as e:
        print("Error occurred:", e)

    finally:
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    main()