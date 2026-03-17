from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

# =========================
# Chrome Options (Disable popup)
# =========================
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})

# =========================
# Driver Setup
# =========================
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.maximize_window()
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 10)

# =========================
# Helper to run tests
# =========================
def run_test(name, func):
    try:
        func()
        print(f"✅ {name} Passed")
    except Exception as e:
        print(f"❌ {name} Failed: {e}")

# =========================
# TEST CASES
# =========================

def test_login():
    driver.get("https://the-internet.herokuapp.com/login")

    username = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    password = wait.until(EC.visibility_of_element_located((By.ID, "password")))

    username.clear()
    password.clear()

    username.send_keys("tomsmith")
    password.send_keys("SuperSecretPassword!")

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    flash = wait.until(EC.visibility_of_element_located((By.ID, "flash")))
    assert "You logged into a secure area!" in flash.text


def test_checkbox():
    driver.get("https://the-internet.herokuapp.com/checkboxes")

    checkboxes = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='checkbox']"))
    )

    # Use JavaScript click (avoids interaction issues)
    driver.execute_script("arguments[0].click();", checkboxes[0])

    assert checkboxes[0].is_selected()


def test_dropdown():
    driver.get("https://the-internet.herokuapp.com/dropdown")

    dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "dropdown"))))
    dropdown.select_by_visible_text("Option 1")

    assert dropdown.first_selected_option.text == "Option 1"


def test_add_remove():
    driver.get("https://the-internet.herokuapp.com/add_remove_elements/")

    add_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Add Element']"))
    )

    # JS click
    driver.execute_script("arguments[0].click();", add_btn)

    delete_btn = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.added-manually"))
    )

    assert delete_btn.is_displayed()

    # JS click again
    driver.execute_script("arguments[0].click();", delete_btn)


def test_broken_images():
    driver.get("https://the-internet.herokuapp.com/broken_images")

    images = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
    broken = []

    for img in images:
        src = img.get_attribute("src")
        try:
            if requests.get(src, timeout=5).status_code != 200:
                broken.append(src)
        except:
            broken.append(src)

    assert len(broken) == 2


# =========================
# RUN ALL TESTS
# =========================
run_test("Login Test", test_login)
run_test("Checkbox Test", test_checkbox)
run_test("Dropdown Test", test_dropdown)
run_test("Add/Remove Test", test_add_remove)
run_test("Broken Images Test", test_broken_images)

print("\n🎉 ALL TESTS EXECUTED")

time.sleep(2)
driver.quit()