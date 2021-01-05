from captioning.captioning_database.backend_functionality.captioning_api_v1_functions import QueryStudentsTable

from flask_site.captioning_api.captioning_api_v1_dispatch.captioning_api_v1_errors import courses_errors as api_error


def dispatch_student_get(query_params):

    query_params = query_params.to_dict()

    allowed_queries = ['student_id', 'captioning_active']

    query_check = [False for x in query_params if x not in allowed_queries]

    if False not in query_check:

        student_query = QueryStudentsTable(query_params)
        student_query.run()
        print(student_query.returned)
        return student_query.returned

    else:
        return api_error.InvalidParams("Only Student and captioning_active")




def dispatch_student_post(data):
    pass



