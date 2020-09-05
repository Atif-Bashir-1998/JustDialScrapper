# import Libraries
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


def login(url, name, password):
    path = r'chromedriver.exe'

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    browser = webdriver.Chrome(path, options=chrome_options)

    urls = browser.get(url)

    # starting from the login page
    browser.find_element_by_id('username').send_keys(name)
    browser.find_element_by_id('password').send_keys(password)
    browser.find_element_by_css_selector('button[type="submit"]').click()  # sign in

    return browser


# Create Function to scrape webpage
def getURL(url, name, password, job_title, location):
    browser = login(url, name, password)

    browser.get(f'https://www.linkedin.com/search/results/people/?keywords={job_title}&origin=FACETED_SEARCH')

    browser.find_element_by_css_selector('form[aria-label="Filter results by: Locations"]').click()
    browser.find_element_by_css_selector('input[placeholder="Add a country/region"]').send_keys(location)
    time.sleep(3)
    search_location = browser.find_element_by_css_selector(
        'div[class="search-typeahead-v2__hit ember-view"]').text  # Tell what it is searching for
    response['text'] = f"Searching in {search_location}"
    browser.find_element_by_css_selector('div[class="search-typeahead-v2__hit ember-view"]').click()
    # browser.execute_script("window.scrollTo(0, 500)")
    time.sleep(10)

    '''
    try:
        browser.find_element_by_xpath('/html/body/div[9]/div[4]/div/div[1]/header/div/div/div[2]/div/div/div/ul/li[2]/form/div/fieldset/div/div[2]/div/button[2]').click()

    except:
        browser.find_element_by_xpath('/html/body/div[8]/div[4]/div/div[1]/header/div/div/div[2]/div/div/div/ul/li[2]/form/div/fieldset/div/div[2]/div/button[2]').click()

        '''
    # browser.find_element_by_css_selector('button[type="button"] > span[class="artdeco-button__text"]').click()
    time.sleep(3)

    # except:

    # browser.find_element_by_xpath(
    # /html/body/div[8]/div[3]/div/div[1]/header/div/div/div[2]/div/div/div/ul/li[2]/form/div/fieldset/div/div[2]/div/button[2]
    # '/html/body/div[9]/div[4]/div/div[1]/header/div/div/div[2]/div/div/div/ul/li[2]/form/div/fieldset/div/div[2]/div/button[2]').click()

    # Here the function should return the url with all the search parameters. This URL would be passed to another function using multithreading
    print("The URL of the page", browser.current_url)
    browser.execute_script("document.body.style.zoom='50%' ")
    time.sleep(1)

    try:
        pages = browser.find_elements_by_css_selector(
            'ul[class="artdeco-pagination__pages artdeco-pagination__pages--number"] > li')
        # print(len(pages))
        no_of_pages = pages[-1].text
        # print(no_of_pages)
    except:
        print("Not caught")
        no_of_pages = 100

    URL = str(browser.current_url) + '&page='
    browser.close()

    return (URL, no_of_pages)


