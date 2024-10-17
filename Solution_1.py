from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Setup WebDriver
driver = webdriver.Chrome()

try:
    # Navigate to Saucedemo
    driver.get("https://www.saucedemo.com/")

    # Attempt to log in with locked out user
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Wait for the error message to appear
    time.sleep(4)  # Adjust as necessary for your environment

    # Verify the error message
    error_message = driver.find_element(By.CSS_SELECTOR, ".error-message-container").text
    expected_message = "Sorry, this user has been locked out."

    assert error_message == expected_message, f"Expected: {expected_message}, but got: {error_message}"
    print("Locked out user test passed. Error message displayed correctly.")

finally:
    driver.quit()