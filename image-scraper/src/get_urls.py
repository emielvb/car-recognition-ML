# from video tutorial: https://www.youtube.com/watch?v=NBuED2PivbY
# code from https://github.com/techwithtim/Image-Scraper-And-Downloader/blob/main/tutorial.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

def get_search_url_from_query(search_query):
    # get separate words in lower case by splitting on each space
    separate_words = search_query.lower().split(' ')
    # add them all together with a + between each word.
    query_reformed = '+'.join(separate_words)
    # return search url in correct format.
    return 'https://www.google.com/search?tbm=isch&q={}'.format(query_reformed)

# function to scroll down to bottom of google img search to allow for larger amounts of images to be downloaded at once
def scroll_down(web_driver, delay=0.25, ntimes=1):
    for i in range(ntimes):
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

def click_reject_cookies(web_driver):
    # Locate the reject-cookies button with contains()
    reject_cookies_button = web_driver.find_element(By.NAME, "V67aGc")

    # Now click on it to reject all cookies
    reject_cookies_button.click()


def get_image_urls(search_query, max_images=10, delay=0.25):
    # don't need to specify path to chrome webdriver with latest Selenium versions.
    web_driver = webdriver.Chrome()

    # (try to) open chrome to google front page, this will first give a cookie notification
    web_driver.get("https://www.google.com")
    # reject cookies
    # click_reject_cookies(web_driver)

    # url of the google image search.
    url = get_search_url_from_query(search_query)
    # open the url in chrome
    web_driver.get(url)

    image_urls = []
    skips = 0

    # scroll down before going over images
    scroll_down(web_driver, delay=delay, ntimes=int(max_images/10))

    # gather image urls
    while len(image_urls) + skips < max_images:
        # finds all the elements on the google page that has that class name (which is the class of the image thumbnails of the google search page)
        thumbnails = web_driver.find_elements(By.CLASS_NAME, "Q4LuWd")

        # loop through all the thumbnails and try to click on them
        # len(image_urls) + skips part ensures that we don't loop through images we've already gotten.
        for img in thumbnails[(len(image_urls) + skips): max_images]:
            try:
                img.click()
                # delay to wait for the actual image to pop up.
                time.sleep(delay)
            except:
                continue
            
            # this class name should correspond to the top image once a thumbnail has been clicked.
            # compound class names (ones with spaces in them) are not supported using this method.
            # Thus, we only use the first part of the class, and ignore subclasses. (Hopefully this works)
            images = web_driver.find_elements(By.CLASS_NAME, "r48jcc")
            
            # check that indeed an image has been found
            if len(images) == 0:
                print('Wrong class code. Find the correct new classname and change code accordingly.')
            # this should ideally only give us one image, but it could loop through mutliple and hence,
            # we will go through each of them and do some checks in order to verify that they have a proper image source.
            for image in images:
                # in order to ensure we don't keep clicking on the same image again and again (infinite while loop)
                if image.get_attribute('src') in image_urls: # if image src is already inside image urls, we've already found it.
                    # if we found an image, we move on to the next image
                    max_images += 1
                    skips += 1
                    break
                
                # 'if it does have the source (src) attribute, we still have to check if the url is in a format that we can act. download the image.
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.append(image.get_attribute('src'))
                    print(f"Found {len(image_urls)} images")
    # close chrome
    web_driver.quit()

    return image_urls

def test_getting_urls():
    urls = get_image_urls('porsche', 10, 0.25)

# print(get_search_url_from_query('porsche gt3 rs'))
test_getting_urls()