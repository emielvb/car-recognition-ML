# from video tutorial: https://www.youtube.com/watch?v=NBuED2PivbY
# code from https://github.com/techwithtim/Image-Scraper-And-Downloader/blob/main/tutorial.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

# don't need to specify path to chrome webdriver with latest Selenium versions.
web_driver = webdriver.Chrome()

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)