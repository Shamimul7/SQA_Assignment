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


def test_standard_user_checkout(setup_driver):
    driver = setup_driver

    # Step 1: Navigate to Saucedemo and log in
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Step 2: Reset App State from hamburger menu
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))
    ).click()

    # Step 3: Add three items to the cart
    products = driver.find_elements(By.CSS_SELECTOR, ".btn_primary.btn_inventory")
    for i in range(3):  # Add the first three products
        products[i].click()

    # Step 4: Navigate to the cart and proceed to checkout
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    ).click()

    # Step 5: Fill in checkout information
    driver.find_element(By.ID, "first-name").send_keys("Shamimul")
    driver.find_element(By.ID, "last-name").send_keys("Islam")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()

    # Step 6: Verify product names and total price
    product_names = [item.text for item in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    total_price_label = driver.find_element(By.CLASS_NAME, "summary_total_label").text
    total_price = total_price_label.split(": $")[1]

    assert len(product_names) == 3, "Number of products in cart does not match."

    # Step 7: Finish the purchase
    driver.find_element(By.ID, "finish").click()

    # Step 8: Verify successful order message
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    ).text

    assert "THANK YOU FOR YOUR ORDER" in success_message, f"Expected success message, but got: {success_message}"

    # Step 9: Reset the app state again
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))
    ).click()

    # Step 10: Log out
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    ).click()


if __name__ == "__main__":
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    pytest.main(['-q', '--html=report_' + timestamp + '.html', 'your_test_file.py'])
