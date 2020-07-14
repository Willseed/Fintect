
import os
import json
import logging
import zipfile

import requests

import detect

def get_chrome_driver_major_version(chrome_browser_path: str):
    chrome_ver = detect.get_chrome_version(chrome_browser_path)
    chrome_major_ver = chrome_ver.split(".")[0]
    return chrome_major_ver

def get_latest_driver_version(chrome_browser_path: str, browser_ver: str):
    latest_api = "{}/LATEST_RELEASE_{}".format(chrome_browser_path, browser_ver)
    resp = requests.get(latest_api)
    lastest_driver_version = resp.text.strip()
    return lastest_driver_version

def download_driver(dest_folder: str,  chrome_driver_base_url: str, driver_ver: str):
    download_api = "{}/{}/chromedriver_win32.zip".format(chrome_driver_base_url, driver_ver)
    dest_path = os.path.join(dest_folder, os.path.basename(download_api))
    response = requests.get(download_api, stream=True, timeout=300)

    if response.status_code == 200:
        with open(dest_path, "wb") as f:
            f.write(response.content)
        logging.info("Download driver completed")
    else:
        raise Exception("Download chrome driver failed")

def unzip_driver_to_target_path(src_file: str, dest_path: str):
    with zipfile.ZipFile(src_file, 'r') as zip_ref:
        zip_ref.extractall(dest_path)
    logging.info("Unzip [{}] -> [{}]".format(src_file, dest_path))

def read_driver_mapping_file(mapping_file: str):
    driver_mapping_dict = {}
    if os.path.exists(mapping_file):
        driver_mapping_dict = detect.read_json(mapping_file)
    return driver_mapping_dict
