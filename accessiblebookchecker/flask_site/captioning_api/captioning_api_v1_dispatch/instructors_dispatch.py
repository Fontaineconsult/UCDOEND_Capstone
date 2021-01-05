from captioning.captioning_database.backend_functionality.captioning_api_v1_functions import QueryEmployeesTable
from flask_site.captioning_api.captioning_api_v1_dispatch.captioning_api_v1_errors import courses_errors as api_error


def dispatch_instructor_get(query_params):

    query_params = query_params.to_dict()

    allowed_queries = ['semester', 'instructor_id']

    query_check = [False for x in query_params if x not in allowed_queries]

    if False not in query_check:

        instructor_query = QueryEmployeesTable(query_params)
        instructor_query.run()
        return instructor_query.returned

    else:
        return api_error.InvalidParams("Only Instructor_ID and Semester")




def dispatch_instructor_post(data):
    pass






def build_instructors_dict(instructor_query):

    dict_to_return = {}

    for instructor_dict in instructor_query[0]:

        dict_to_return[instructor_dict['instructor_id']] = instructor_dict

    return dict_to_return
