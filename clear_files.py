# this will be used inside app.py to clear the data
def clear():
    with open('categories.txt', 'w') as f:
        f.write('')

    with open('sub-categories.txt', 'w') as f:
        f.write('')

    with open('last.txt', 'w') as f:
        f.write('')

    return