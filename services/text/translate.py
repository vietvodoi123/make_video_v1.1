import time
from config.path import path_save_trans
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def translate_text(driver,name):
    driver.get('https://dichnhanh.com/')
    wait = WebDriverWait(driver, 10)
    text_area = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'textarea')))

    # Đường dẫn đến thư mục bạn muốn tạo
    text_trans_path = './text_trans'
    #
    # Tạo thư mục nếu nó chưa tồn tại
    if not os.path.exists(text_trans_path):
        os.makedirs(text_trans_path)

    # # Đường dẫn đến thư mục bạn muốn tạo
    # save_text_trans_path = rf'{path_save_trans}/{name}'
    # cnt = len(os.listdir(save_text_trans_path))
    # # Tạo thư mục nếu nó chưa tồn tại
    # if not os.path.exists(save_text_trans_path):
    #     os.makedirs(save_text_trans_path)

    relative_path = "./text"
    absolute_path = os.path.abspath(relative_path)
    all_files = os.listdir(absolute_path)

    sorted_files = sorted(all_files, key=lambda x: os.path.getmtime(os.path.join(relative_path, x)))

    # Lặp qua từng tệp trong danh sách đã sắp xếp

    for file_name in sorted_files:
        if file_name.endswith(".txt"):
            file_path = os.path.join(absolute_path, file_name)
            print("Processing translate file:", file_path)
            text_area.clear()
            # Read the file content
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                text = text.replace('最新站名：千夜阁 最新网址：www.qianyege.com','')
                text_area.send_keys(text)

            btn_qt = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@title="Dịch sang QT"]')))
            btn_qt.click()
            time.sleep(3)

            # Tìm thẻ div với thuộc tính spellcheck="false"
            div = wait.until(EC.visibility_of_element_located((By.XPATH,'//div[@spellcheck="false"]')))
            while True:
                print('waiting text')
                if div.text:
                    print('dich thanh cong')
                    break
            # Đường dẫn đầy đủ đến tệp bạn muốn tạo
            file_path = os.path.join(text_trans_path, f'{file_name}.txt')

            # Mở tệp và ghi vào nó
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(div.text)

            # save_trans = os.path.join(save_text_trans_path,f'chapter_{cnt+1}.txt')
            # # Mở tệp và ghi vào nó
            # with open(save_trans, "w", encoding="utf-8") as file:
            #     file.write(div.text)
            #     cnt += 1

            print(f'save thành công {file_path}')
        text_area.clear()
    for file_name in sorted_files:
        if file_name.endswith(".txt"):
            file_path = os.path.join(absolute_path, file_name)
            os.remove(file_path)

    driver.quit()