import requests
import json


google_books_api = "https://www.googleapis.com/books/v1/volumes?"
search_query = "{}q=isbn{}".format(google_books_api, "9780060777579")



class GoogleBooksHolding:

    def __init__(self, isbn):

        self.isbn = isbn
        self.title = None
        self.author = None
        self.available = None
        self.response_code = None
        self.google_books_api_search()


    def google_books_api_search(self):



        google_books_api = "https://www.googleapis.com/books/v1/volumes?"
        search_query = "{}q=isbn{}".format(google_books_api, self.isbn)
        google_books_api_request = requests.get(search_query)
        api_response_content = json.loads(google_books_api_request.content.decode('utf-8'))

        if google_books_api_request.status_code == requests.codes.ok:



            self.response_code = google_books_api_request.status_code

            if api_response_content['totalItems'] == 0:
                self.available = False
            else:
                self.available = True
                self.title = api_response_content['items'][0]['volumeInfo']['title']
                try:
                    self.author = api_response_content['items'][0]['volumeInfo']['authors'][0]
                except KeyError:
                    self.author = "No Author Provided"
                print(api_response_content['items'][0]['volumeInfo']['title'])