def scraper_fun(browser):
    browser.execute_script("document.body.style.zoom='50%' ")
    data = {}
    df = pd.DataFrame(
        columns=['Name', 'Role', 'Location', 'Experience', 'Connect', 'Link', 'Websites', 'Email', 'Phone'])

    time.sleep(3)
    profiles = browser.find_elements_by_css_selector(
        'li[class="search-result search-result__occluded-item ember-view"]')
    print(len(profiles))

    if len(profiles) > 10:
        profiles = profiles[-10:]

    print(len(profiles))

    for profile in profiles:
        try:
            data['Name'] = profile.find_element_by_class_name("actor-name").text
        except:
            data['Name'] = ""
        try:
            data['Role'] = profile.find_element_by_css_selector(
                'p[class="subline-level-1 t-14 t-black t-normal search-result__truncate"]').text
        except:
            pass
        try:
            data['Location'] = profile.find_element_by_css_selector(
                'p[class="subline-level-2 t-12 t-black--light t-normal search-result__truncate"]').text
        except:
            pass
        try:
            data['Experience'] = profile.find_element_by_css_selector(
                'p[class="mt2 t-12 t-black--light t-normal search-result__snippets-black"]').text

        except:
            data['Experience'] = ""

        try:
            data['Connect'] = profile.find_element_by_css_selector('div[class="search-result__actions"]').text
            link = profile.find_element_by_css_selector(
                'a[class="search-result__result-link ember-view"]').get_attribute('href')
            # print(link)
            data['Link'] = link

        except:
            data['Connect'] = "No Connect"
            data['Link'] = ""
            # print(data['Link'])

        if data['Name'] != "LinkedIn Member" and data['Name'] != "":
            window_before = browser.window_handles[0]
            print("Window before: ", window_before)
            browser.execute_script("window.open('about:blank', 'tab2');")
            browser.switch_to.window("tab2")
            browser.get(str(data['Link']))
            time.sleep(3)
            contact_info_btn = str(data['Link']) + r'/details/contact-info/'
            browser.find_element_by_css_selector(f'a[data-control-name="contact_see_more"]').click()
            time.sleep(1)
            '''
            try:
                #linked_in_profile = browser.find_element_by_css_selector('section[class="pv-contact-info__contact-type ci-varnity-url"]')
                linked_in_profile_link = browser.find_element_by_css_selector('section[class="pv-contact-info__contact-type ci-vanity-url"] > div > a[class="pv-contact-info__contact-link t-14 t-black t-normal"]').get_attribute('href')
                data['LinkedIn Profile'] = linked_in_profile_link
            except:
                data['LinkedIn Profile'] = ""
                print("LinkedIn profile error")
            '''

            try:
                # websites = browser.find_element_by_css_selector('section[class="pv-contact-info__contact-type ci-websites"]')
                websites_link = browser.find_element_by_css_selector(
                    'section[class="pv-contact-info__contact-type ci-websites"] > ul > li > div > a[class="pv-contact-info__contact-link t-14 t-black t-normal"]').get_attribute(
                    'href')
                data['Websites'] = websites_link
            except:
                data['Websites'] = ""
                # print("Website error")
            try:
                # emails = browser.find_element_by_css_selector('section[class="pv-contact-info__contact-type ci-email"]')
                emails_link = browser.find_element_by_css_selector(
                    'section[class="pv-contact-info__contact-type ci-email"] > div > a[class="pv-contact-info__contact-link t-14 t-black t-normal"]').text
                data['Email'] = emails_link
            except:
                data['Email'] = ""
                # print("Email Error")

            try:
                phone = browser.find_element_by_css_selector(
                    'section[class="pv-contact-info__contact-type ci-phone"] > ul > li[class="pv-contact-info__ci-container t-14 > span[class="t-14 t-black t-normal"]').text
                data['Mobile'] = phone
                print(phone)
            except:
                print("Mobile Error")

            time.sleep(5)
            browser.switch_to.window(window_before)
            time.sleep(3)

        else:
            # data['LinkedIn Profile'] = ""
            data['Websites'] = ""
            data['Email'] = ""

        # print(data['Name'], data['Role'], data['Location'], data['Experience'], data['Connect'])

        df = df.append(data, ignore_index=True)

    return df


def getdata(log_url, URL, name, password, pages):
    browser = login(log_url, name, password)

    DATA = pd.DataFrame(columns=['Name', 'Role', 'Location', 'Experience', 'Link', 'Websites', 'Email', 'Phone'])

    i = 1
    while i <= pages:
        URL = URL + str(i)
        browser.get(URL)
        DATA = DATA.append(scraper_fun(browser), ignore_index=True)
        if len(str(i)) >= 2:
            URL = URL[0:-2]

        elif len((str(i))) >= 3:
            URL = URL[0:-3]

        else:
            URL = URL[0:-1]

        i = i + 1

    return DATA


# url = f'https://www.linkedin.com/login'
# name = 'adobe8832289@gmail.com'
# password = 'JZE%Ej9L4@G$!!9'
# job_title = 'frontend%20developer'
# location = 'Pakistan'

