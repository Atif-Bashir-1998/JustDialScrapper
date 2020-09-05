def opt_saver(lists, file_name, REP):
    print("Saving the file")
    with open(f'{file_name}.txt', 'w') as f:
        for item in lists:
            # get name and link of sub category
            name = item.text
            link = item.find_element_by_css_selector('a').get_attribute('href')
            if len(REP) != 0:
                link = link.replace("DSTATE", REP)

            #print(name, link)
            if type(name) != None and type(link) != None:
                f.write(name + "," + link + "\n")

    return None