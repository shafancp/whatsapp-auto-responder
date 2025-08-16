from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime

# Your details
FULL_NAME = "Your Name"
STAFF_NUMBER = "00000"
GROUP_NAME = "Group Name"
TRIGGER_PHRASE = "Trigger Message"

def wait_for_message_box(driver, timeout=1):
    """Wait for message input box to be available and return it."""
    try:
        message_box = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//footer//div[@contenteditable='true']"))
        )
        return message_box
    except TimeoutException:
        return None

def find_today_separator(driver):
    """Find the latest 'Today' separator element in the chat, not user messages."""
    try:
        today_elements = driver.find_elements(
            By.XPATH,
            "//div[not(contains(@class, 'copyable-text'))]//span[normalize-space(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))='today']"
        )
        today_elements = [el for el in today_elements if el.is_displayed()]
        if not today_elements:
            return None
        latest_today = max(today_elements, key=lambda el: el.location['y'])
        return latest_today
    except StaleElementReferenceException:
        return None

def main():
    print("Script started")

    # Use webdriver-manager to auto-resolve driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./User_Data")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com/")
    print("Please scan the QR code if not logged in.")
    input("Press Enter after scanning QR code and loading WhatsApp Web...")

    try:
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
        )
        search_box.clear()
        search_box.send_keys(GROUP_NAME)
        search_box.send_keys(Keys.ENTER)
        print(f"Opened group: {GROUP_NAME}")

        last_sent_date = ""

        print("Waiting for today's date separator...")

        today_separator = None
        while today_separator is None:
            today_separator = find_today_separator(driver)
            if today_separator is None:
                print("No 'today' separator found. Retrying in 5 seconds...")
                time.sleep(5)

        print("'Today' separator found. Starting message monitoring...")

        while True:
            try:
                today_separator = find_today_separator(driver)
                if today_separator is None:
                    print("'Today' separator disappeared, waiting again...")
                    while today_separator is None:
                        today_separator = find_today_separator(driver)
                        if today_separator is None:
                            time.sleep(5)
                    print("'Today' separator found again. Resuming monitoring...")

                chat_container = driver.find_element(By.XPATH, "//div[@id='main']//div[contains(@class, 'copyable-area')]")
                all_messages = chat_container.find_elements(By.XPATH, ".//div[contains(@class,'copyable-text')]//span[@dir='ltr']")

                try:
                    separator_y = today_separator.location['y']
                except StaleElementReferenceException:
                    separator_y = 0

                todays_messages = []
                for msg in all_messages:
                    try:
                        if msg.location['y'] > separator_y:
                            todays_messages.append(msg)
                    except StaleElementReferenceException:
                        continue

                message_found = False
                for msg in reversed(todays_messages):
                    try:
                        if TRIGGER_PHRASE in msg.text.lower():
                            if last_sent_date != datetime.date.today().isoformat():
                                message_found = True
                            break
                    except StaleElementReferenceException:
                        continue

                if message_found:
                    print("Trigger phrase found. Waiting for message box to be available...")
                    message_box = wait_for_message_box(driver, timeout=1)
                    if message_box:
                        message = f"{FULL_NAME} - {STAFF_NUMBER}"
                        message_box.send_keys(message)
                        message_box.send_keys(Keys.ENTER)
                        last_sent_date = datetime.date.today().isoformat()
                        print("Message sent successfully.")
                    else:
                        print("Message box not available (maybe admin-only). Will retry...")

            except Exception as e:
                print("Error during monitoring loop:", e)
                time.sleep(5)

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()