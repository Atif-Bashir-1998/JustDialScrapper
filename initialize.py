# Initially open the version of the website and save the main categories

from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def get_main_categories(url, name_of_file):
    path = r'chromedriver.exe'

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    browser = webdriver.Chrome(path, options=chrome_options)

    urls = browser.get(url)

    # get the names of Big Categories
    tiles = browser.find_elements_by_class_name('tile')

    with open(f'{name_of_file}.txt', 'w') as f:
        for tile in tiles:
            # get title, picture and description of tile
            title = tile.find_element_by_class_name('hotkey-title').text
            pic = tile.find_element_by_css_selector('a').get_attribute('href')
            pic = pic.split('/')
            pic = pic[-1]
            pic = pic.split('_')
            pic = pic[0]
            link = tile.find_element_by_css_selector('a').get_attribute('href')

            if len(title) != 0:
                f.write(title)

            else:
                if pic.find("?") == -1:
                    f.write(pic)

                else:
                    pic = tile.find_element_by_css_selector('a').get_attribute('title')
                    pic = pic.split(" ")
                    if len(pic[1]) <= 2:
                        pic = pic[0]

                    else:
                        pic = pic[0] + " " + pic[1]

                    f.write(pic)

            f.write(',' + link)
            f.write('\n')

    browser.close()
    return
