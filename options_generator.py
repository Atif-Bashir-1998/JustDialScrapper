# this function would return names and links of the categories associated to it
def opt_generator(name_of_file):
    # from here the new drop down list of categories will be created (window2)
    names = []
    links = []
    with open(f'{name_of_file}.txt', 'r') as f:
        while True:
            try:
                name, link = f.readline().split(',')
                if len(name) * len(link) > 0:
                    names.append(name)
                    links.append(link[0:-1])
            except:
                break

    return (names, links)