# import Libraries
from selenium import webdriver
import pandas as pd
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from tkinter import *
from backend import get_main_categories


# clearing all the files at start
from clear_files import clear
clear()

# global variable to keep track of version of website
global URL
global path
global CATEGORY_INFO
path = r'chromedriver.exe'
CATEGORY_INFO = []


def download_pic(url, index_number):
    r = requests.get(url)
    with open(f"{index_number}.png", "wb") as f:
        f.write(r.content)
    return

def prepare_category_info(lst):
    category_info_string = ""
    for items in lst:
        category_info_string += f"/{items}"
    return category_info_string

def initial():
    VERSION = ver.get()

    urls = ['https://www.justdial.com/uae/','https://www.justdial.com/us','https://www.justdial.com/','https://www.justdial.com/ca']
    error = ""
    global REP
    global DB_NAME
    REP = ""

    if VERSION == "UAE":
        url = urls[0]
        DB_NAME = "UAE"
        REP = "DU"

    elif VERSION == "USA":
        url = urls[1]
        DB_NAME = "USA"

    elif VERSION == "India":
        url = urls[2]
        DB_NAME = "India"

    elif VERSION == "Canada":
        url = urls[3]
        REP = "ON"
        DB_NAME = "Canada"

    else:
        section_one_error['text'] = "ERROR: Version has not been selected"
        return

    CATEGORY_INFO.append(DB_NAME)
    print(CATEGORY_INFO)


    if len(error) == 0:
        get_main_categories(url)
        window1.destroy()
        global URL
        URL = url

# First window which asks for the version of website
window1 = Tk()
window1.title("JustDial Scrapper")
window1.geometry('750x500')

# top section with selection of version
lbl = Label(window1, text="JustDial Scrapper",fg="green", font=("Times New Roman", 22, 'bold'))
lbl.grid(column=2, row=0, columnspan=30)

versions = Label(window1, text="Choose the version of the website", font=("Times New Roman", 14, 'bold'), fg="blue")
versions.grid(column=1, row=1, columnspan=30)

ver = StringVar()
ver.set("null")
Radiobutton(window1, text="UAE", variable=ver, value="UAE").grid(column=1, row=2)
Radiobutton(window1, text="USA", variable=ver, value="USA").grid(column=2, row=2)
Radiobutton(window1, text="India", variable=ver, value="India").grid(column=3, row=2)
Radiobutton(window1, text="Canada", variable=ver, value="Canada").grid(column=4, row=2)

next_button = Button(window1, text="Get Categories", bg="yellow", fg="black", font=("Times New Roman", 16, 'bold'), command=initial)
next_button.grid(column=1, row=5,columnspan=30)

section_one_error = Label(window1, text="", font=("Times New Roman", 10), fg="red")
section_one_error.grid(column=1, row=6)

window1.mainloop()


# Second window with MAIN CATEGORIES drop down

from options_generator import opt_generator
names, links = opt_generator('categories')

###########################################################################################################################################################################################################################
# Second Window and its functions
from scrapper import scrap_complete_page
from options_saver import opt_saver
from page_scroller import scroll
from main_scraper import scrapper
from page_scraper import scrap_page
from local_db import enter_data

def except_block(browser):
    print("except_block function")
    scroll(browser)

    data = {}  # it is empty object and will store data for each iteration
    df = pd.DataFrame(
        columns=['Category Info','Page Link', 'Name', 'Image Link', 'Location', 'Address', 'Website', 'Telephone_1', 'Telephone_2',
                 'Telephone_3'])
    PAGE_LINKS, NAMES, IMAGE_LINKS = scrapper(browser)
    CAT_INFO = prepare_category_info(CATEGORY_INFO)

    i = 0
    while i < len(PAGE_LINKS) and PAGE_LINKS[i] != "NULL":
        data['Category Info'] = CAT_INFO
        data['Page Link'] = PAGE_LINKS[i]
        data['Name'] = NAMES[i]
        data['Image Link'] = IMAGE_LINKS[i]
        download_pic(url=IMAGE_LINKS[i], index_number=i)
        LOCATION, ADDRESS, WEBSITE, TELEPHONE = scrap_page(PAGE_LINKS[i])
        data['Location'] = LOCATION
        data['Address'] = ADDRESS
        data['Website'] = WEBSITE
        j = 0
        while j < 3:
            data[f'Telephone_{j + 1}'] = TELEPHONE[j]
            j -= - 1
        print("Table name",TABLE_NAME)
        enter_data(DB_NAME, TABLE_NAME, data)
        #print(data)

        i -= - 1
        df = df.append(data, ignore_index=True)

    print("No sub-categories")
    df.to_excel(f"{CAT_INFO}.xlsx")
    print("results saved")
    browser.quit()
    exit()

