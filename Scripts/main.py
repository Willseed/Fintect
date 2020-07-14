import detect
import chrome_helper
from selenium import webdriver

CHROME_PATH = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
CHROME_DRIVER_BASE_URL = r'https://chromedriver.storage.googleapis.com'
CHROME_DRIVER_FOLDER = r'C:\Users\方塊馬\fintech\Download'
CHROME_DRIVER_ZIP = r'{}\chromedriver_win32.zip'.format(CHROME_DRIVER_FOLDER)
CHROME_DRIVER_EXE = r'{}\chromedriver.exe'.format(CHROME_DRIVER_FOLDER)
CHROME_DRIVER_MAPPING_FILE = r"{}\mapping.json".format(CHROME_DRIVER_FOLDER)

def check_browser_driver_available():
    # 取得 Chrome 版本
    chrome_major_ver = chrome_helper.get_chrome_driver_major_version(CHROME_PATH)
    # 取得 Chrome Driver 版本
    driver_ver = chrome_helper.get_latest_driver_version(CHROME_DRIVER_BASE_URL, chrome_major_ver)
    # 對應檔案版本資訊
    mapping_dict = chrome_helper.read_driver_mapping_file(CHROME_DRIVER_MAPPING_FILE)

    # 如果版本不對應更新並下載 Chrome Driver
    if chrome_major_ver not in mapping_dict:
        # 下載 Chrome Driver
        chrome_helper.download_driver(CHROME_DRIVER_FOLDER, CHROME_DRIVER_BASE_URL, driver_ver)
        # 解壓縮 Chrome Driver
        chrome_helper.unzip_driver_to_target_path(CHROME_DRIVER_ZIP, CHROME_DRIVER_FOLDER)

        # Chrome Driver 與 Chrome 版本資訊
        mapping_dict = {
            chrome_major_ver: {
                "driver_path": CHROME_DRIVER_EXE,
                "driver_version": driver_ver
            }
        }
        # 更新相關版本資訊字典
        mapping_dict.update(mapping_dict)
        # 寫入版本資訊檔案
        detect.write_json(CHROME_DRIVER_MAPPING_FILE, mapping_dict)

if __name__ == '__main__':
    check_browser_driver_available()
