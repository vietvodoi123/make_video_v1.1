from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
import os

def init_tts(driver):
    try:
        cookie_alert = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "cookiealert")))
        time.sleep(2)
        cookie_alert.find_element(By.CLASS_NAME, "acceptcookies").click()
    except:
        pass

    select_element = Select(driver.find_element(By.ID, "locale"))
    # Chọn tùy chọn theo giá trị (value)
    select_element.select_by_value("vi-VN")
    time.sleep(0.1)
    # Chọn phần tử <select> bằng id hoặc tên
    select_element1 = Select(driver.find_element(By.ID, "voice"))
    # Chọn tùy chọn theo giá trị (value)
    select_element1.select_by_value("vi-VN-NamMinhNeural")



def get_audio(driver):
    print('get audio')
    driver.get('https://text-to-speech.online/')
    init_tts(driver)

    input_field1 = driver.find_element(By.ID, 'text')
    # Đường dẫn tương đối
    relative_path = "./text"

    # Chuyển đổi đường dẫn tương đối thành đường dẫn tuyệt đối
    absolute_path = os.path.abspath(relative_path)
    # Lấy danh sách tất cả các tệp trong thư mục Downloads
    all_files = os.listdir(absolute_path)

    # Sắp xếp danh sách các tệp theo thời gian sửa đổi (hoặc thời gian tạo) từ cũ đến mới nhất
    sorted_files = sorted(all_files, key=lambda x: os.path.getmtime(os.path.join(relative_path, x)))

    # Lặp qua từng tệp trong danh sách đã sắp xếp

    for file_name in sorted_files:
        if file_name.endswith(".txt"):
            file_path = os.path.join(absolute_path, file_name)
            print("Processing file:", file_path)
            start_time = time.time()
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                input_field1.clear()
                time.sleep(0.1)
                for line in lines:
                    if 'QUẢNG CÁO' not in line:
                        input_field1.send_keys(line.strip())

                # Chờ cho nút tải xuống trở nên nhấp được và sau đó thực hiện click
                time.sleep(2)
                button_download = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "download")))
                button_download.click()

                while True:
                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    time.sleep(1)
                    # neu tai qua lau hoac bi ngung
                    if elapsed_time >= 200:
                        print("tải audio quá lâu hoặc bị đứng khi tải")
                        driver.refresh()
                        print(f"bắt đầu chạy lại file {file_path}")
                        init_tts(driver)
                        input_field1.clear()
                        time.sleep(0.1)
                        for line in lines:
                            if 'QUẢNG CÁO' not in line:
                                input_field1.send_keys(line.strip())
                    # Kiểm tra nếu nút download không còn hiển thị thì thoát khỏi vòng lặp
                    if driver.find_element(By.ID, "download").is_displayed():
                        break


            # sau khi chuyen doi xong thi xoa file text
            if os.path.exists(file_path):
                # Xóa tệp
                os.remove(file_path)
                print(f"Tệp '{file_path}' đã được xóa thành công.")
            else:
                print(f"Tệp '{file_path}' không tồn tại.")
    print('finish get audio')
    driver.quit()