def selection():
    #get index of that name
    choice = category_selected.get()
    #global CATEGORY_INFO
    CATEGORY_INFO.append(f"{choice}")
    print(CATEGORY_INFO)
    index = names.index(choice)
    category_link = links[index]

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    browser = webdriver.Chrome(path, options=chrome_options)
    browser.get(category_link)

    global TABLE_NAME
    TABLE_NAME = str(choice)
    TABLE_NAME = TABLE_NAME.replace(" ", "_")

    time.sleep(4)

    try:
        print("Found categories")
        lists = browser.find_elements_by_css_selector('ul>li[class="ng-scope"]')
        print(len(lists))
        opt_saver(lists, file_name="last", REP=REP)
        browser.quit()
        window2.destroy()


    except:
        print("No further categories line 163")
        lists = browser.find_elements_by_css_selector('ul[class="list"]')
        print(len(lists))
        for item in lists:
            print(item)
        except_block(browser)
'''

    try:
        lists = browser.find_elements_by_css_selector('ul[class="mm-listview mm-lstex"]>li[class="ng-scope"]')
        if len(lists) == 0:
            print("Faulty try")
        print(len(lists))
        opt_saver(lists=lists, file_name="last", REP=REP)
        browser.quit()
        window2.destroy()


    except:
        print("In except block")
        except_block(browser)

'''
# Second window which asks for the selection from dropdown
window2 = Tk()
window2.title("JustDial Scrapper")
window2.geometry('750x500')

# top section with selection of version
lbl = Label(window2, text="JustDial Scrapper",fg="green", font=("Times New Roman", 22, 'bold'))
lbl.grid(column=2, row=0, columnspan=30)

lbl = Label(window2, text="Username:")
lbl.grid(column=0, row=1)
username = Entry(window2)
username.grid(column=1, row=1)

lbl = Label(window2, text="Password:")
lbl.grid(column=0, row=2)
password = Entry(window2)
password.grid(column=1, row=2)

lbl = Label(window2, text="Choose from following", fg="green", font=("Times New Roman", 14, 'bold')).grid(row=3, column=1)
category_selected = StringVar()
category_selected.set("Choose a category")
drop = OptionMenu(window2, category_selected, *names).grid(row=4, column=1)

scrap_button = Button(window2, text="NEXT", bg="yellow", fg="black", font=("Times New Roman", 16, 'bold'), command=selection)
scrap_button.grid(column=1, row=5,columnspan=30)


window2.mainloop()

#######################################################################################################################################################

names, links = opt_generator('last')

def sub_selection():
    choice = last_category_selected.get()
    index = names.index(choice)
    category_page_link = links[index]

    global CATEGORY_INFO
    CATEGORY_INFO.append(f"{choice}")
    print(CATEGORY_INFO)

    path = r'chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    browser = webdriver.Chrome(path, options=chrome_options)

    #category page link

    print("opening sub-category page",category_page_link)
    time.sleep(5)
    browser.get(category_page_link)
    time.sleep(5)

    try:
        lists = browser.find_elements_by_css_selector('ul[class="list"]>li[class="ng-scope"]')
        opt_saver(lists=lists, file_name="very_last", REP="")
        browser.quit()

    except:
        except_block(browser)


    window3.destroy()


window3 = Tk()
window3.title("JustDial Scrapper")
window3.geometry('750x500')

# top section with selection of version
lbl = Label(window3, text="JustDial Scrapper",fg="green", font=("Times New Roman", 22, 'bold'))
lbl.grid(column=2, row=0, columnspan=30)


lbl = Label(window3, text="Choose from following sub-categories", fg="green", font=("Times New Roman", 14, 'bold')).grid(row=3, column=1)
last_category_selected = StringVar()
last_category_selected.set("Choose a category")
drop = OptionMenu(window3, last_category_selected, *names).grid(row=4, column=1)

scrap_button = Button(window3, text="NEXT", bg="yellow", fg="black", font=("Times New Roman", 16, 'bold'), command=sub_selection)
scrap_button.grid(column=1, row=5,columnspan=30)


window3.mainloop()