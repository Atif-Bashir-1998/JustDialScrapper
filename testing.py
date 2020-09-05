from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from tkinter import *

state = ["DU", "ON", ""]

# USERNAME = username.get()
USERNAME = "atifbashirmanto786@gmail.com"
# PASSWORD = password.get()
PASSWORD = "jRiV8qSpjN$D6#N"
path = r'chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
browser = webdriver.Chrome(path, options=chrome_options)

login_url =  'https://www.justdial.com/uae/login'
urls = browser.get(login_url)
browser.find_element_by_id('inputPassword3').send_keys(USERNAME)
browser.find_element_by_id('exampleInputPassword1').send_keys(PASSWORD)
browser.find_element_by_css_selector('button[type="submit"]').click()


url = r'https://www.justdial.com/us/NY-New-York/167/Medical_fil'

time.sleep(3)
browser.get(url)


# get the root categories links and names
#items = browser.find_elements_by_css_selector('ul > li [class="ng-scope"]')
time.sleep(3)
lists = browser.find_elements_by_css_selector('li[class="ng-scope"]')

names = []
links = []

print(len(lists))
#print(len(items))
for item in lists:
    name = item.text
    link = item.find_element_by_css_selector('a').get_attribute("href")
    print(name)
    print(link)
    #link = link.replace("DSTATE","ON")

    names.append(name)
    links.append(link)
time.sleep(2)
for link in links:
    print(link)

browser.close()
time.sleep(2)

path = r'chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
browser = webdriver.Chrome(path, options=chrome_options)

browser.get(links[3])