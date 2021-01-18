
from flask import Blueprint, render_template, request, abort
# from booksearch.book_searcher import BookSearch
from flask_login import login_required
from captioning.request_dispatch import get_courses_videos, get_all_videos


page_routes = Blueprint('pages',
                        __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/pages/static',)


@page_routes.route("/")
def main():
    return "This is the SF State Accessible Media Program's application page GREEEEEEENNNNNN"


# @page_routes.route('/booksearcher', methods=['GET', 'POST'])
# def hello_world():
#     if request.method == "POST":
#         isbn = request.form['isbn']
#         search = BookSearch(isbn)
#         #search.search()
#
#     return render_template('booksearcher.html')




@page_routes.route('/captioning/job-manager', methods=["GET"])
@page_routes.route('/captioning/add-job', methods=["GET"])
@page_routes.route('/captioning/ilearn-scraper/active-courses', methods=["GET"])
@page_routes.route('/captioning/ilearn-scraper/inactive-courses', methods=["GET"])
@page_routes.route('/captioning/users', methods=["GET"])
@login_required
def captioning_route():
    return render_template("index.html")








@page_routes.route('/videos/<semester>/<int:course_id>', methods=['GET'])
def load_video_list_page(semester, course_id):
    single_course_videos = get_courses_videos(semester, course_id)
    print(single_course_videos)
    if single_course_videos:
        return render_template('course_list.html', course_video_list=single_course_videos)
    else:
        abort(404)

@page_routes.route('/videos/<semester>/all_course_videos', methods=['GET'])
def load_all_course_videos(semester):
    all_course_videos = get_all_videos(semester)
    if all_course_videos:



        print(all_course_videos)
        return render_template("course_list.html", course_video_list=all_course_videos)
    else:
        return "Nothing to load"


@page_routes.route('/saml-test', methods=['GET'])
def saml_test():
    return render_template("saml_test_page.html")