# (URL,pages) = getURL(url, name, password, job_title, location)
# URL = "https://www.linkedin.com/search/results/people/?keywords=frontend%20developer&origin=FACETED_SEARCH&page="

# DATA = pd.DataFrame(columns=['Name', 'Role', 'Location', 'Experience', 'Connect', 'Link', 'LinkedIn Profile', 'Websites', 'Email'])

# Frontend of the application is here

def start():
    U_Error = ""
    P_Error = ""
    J_Error = ""
    L_Error = ""
    action = "Searching..."

    Username = username.get()
    if Username == "":
        U_Error = "Please Enter User Name"
        action = "Program terminated"
        exit()
    else:
        U_Error = ""
        action = "Searching..."

    Password = password.get()
    if Password == "":
        P_Error = "Please Enter Password"
        action = "Program terminated"
        exit()
    else:
        P_Error = ""
        action = "Searching..."

    Job_title = job_title.get()
    if Job_title == "":
        J_Error = "Please Enter Job Title"
        action = "Program terminated"
        exit()
    else:
        J_Error = ""
        action = "Searching..."
        Job_title = Job_title.lower()
        Job_title = Job_title.replace(" ", "%20")

    Location = location.get()
    if Location == "":
        L_Error = "Please Enter Location"
        action = "Program terminated"
        exit()
    else:
        L_Error = ""
        action = "Searching..."

    error_1['text'] = U_Error
    error_2['text'] = P_Error
    error_3['text'] = J_Error
    error_4['text'] = L_Error

    print(Username, Password, Job_title, Location)
    response['text'] = action

    # Now the data is being sent to the backend
    url = f'https://www.linkedin.com/login'
    (URL, no_of_pages) = getURL(url, Username, Password, Job_title, Location)
    print(URL)
    response['text'] = f"Pages scrapped: {no_of_pages}"
    DATA = pd.DataFrame(
        columns=['Name', 'Role', 'Location', 'Experience', 'Connect', 'Link', 'Websites', 'Email', 'Phone'])
    DATA = getdata(url, URL, Username, Password, pages=int(no_of_pages))
    DATA.to_excel(f"Results_{date.today()}.xlsx")


from tkinter import *
from datetime import date

window = Tk()

window.title("LinkedIn Scrapper")
window.geometry('750x500')

lbl = Label(window, text="LinkedIn Scrapper", font=("Times New Roman", 22, 'bold'))
lbl.grid(column=0, row=0, columnspan=30)

lbl = Label(window, text="Username:")
lbl.grid(column=0, row=1)
username = Entry(window, width=50)
username.grid(column=1, row=1)

lbl = Label(window, text="Password:")
lbl.grid(column=0, row=2)
password = Entry(window, width=50)
password.grid(column=1, row=2)

lbl = Label(window, text="Job Title:")
lbl.grid(column=0, row=3)
job_title = Entry(window, width=50)
job_title.grid(column=1, row=3)

lbl = Label(window, text="Location:")
lbl.grid(column=0, row=4)
location = Entry(window, width=50)
location.grid(column=1, row=4)

lbl = Label(window, text="")
lbl.grid(column=0, row=5)
send_button = Button(window, text="GO", bg="green", fg="white", font=("Times New Roman", 16, 'bold'), command=start)
send_button.grid(column=1, row=6)

response = Label(window, text="Response here", fg='green', font=("Times New Roman", 16, 'bold'))
response.grid(column=0, row=7)

error_1 = Label(window, text="", fg='red', font=("Times New Roman", 12, 'bold'))
error_1.grid(column=0, row=8)

error_2 = Label(window, text="", fg='red', font=("Times New Roman", 12, 'bold'))
error_2.grid(column=0, row=9)

error_3 = Label(window, text="", fg='red', font=("Times New Roman", 12, 'bold'))
error_3.grid(column=0, row=10)

error_4 = Label(window, text="", fg='red', font=("Times New Roman", 12, 'bold'))
error_4.grid(column=0, row=11)

window.mainloop()

'''
atif.bashr.1998@gmail.com
MyPassword12345
Frontend Developer
Afghanistan
'''