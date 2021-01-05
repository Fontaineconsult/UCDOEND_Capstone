import requests
from xml.dom import minidom

class WordcatHolding:

    def __init__(self, isbn):
        self.isbn = isbn
        self.title = None
        self.author = None
        self.available = None
        self.response_code = None
        self.worldcat_title_search()


    def worldcat_title_search(self):
        payload = {'wskey': '7EknBwgDCLs1YSoN5X7wNsUnCJxIWtkakXSUr6g8cgIQzMHwHE6uXqNp6RmKJMNluMi8bFLnPRrSCXWE', 'q': self.isbn}
        worldcat_request = requests.get('http://www.worldcat.org/webservices/catalog/search/worldcat/opensearch?', params=payload)

        if worldcat_request.status_code == requests.codes.ok:
            print(worldcat_request.headers)
            print(worldcat_request.content)
            self.response_code = worldcat_request.status_code

            if worldcat_request.headers['content-length'] == '352':  # strange way to test for no results found
                self.available = False
            else:
                self.available = True

                self.build_xml_dom(worldcat_request.content)
        else:
            print("World Cat Request Error", worldcat_request.status_code)
            self.available = False
            self.response_code = worldcat_request.status_code

    def build_xml_dom(self, request_content):
        request_dom = minidom.parseString(request_content)



        wordlcat_response = request_dom.getElementsByTagName('entry')

        ##! set isbn to worldcat response isbn
        #self.isbn = wordlcat_response[0].getElementsByTagName('isbn')[0].firstChild.nodeValue
        self.title = wordlcat_response[0].getElementsByTagName('title')[0].firstChild.nodeValue
        self.author = wordlcat_response[0].getElementsByTagName('author')[0].getElementsByTagName('name')[0].firstChild.nodeValue




