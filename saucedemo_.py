from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver
driver = webdriver.Chrome()

try:
    # Step 1: Navigate to Saucedemo
    driver.get("https://www.saucedemo.com/")

    # Step 2: Login with valid credentials
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Step 3: Wait for products to load and check the title
    WebDriverWait(driver, 60).until(EC.title_contains("Products"))

    print("Login successful. You are on the products page.")

    # You can add more interactions here (e.g., add items to the cart, etc.)

finally:
    # Close the WebDriver
    driver.quit()

