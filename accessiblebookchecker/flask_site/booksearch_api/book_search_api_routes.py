
from flask import Blueprint, request, jsonify, make_response
from booksearch.book_searcher import BookSearch
from booksearch.request_dispatch import RequestDispatch


booksearch_api_routes = Blueprint('booksearch_api', __name__)



@booksearch_api_routes.route('/getdata')
def get_data():

    isbn = request.args.get('q')
    booksearch = BookSearch(isbn)
    search = booksearch.search()
    return jsonify(search)

@booksearch_api_routes.route('/textbook-json')
def query_textbook():


    isbn = request.args.get('isbn')
    course = request.args.get('course')
    accessible_check = request.args.get("check")


    if isbn or course:
        if isbn:
            if accessible_check == 'true':
                print('ACCESSIBLE CHECK', isbn)
                return jsonify(RequestDispatch(isbn, 'isbn').accessible_check())
            else:
                print('ISBNTRUE')
                return jsonify(RequestDispatch(isbn, 'isbn').build_textbook_response_object())

        if course:
            print('COURSETRUE')
            return jsonify(RequestDispatch(course, 'course').build_textbook_response_object())
    else:
        return make_response(jsonify("Something isn't right. Please check your query"), 400)
