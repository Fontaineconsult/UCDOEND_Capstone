import requests, time

##! Add request from booksahre if unavailable.

class BookShareHolding:

    def __init__(self, isbn):
        self.isbn = isbn
        self.title = None
        self.author = None
        self.itemId = None
        self.available = None
        self.response_code = None
        self.bookshare_status_code = None
        self.construct_holding()

    def bookshare_request(self):
        isbn = self.isbn

        payload = {'api_key': 'xxx'}

        bookshare_request = requests.get("https://api.bookshare.org/book/isbn/" + isbn + "/format/json?",
                                         params=payload)

        if bookshare_request.status_code == 200:
            return bookshare_request
        elif bookshare_request.status_code == 403:
            time.sleep(1)
            bookshare_request = requests.get("https://api.bookshare.org/book/isbn/" + isbn + "/format/json?",
                         params=payload)
            return bookshare_request

    def construct_holding(self):
        request = self.bookshare_request()
        request_json = request.json()

        if request.status_code == requests.codes.ok:
            self.response_code = request.status_code
            if 'statusCode' in request_json['bookshare']:
                self.bookshare_status_code = request_json['bookshare']['statusCode']

                if request_json['bookshare']['statusCode'] == '85' or request_json['bookshare']['statusCode'] == '0':
                    self.available = False

            else:
                self.title = request_json['bookshare']['book']['metadata']['title']
                self.author = request_json['bookshare']['book']['metadata']['author']
                self.itemId = request_json['bookshare']['book']['metadata']['contentId']
                self.available = True
        else:
            self.available = False
            self.response_code = request.status_code
