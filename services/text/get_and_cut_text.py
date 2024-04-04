from services.text.splice_text import cut_string
from services.text.get_text import  get_text
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def get_and_cut_text(driver,truyen,web_config,start_chapter,end_chapter,number_chapter_in_video):
    wait = WebDriverWait(driver, 10)
    chapter_texts = []
    name = web_config['name']
    url = truyen[f'url_{name}']

    print('checking web config')
    if 'btn_next' in web_config:
        driver.get(url)

    print('start get text')
    for i in range(start_chapter, end_chapter):
        if 'btn_next' not in web_config:
            url1 = f'{url}-{i}'
            driver.get(url1)

        text = get_text(driver,web_config)
        chapter_texts.append(text)

        if 'btn_next' in web_config:
            btn_next_atb = web_config['btn_next']
            # nhan nut next chap
            btn_next = wait.until(EC.element_to_be_clickable(By.CSS_SELECTOR,btn_next_atb))
            btn_next.click()

        print('next chap')

    # Tạo thư mục "text" nếu nó chưa tồn tại
    text_directory = "text"
    if not os.path.exists(text_directory):
        os.makedirs(text_directory)

    # bien arr dem so file mp3 cua 10 chap
    arr_count_file_mp3 = []
    count_file_text = 0
    # Lặp qua danh sách các đoạn văn và lưu vào các tệp văn bản
    for i, chapter_text in enumerate(chapter_texts, start=1):
        arr = cut_string(chapter_text)
        count_file_text += len(arr)
        if i % number_chapter_in_video == 0:
            arr_count_file_mp3.append(count_file_text)
            count_file_text = 0

        for index, item in enumerate(arr, start=1):
            filename = os.path.join(text_directory, f"chapter_{i}_{index}.txt")
            with open(filename, "w", encoding="utf-8") as file:
                file.write(item)
                print(f"Dữ liệu của chương đã được lưu vào tệp {filename}")

    if count_file_text != 0:
        arr_count_file_mp3.append(count_file_text)
    driver.quit()
    print(arr_count_file_mp3)
    with open('arr_count_file_mp3.txt','w') as file:
        for value in arr_count_file_mp3:
            file.write(f"{value}\n")
    print('finish get text')
    return arr_count_file_mp3

