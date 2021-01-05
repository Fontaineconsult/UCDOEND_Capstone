from booksearch.aimhub_api import AimHubHolding
from booksearch.atn_api import AtnHolding
from booksearch.bookshare_api import BookShareHolding
from booksearch.local_holding_search import LocalHoldingSearch


class BookSearch:

    def __init__(self, isbn):
        self.isbn = isbn
        self.atn_available = None
        self.aimhub_available = None

    def search_atn(self):
        atn_search_object = AtnHolding(self.isbn)
        return atn_search_object

    def search_aimhub(self):
        aimhub_search_object = AimHubHolding(self.isbn)
        return aimhub_search_object

    def search_local(self):
        local_search_object = LocalHoldingSearch(self.isbn)
        return local_search_object

    def search_bookshare(self):
        bookshare_search_object = BookShareHolding(self.isbn)
        return bookshare_search_object


    def verify_isbn(self):
        pass

    def search(self):
        atn_search = self.search_atn()
        bookshare_search = self.search_bookshare()
        aimhub_search = self.search_aimhub().available
        local_search = self.search_local().available

        return_object = {'atn': {'available': atn_search.available, 'id': atn_search.itemId},
                         'aimhub': {'available': aimhub_search},
                         'local': {'available': local_search},
                         'bookshare': {'available': bookshare_search.available, 'id': bookshare_search.itemId}}
        return return_object


