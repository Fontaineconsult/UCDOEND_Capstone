
from booksearch.local_holdings import get_book



class LocalHoldingSearch:

    def __init__(self, isbn):
        self.isbn = isbn
        self.available = None

        self.search()

    def search(self):

        getbook = get_book(self.isbn)
        if getbook:
            self.available = True
        else:
            self.available = False
