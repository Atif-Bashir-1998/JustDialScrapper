from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def scrap_page(url):
    path = r'chromedriver.exe'

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    browser = webdriver.Chrome(path, options=chrome_options)
    browser.get(url)
    time.sleep(2)
    try:
        addr = browser.find_elements_by_class_name('adr_cnt')
        location = addr[0].find_element_by_css_selector('span').text
        try:
            address = addr[1].find_element_by_css_selector('span').text

        except:
            address = ""

    except:
        location = ""
        address = ""

    try:
        link = browser.find_element_by_class_name('ex_mrgn')
        web = link.find_element_by_css_selector('a').get_attribute('href')

    except:
        web = ""

    tel = ["", "", ""]
    try:
        numbers = browser.find_elements_by_class_name('tel')
        i = 0
        for num in numbers:
            tel[i] = num.text
            i -= -1
    except:
        pass

    browser.close()

    return location, address, web, tel


#scrap_page(r'https://www.justdial.com/uae/DU-Dubai/Eurostar-Cellar-near-Dubai-Waterfront/PLG91612009102?xid=RHViYWksRFUgTGlxdW9yIHJldGFpbA==')