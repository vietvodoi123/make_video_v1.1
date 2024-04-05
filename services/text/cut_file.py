import json
import os
from services.text.splice_text import cut_string

def cut_and_save_files(trans,number_chapter_in_video):
    # Chọn thư mục tương ứng với giá trị của trans
    if trans:
        dir_path = './text_trans'
    else:
        dir_path = './text'

    # Lấy danh sách tất cả các tệp tin trong thư mục
    files = os.listdir(dir_path)

    # Sắp xếp các tệp tin theo thứ tự từ cũ đến mới
    files.sort(key=lambda file: os.path.getctime(os.path.join(dir_path, file)))

    count_files = 0
    arr_count_file_mp3 = []
    tmp = 0
    # Duyệt qua từng tệp tin
    for file in files:
        # Định nghĩa đường dẫn đầy đủ đến tệp tin
        file_path = os.path.join(dir_path, file)

        # Đọc nội dung tệp tin
        with open(file_path, 'r', encoding="utf-8") as f:
            content = f.read()

        # Sử dụng hàm cut_string để cắt nội dung
        cut_content = cut_string(content)

        # Định nghĩa đường dẫn đến thư mục chứa các tệp tin sau khi cắt
        cut_dir_path = './text_cut'

        # Đảm bảo rằng thư mục đích tồn tại
        if not os.path.exists(cut_dir_path):
            os.makedirs(cut_dir_path)

        # Lưu các chuỗi đã cắt vào các tệp tin mới
        for i, string in enumerate(cut_content):
            cut_file_path = os.path.join(cut_dir_path, f'{file}_{i}.txt')
            with open(cut_file_path, 'w', encoding="utf-8") as f:
                f.write(string)

        tmp += len(cut_content)
        count_files += 1
        if count_files == number_chapter_in_video:
            arr_count_file_mp3.append(tmp)
            count_files = 0
            tmp = 0


    # Xóa tất cả các tệp tin trong thư mục gốc sau khi đã xử lý
    for file in files:
        os.remove(os.path.join(dir_path, file))
    print(arr_count_file_mp3)
    # Lưu mảng arr_count_file_mp3 vào file
    with open('arr_count_file_mp3.json', 'w', encoding="utf-8") as f:
        json.dump(arr_count_file_mp3, f)