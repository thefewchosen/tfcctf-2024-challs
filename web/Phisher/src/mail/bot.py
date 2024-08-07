from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os

SECONDS = 60
MAIL_PORT = int(os.getenv('MAIL_PORT', 5000))

driver_service = Service(GeckoDriverManager().install())
options = webdriver.FirefoxOptions()
options.add_argument('-headless')
options.add_argument('-private')
options.add_argument('-no-remote')


def bot_visit(email, password):
    try:
        print("Bot started")
        client = webdriver.Firefox(options=options, service=driver_service)

        client.get(f"http://localhost:{MAIL_PORT}/login")
        WebDriverWait(client, 10).until(
            EC.presence_of_element_located((By.ID, 'email'))
        )

        client.find_element(By.ID, "email").send_keys(email)
        client.find_element(By.ID, "password").send_keys(password)
        client.find_element(By.ID, "submit").click()

        # Wait until the page loads
        WebDriverWait(client, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'email-item'))
        )
        print("Bot logged in")

        email_items = client.find_elements(By.CLASS_NAME, 'email-item')
        for email_item in email_items:
            email_item.click()
            
            # Focus all iframes
            iframes = client.find_elements(By.TAG_NAME, 'iframe')
            for iframe in iframes:
                client.switch_to.frame(iframe)
                time.sleep(5)
                client.switch_to.default_content()

        print("Emails read")

        # Delete the emails
        delete_button = client.find_element(By.CLASS_NAME, 'trash-button')
        delete_button.click()
        time.sleep(3)

        client.quit()
    except Exception as e:
        print("Bot error", e)
    finally:
        print("Bot finished")

def start_bot(email, password):
    while True:
        bot_visit(email=email, password=password)
        time.sleep(SECONDS)