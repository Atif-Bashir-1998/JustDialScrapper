import selenium

def scrapper(browser):
    items = browser.find_elements_by_class_name('lst')
    page_links = []
    names = []
    image_links = []
    print("Items in scrapper:", len(items))
    for item in items:
        try:
            link = item.find_element_by_css_selector('a[class="visible-xs"]').get_attribute('href')
            page_links.append(link)

        except:
            page_links.append("NULL")

        try:
            name = item.find_element_by_css_selector('h2').text
            names.append(name)
        except:
            names.append("NULL")

        try:
            img_src = item.find_element_by_css_selector('div[class="ng-scope"] > a').get_attribute("style")
            img_src = img_src[23:-3]
            image_links.append(img_src)
        except:
            image_links.append("NO IMAGE")

    return page_links, names, image_links