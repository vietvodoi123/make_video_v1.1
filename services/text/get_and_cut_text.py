from services.text.splice_text import cut_string
from services.text.get_text import  get_text
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def save_text(driver,truyen,web_config,start_chapter,end_chapter):
    wait = WebDriverWait(driver, 10)
    chapter_texts = []
    name = web_config['name']
    url = truyen[f'url_{name}']
    print(url)
    print('checking web config')
    if 'btn_next' in web_config:
        driver.get(url)
        print(url)

    print('start get text')
    for i in range(start_chapter, end_chapter):
        if 'btn_next' not in web_config:
            url1 = f'{url}-{i}'
            print(url1)
            driver.get(url1)

        text = get_text(driver,web_config)
        chapter_texts.append(text)

        if 'btn_next' in web_config:
            if 'css_selector' in web_config['btn_next']:
                btn_next_atb = web_config['btn_next']['css_selector']
                if btn_next_atb:
                    # nhan nut next chap
                    btn_next = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,btn_next_atb)))
                    driver.execute_script("arguments[0].click();", btn_next)

            if 'elm' in web_config['btn_next']:
                btn_next_elm = web_config['btn_next']['elm']
                if btn_next_elm:
                    # nhan nut next chap
                    btn_next_a = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='下一章']")))
                    driver.execute_script("arguments[0].click();", btn_next_a)

        print('next chap')

    # Tạo thư mục "text" nếu nó chưa tồn tại
    text_directory = "text"
    if not os.path.exists(text_directory):
        os.makedirs(text_directory)

    # Lặp qua danh sách các đoạn văn và lưu vào các tệp văn bản
    for i, chapter_text in enumerate(chapter_texts, start=1):
        filename = os.path.join(text_directory, f"chapter_{i}.txt")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(chapter_text)
            print(f"Dữ liệu của chương đã được lưu vào tệp {filename}")

    driver.quit()


