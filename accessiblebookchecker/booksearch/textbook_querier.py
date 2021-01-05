from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker, exc
from booksearch.local_holdings import textbook_query,  coure_name_query



def query_textbooks_isbn(isbn):
    if isbn is None:
        return None
    else:

        ##! Filter out non standard ISBN entries

        textbookquery = textbook_query(isbn)
        if textbook_query:
            if textbookquery.count() > 0:
                return textbookquery
            else:
                return False
        else:
            return False



def query_course_name(course_name):
    if course_name is None:
        return None
    else:

        print("STRING", course_name)

        course_query = coure_name_query(course_name)
        if course_query:
            if course_query.count() > 0:
                return course_query
            else:
                return False
        else:
            return False
