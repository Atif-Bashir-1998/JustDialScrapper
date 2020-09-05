import time

def scroll(browser):
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
