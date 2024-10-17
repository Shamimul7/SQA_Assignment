import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture(scope="module")
def setup_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_login_locked_out_user(setup_driver):
    driver = setup_driver

    # Step 1: Navigate to Saucedemo
    driver.get("https://www.saucedemo.com/")

    # Step 2: Try to log in with locked_out_user
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Step 3: Verify the error message
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']"))
    ).text

    expected_message = "Epic sadface: Sorry, this user has been locked out."
    assert error_message == expected_message, f"Expected error message: '{expected_message}', but got: '{error_message}'"
    print("Error message verified successfully.")


if __name__ == "__main__":
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    pytest.main(['-q', '--html=report_' + timestamp + '.html', 'test_locked_out_user.py'])