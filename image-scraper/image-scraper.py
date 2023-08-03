# from video tutorial: https://www.youtube.com/watch?v=NBuED2PivbY
# code from https://github.com/techwithtim/Image-Scraper-And-Downloader/blob/main/tutorial.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

# PATH = "C:\\Program Files (x86)\\chromedriver-win64\\chromedriver.exe"
# No longer need to add PATH to webdriver.Chrome(): webdriver.Chrome(PATH_TO_WEBDRIVER) is depracated.
wd = webdriver.Chrome()

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
	
test_img_url = r'https://www.motortrend.com/uploads/2023/08/2024-porsche-911-st-60th-anniversary-18.jpg?fit=around%7C875:492'
download_image('./', test_img_url, file_name='Porsche.jpg')