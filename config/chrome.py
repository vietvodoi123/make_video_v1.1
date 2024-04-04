from selenium.webdriver.chrome.options import Options

def option_chrome(path_to_save_mp3):
    print('init chrome driver')
    options = Options()
    options.add_argument('--headless')
    options.add_experimental_option("prefs", {
        "download.default_directory": path_to_save_mp3
    })
    return  options