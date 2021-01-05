import requests
import time
import openpyxl
import json

workbook = openpyxl.load_workbook('Spring 2020 E-Book List.xlsx') # make sure this file is in the same folder as the .py file
worksheet = workbook.worksheets[0]

isbn_list = []

for cell in worksheet['F']: # get all the ISBN Values
    isbn_list.append(cell.value)

print("All the ISBNs", isbn_list)

for isbn in list(set(isbn_list)):


    request_string ='https://amp.sfsu.edu/api/booksearch/getdata?q={}'.format(isbn) # Check the server for availability

    time.sleep(1) # Wait a second to avoid overworking the servers
    book_request = requests.get(request_string, verify=False)
    status = json.loads(book_request.content)


    availability = status['aimhub']['available'] or status['atn']['available'] or status['bookshare']['available'] # returns True or False if available

    print(isbn, status, book_request.status_code, availability)


    for row in worksheet:
        if row[5].value == isbn:
            row[22].value = str(availability) # column index to insert availablilty

            print(row[5].value, isbn)


workbook.save('Spring 2020 E-Book List.xlsx')
print("All Done")