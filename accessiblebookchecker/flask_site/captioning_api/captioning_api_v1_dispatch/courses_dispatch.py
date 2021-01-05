import captioning.captioning_database.backend_functionality.captioning_api_v1_functions as cap_functions
from flask_site.captioning_api.captioning_api_v1_dispatch.captioning_api_v1_errors import courses_errors as api_error


def dispatch_courses_query():

    courses_query = cap_functions.QueryCoursesTable()
    courses_query.run()
    return courses_query.returned

def dispatch_courses_get(query_params):

    query_params = query_params.to_dict()

    allowed_queries = ["instructor_id", "course_gen_id", "semester"]

    query_check = [False for x in query_params if x not in allowed_queries]

    if 'instructor_id' in query_params:
        query_params['course_instructor_id'] = query_params['instructor_id']
        del query_params['instructor_id']

    if False not in query_check:

        courses_query = cap_functions.QueryCoursesTable(query_params)
        courses_query.run()
        return courses_query.returned
    else:
        return api_error.InvalidParams("Allowed queries are: Instructor_ID,  Course_Gen_ID", "Semester")



def dispatch_courses_post(post_data):



    print("POST", post_data)

    writable_columns = ["course_online",
                        "no_students_enrolled",
                        "contact_email_sent",
                        "no_student_enrolled_email_sent",
                        "course_comments",
                        "activate_ilearn_video_notification_sent",
                        "instructor_requests_captioning"]


    if post_data['column'] in writable_columns:


        courses_write = cap_functions.WriteCourseToTable(post_data)
        courses_write.run()
        return courses_write.returned

    else:

        return api_error.InvalidParams("Can't write to that column")






def build_courses_dict(courses_query):

    dict_to_return = {}

    for course_dict in courses_query[0]:

        dict_to_return[course_dict['course_gen_id']] = course_dict

    return dict_to_return
