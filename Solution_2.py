from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup WebDriver
driver = webdriver.Chrome()

try:
    # Step 1: Navigate to Saucedemo and log in
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Step 2: Reset App State from hamburger menu
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))).click()

    # Step 3: Add three items to the cart
    products = driver.find_elements(By.CSS_SELECTOR, ".btn_primary.btn_inventory")
    for i in range(3):  # Add first three products
        products[i].click()

    # Step 4: Navigate to the cart and proceed to checkout
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    # Step 5: Fill in checkout information
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()

    # Step 6: Verify product names and total price
    product_names = [item.text for item in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    total_price = driver.find_element(By.CLASS_NAME, "summary_total_label").text

    # Extract the price (assuming the total price format is "Total: $XX.XX")
    total_amount = total_price.split(": $")[1]
    print(f"Products in cart: {product_names}")
    print(f"Total price: {total_amount}")

    # Step 7: Finish the purchase
    driver.find_element(By.ID, "finish").click()

    # Step 8: Verify successful order message
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    ).text

    assert "THANK YOU FOR YOUR ORDER" in success_message, f"Expected success message, but got: {success_message}"
    print("Order completed successfully.")

    # Step 9: Reset the app state again
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))).click()

    # Step 10: Log out
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))).click()

    print("Logged out successfully.")

finally:
    driver.quit()