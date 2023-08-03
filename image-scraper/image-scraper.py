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
