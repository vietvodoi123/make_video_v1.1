import os
def dele_mp3(path_to_save_mp3):
    audio_folder = path_to_save_mp3
    # xoa het cac file audio
    # Lặp qua tất cả các tệp trong thư mục audio
    for file_name in os.listdir(audio_folder):
        # Kiểm tra xem tệp có phải là file MP3 không
        if file_name.lower().endswith(".mp3"):
            # Xóa file MP3
            file_path = os.path.join(audio_folder, file_name)
            os.remove(file_path)
            print(f"Đã xóa file MP3: {file_name}")