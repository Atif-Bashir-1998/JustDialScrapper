# gets the name of shop, page address and image link

from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


def scrap_complete_page(browser):
    while True:
        # Scroll down to bottom

        last_height = browser.execute_script("return document.body.scrollHeight")
        #print("Last Height", last_height)

        # Scroll down to the bottom.
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = browser.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

    # now get the links

    items = browser.find_elements_by_class_name('lst')
    links = []
    names = []
    images = []
    for item in items:
        try:
            link = item.find_element_by_css_selector('a[class="visible-xs"]').get_attribute('href')
            links.append(link)

        except:
            links.append("NULL")

        try:
            name = item.find_element_by_css_selector('h2').text
            names.append(name)
        except:
            names.append("NULL")

        try:
            img_src = item.find_element_by_css_selector('div[class="ng-scope"] > a').get_attribute("style")
            img_src = img_src[23:-3]
            images.append(img_src)
        except:
            images.append("NO IMAGE")

    return links, names, images
