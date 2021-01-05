import requests
from xml.dom import minidom
from xml.parsers.expat import ExpatError


class AtnHolding:

    def __init__(self, isbn):
        self.isbn = isbn
        self.title = None
        self.author = None
        self.edition = None
        self.imprint = None
        self.available = None
        self.itemId = None
        self.no_results = False
        self.error = False
        self.error_type = None
        self.atn_title_search()

    def build_xml_dom(self, xml_string):

        try:
            request_dom = minidom.parseString(xml_string.content)
            print(xml_string.content)
        except ExpatError:
            request_dom = None
            self.error = True
            self.available = False

        if not self.error:

            if request_dom.getElementsByTagName('titles')[0].firstChild is not None:

                try:
                    self.title = request_dom.getElementsByTagName('title')[0].firstChild.nodeValue
                except AttributeError:
                    self.title = "Unavailable"
                try:
                    self.author = request_dom.getElementsByTagName('author')[0].firstChild.nodeValue
                except AttributeError:
                    self.author = "Unavailable"
                try:
                    self.edition = request_dom.getElementsByTagName('edition')[0].firstChild.nodeValue
                except AttributeError:
                    self.edition = "Unavailable"
                try:
                    self.imprint = request_dom.getElementsByTagName('imprint')[0].firstChild.nodeValue
                except AttributeError:
                    self.imprint = "Unavailable"
                try:
                    self.itemId = request_dom.getElementsByTagName('id')[0].firstChild.nodeValue
                except AttributeError:
                    self.imprint = "Unavailable"
                try:
                    is_available = request_dom.getElementsByTagName('title_unavailable')[0].firstChild.nodeValue

                    if is_available:
                        self.available = True
                except AttributeError:
                    self.available = False


                try:
                    is_available = request_dom.getElementsByTagName('publisher_file_unavailable')[0].firstChild.nodeValue
                    print(is_available)
                    if is_available == '1':
                        self.available = False

                    if is_available == '0':
                        self.available = True

                except AttributeError:
                    self.available = False
            else:
                self.available = False

    def atn_title_search(self):
        payload = {'username': 'amp@sfsu.edu', 'apikey': '0t86erg10ltltde8', 'isbn13': self.isbn}

        try:
            atn_request = requests.get('https://accesstext.gatech.edu/atn/titles/do_query.xml?', params=payload, timeout = 3)
            if atn_request.status_code == 200:
                self.build_xml_dom(atn_request)
            else:
                self.available = False
                self.error = True
        except requests.ConnectionError:
            self.error = True




