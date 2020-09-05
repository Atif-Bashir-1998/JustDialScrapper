import sqlite3

#called from except_block
def enter_data(DB_NAME, TABLE_NAME, data_object):
    # Connecting to sqlite
    conn = sqlite3.connect(f'{DB_NAME}.db')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # destructuring the object
    #print("data inside enter data", data_object)

    CATEGORY_INFO = data_object['Category Info']
    PAGE_LINK = data_object['Page Link']
    NAME = data_object['Name']
    IMAGE_LINK = data_object['Image Link']
    LOCATION = data_object['Location']
    ADDRESS = data_object['Address']
    WEBSITE = data_object['Website']
    TELEPHONE_1 = data_object['Telephone_1']
    TELEPHONE_2 = data_object['Telephone_2']
    TELEPHONE_3 = data_object['Telephone_3']

    # Preparing SQL queries to INSERT a record into the database.
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} ( CATEGORY_INFO VARCHAR(255), PAGE_LINK VARCHAR(255), NAME VARCHAR(255), IMAGE_LINK VARCHAR(255), LOCATION VARCHAR(255), ADDRESS VARCHAR(255), WEBSITE VARCHAR(255), TELEPHONE_1 VARCHAR(255), TELEPHONE_2 VARCHAR(255), TELEPHONE_3 VARCHAR(255) )')
    #cursor.execute(f'''INSERT INTO {table_name} (PAGE_LINK, NAME, IMAGE_LINK, LOCATION, ADDRESS, WEBSITE, TELEPHONE_1, TELEPHONE_2, TELEPHONE_3) VALUES ({PAGE_LINK}, {NAME}, {IMAGE_LINK}, {LOCATION}, {ADDRESS}, {WEBSITE}, {TELEPHONE_1}, {TELEPHONE_2}, {TELEPHONE_3})''')
    data = [CATEGORY_INFO,PAGE_LINK, NAME, IMAGE_LINK, LOCATION, ADDRESS, WEBSITE, TELEPHONE_1, TELEPHONE_2, TELEPHONE_3]
    cursor.execute(f'INSERT INTO {TABLE_NAME} VALUES (?,?,?,?,?,?,?,?,?,?)', data)

    # Commit your changes in the database
    conn.commit()
    print("Records inserted........")

    # Closing the connection
    conn.close()


obj = {
    "Category Info": "hello>world",
    "Page Link": "www.google.com",
    "Name": "Shop name",
    "Image Link": "www.imagelink.com",
    "Location": "Pakistan",
    "Address": "My Address is this",
    "Website": "Link to the website",
    "Telephone_1": "",
    "Telephone_2": "",
    "Telephone_3": ""
}

enter_data("example", "exampleTable", obj)