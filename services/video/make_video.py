import json

from pydub import AudioSegment
from moviepy.editor import *

def make_video(start_chapter,path_to_image,path_to_save_mp3,output_video_folder,number_chapter_in_video):
    # Kiểm tra và tạo thư mục nếu nó không tồn tại
    if not os.path.exists(output_video_folder):
        os.makedirs(output_video_folder)


    with open('arr_count_file_mp3.json','r', encoding="utf-8") as file:
        arr_count_file_mp3 = json.load(file)

    print('đọc file arr_count_file_mp3')
    print(arr_count_file_mp3)
    
    # Đường dẫn đến thư mục chứa các file audio
    audio_folder = path_to_save_mp3

    # Lấy danh sách tất cả các tệp trong thư mục
    all_files = os.listdir(audio_folder)

    # Lọc ra các tệp có phần mở rộng là ".mp3"
    mp3_files = [file for file in all_files if file.lower().endswith(".mp3")]

    # Sắp xếp danh sách các tệp MP3 theo thời gian sửa đổi (hoặc thời gian tạo)
    mp3_files.sort(key=lambda x: os.path.getmtime(os.path.join(audio_folder, x)))

    rev = start_chapter
    count = 0
    count_video = 0
    combined_audio = AudioSegment.empty()
    for mp3_file in mp3_files:

        audio_segment = AudioSegment.from_mp3(os.path.join(audio_folder, mp3_file))
        combined_audio += audio_segment
        count += 1
        print(count)
        if count == arr_count_file_mp3[count_video]:
            print(f'đủ {count} tệp mp3')
            # Đường dẫn đến thư mục lưu trữ âm thanh ghép lại
            output_folder = "audio_text"

            # Kiểm tra xem thư mục output_folder có tồn tại không, nếu không thì tạo mới
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Đường dẫn đến file MP3 đã ghép
            output_path = os.path.join(output_folder, f"combined{rev}.mp3")

            # Lưu âm thanh ghép lại thành một tệp MP3 trong thư mục output_folder
            combined_audio.export(output_path, format="mp3")

            print(f"File MP3 đã được ghép và lưu vào '{output_path}'")

            # Đường dẫn đến file ảnh làm nền
            background_image_path = path_to_image

            # Tạo đối tượng ClipAudio từ file âm thanh, sử dụng lại đường dẫn ở trên
            audio = AudioFileClip(output_path)

            # Tạo đối tượng ClipVideo từ file ảnh làm nền
            background = ImageClip(background_image_path).set_duration(audio.duration)

            # Tạo video từ audio và background image
            video = background.set_audio(audio)

            # Lưu video
            output_video_path = os.path.join(output_video_folder, f"{rev}.mp4")
            video.write_videofile(output_video_path, fps=24)

            # xoa file audio
            os.remove(output_path)
            print(f"Đã xóa file MP3: {output_path}")
            print('rev:', rev)
            rev += number_chapter_in_video
            count = 0
            count_video += 1
            combined_audio = AudioSegment.empty()
            print('lam rong combined_audio:', len(combined_audio))
