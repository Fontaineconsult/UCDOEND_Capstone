from booksearch.book_searcher import BookSearch
from booksearch.textbook_querier import query_textbooks_isbn, query_course_name
from booksearch.worldcat_api import WordcatHolding
from booksearch.googlebooks_api import GoogleBooksHolding



class RequestDispatch:

    def __init__(self, search_string, search_type):
        self.search_string = search_string
        self.search_type = search_type
        self.textbook_list = []
        self.course_text = None
        self.worldcat_object = None
        self.google_books_object = None


    def query_textbooks(self):
        textbook_query = query_textbooks_isbn(self.search_string)
        if textbook_query:
            for textbook in textbook_query:
                if textbook:
                    self.textbook_list.append(textbook)
            self.course_text = True
        else:
            self.course_text = False


    def query_courses(self):
        course_query = query_course_name(self.search_string)
        if course_query:
            for course in course_query:
                if course:
                    self.textbook_list.append(course)
            self.course_text = True
        else:
            self.course_text = False


    def accessible_check(self):
        accessible_check = BookSearch(self.search_string).search()
        print(accessible_check)
        response_object = {'isbn': str(self.search_string),
                           "status": accessible_check}
        return response_object


    def world_cat_verify(self):
        worldCat_request = WordcatHolding(self.search_string)
        print("Checking WorldCat")
        if worldCat_request.available:
            self.worldcat_object = {'title': worldCat_request.title,
                                    'author': worldCat_request.author,
                                    'validISBN': worldCat_request.available}
        else:
            self.worldcat_object = {'title': None,
                                    'author': None,
                                    'validISBN': worldCat_request.available}
        print("WordCat Object", self.worldcat_object)


    def google_books_verify(self):
        google_books_request = GoogleBooksHolding(self.search_string)
        print("Checking GoogleBooks")
        if google_books_request.available:
            self.google_books_object = {"title": google_books_request.title,
                                        "author": google_books_request.author,
                                        "validISBN": google_books_request.available}
        else:
            self.google_books_object = {"title": None,
                                        "author": None,
                                        "validISBN": google_books_request.available}



    def build_textbook_response_object(self):
        response_object_list = []

        if self.search_type == 'isbn':
            self.query_textbooks()

            if self.course_text == True:
                for textbook in self.textbook_list:
                    response_object_list.append({'isbn': textbook.isbn,
                                                 "title": textbook.title,
                                                 "course": textbook.course_name.replace("_", " "),
                                                 "validIsbn": True,
                                                 "accessible": None})
            else:
                if len(self.search_string) < 13:
                    response_object_list.append({'isbn': self.search_string,
                                                 'title': None,
                                                 'course': None,
                                                 'validIsbn': None,
                                                 'accessible': None})
                else:

                    self.google_books_verify()
                    if self.google_books_object['validISBN']:
                        print(self.google_books_object['validISBN'])
                        response_object_list.append({'isbn': self.search_string,
                                                     'title': self.google_books_object['title'],
                                                     'author': self.google_books_object['author'],
                                                     'validIsbn': self.google_books_object['validISBN']})

                    else:
                        self.world_cat_verify()
                        print(self.worldcat_object)
                        response_object_list.append({'isbn': self.search_string,
                                                     'title': self.worldcat_object['title'],
                                                     'author': self.worldcat_object['author'],
                                                     'validIsbn': self.worldcat_object['validISBN']})

        if self.search_type == 'course':
            self.query_courses()
            for textbook in self.textbook_list:
                response_object_list.append({
                    'isbn': textbook.isbn,
                    'title': textbook.title,
                    'course': textbook.course_name.replace("_", " "),
                    "validIsbn": True,
                    'instructor': textbook.instructor
                })

        return response_object_list


