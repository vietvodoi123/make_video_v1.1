import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.web_config import web
from config.stories import stories
from config.chrome import option_chrome
from config.path import path_to_save_mp3_base,output_video_folder_base

from services.text.get_and_cut_text import save_text
from services.audio.get_audio import get_audio
from services.video.make_video import make_video
from services.text.translate import translate_text
from services.dele_mp3 import dele_mp3
from services.text.cut_file import cut_and_save_files
def is_image_url(url):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']
    return any(url.endswith(ext) for ext in image_extensions)


def main(web_config, truyen, start_chapter=1, end_chapter=21, number_chapter_in_video=10):
    nametruyen = truyen['name']
    # check truyen
    if (not nametruyen):
        print('name is error')
    if is_image_url(truyen['image_path']):
        print("This URL leads to an image.")
    else:
        print("This URL does not lead to an image.")

    path_to_save_mp3 = path_to_save_mp3_base + rf'\audio{nametruyen}'
    output_video_folder = output_video_folder_base + rf'\{nametruyen}'

    options = option_chrome(path_to_save_mp3)
    # thết lập chrome
    driver = webdriver.Chrome(options=options)
    trans = web_config['trans'] if 'trans' in web_config else False
    print('init successful')
    # # lay text luu vao thu muc text
    save_text(driver, truyen, web_config, start_chapter, end_chapter)

    # # dich
    if trans:
        driver = webdriver.Chrome(options=options)
        translate_text(driver,truyen['name'])

    cut_and_save_files(trans,number_chapter_in_video)

    # #lay audio
    driver = webdriver.Chrome(options=options)
    get_audio(driver,trans)
    make_video(1,truyen['image_path'],path_to_save_mp3,output_video_folder,number_chapter_in_video)

    dele_mp3(path_to_save_mp3)



main(web['qianyege'], stories['chien_tranh_co_khi'], 1,21,10)
