import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

def wait_and_click(driver, locator):
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator)).click()
    except (TimeoutException, WebDriverException) as e:
        print(f"Error: {e}")

def fill_input_field(driver, locator, value):
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(locator)).send_keys(value)
    except (TimeoutException, WebDriverException) as e:
        print(f"Error: {e}")

def get_checkout_information(driver):
    try:
        payment_info = driver.find_element(By.XPATH, "//div[contains(text(), 'Payment Information')]/following-sibling::div").text
        shipping_info = driver.find_element(By.XPATH, "//div[contains(text(), 'Shipping Information')]/following-sibling::div").text
        total_amount = driver.find_element(By.XPATH, "//div[contains(text(), 'Total:')]/following-sibling::div").text
        return (f"Payment Information:\n{payment_info}\n"
                f"Shipping Information:\n{shipping_info}\n"
                f"Total amount:\n{total_amount}")
    except NoSuchElementException as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def export_checkout_information(data, file_path):
    try:
        with open(file_path, 'w') as file:
            for key, value in data.items():
                file.write(f"{key}: {value}\n")
        print("Data has been exported to", file_path)
    except Exception as e:
        print("An error occurred while exporting data:", e)

def login(driver, username, password):
    fill_input_field(driver, (By.ID, "user-name"), username)
    fill_input_field(driver, (By.ID, "password"), password)
    wait_and_click(driver, (By.ID, "login-button"))

def add_items_to_cart(driver, num_items):
    for _ in range(num_items):
        wait_and_click(driver, (By.XPATH, "//button[text()='Add to cart']"))

def open_cart(driver):
    wait_and_click(driver, (By.CLASS_NAME, "shopping_cart_link"))

def proceed_to_checkout(driver):
    wait_and_click(driver, (By.XPATH, "//button[text()='Checkout']"))

def fill_personal_details(driver, first_name, last_name, postal_code):
    fill_input_field(driver, (By.ID, "first-name"), first_name)
    fill_input_field(driver, (By.ID, "last-name"), last_name)
    fill_input_field(driver, (By.ID, "postal-code"), postal_code)
    wait_and_click(driver, (By.XPATH, "//input[@value='Continue']"))

def complete_purchase(driver):
    wait_and_click(driver, (By.XPATH, "//button[text()='Finish']"))

def logout(driver):
    try:
        wait_and_click(driver, (By.ID, "react-burger-menu-btn"))
        wait_and_click(driver, (By.ID, "logout_sidebar_link"))
        print("Logged out successfully.")
    except NoSuchElementException:
        print("Logout option not found.")

def main():
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.saucedemo.com")

        login(driver, "standard_user", "secret_sauce")
        add_items_to_cart(driver, 3)
        open_cart(driver)
        proceed_to_checkout(driver)
        fill_personal_details(driver, "John", "Doe", "12345")
        complete_purchase(driver)

        checkout_info = get_checkout_information(driver)

        if checkout_info:
            file_path = "exported_data.txt"
            export_checkout_information(checkout_info, file_path)

        logout(driver)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()