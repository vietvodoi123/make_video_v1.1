from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_text(driver,web_config):
    wait = WebDriverWait(driver, 10)
    # Lấy nội dung của một phần tử
    name_chap = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, web_config['name_chap']))).text
    chap_content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, web_config['content_chap']))).text

    return name_chap + '. ' + chap_content
