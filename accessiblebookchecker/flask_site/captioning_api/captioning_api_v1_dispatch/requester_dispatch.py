from flask_site.captioning_api.captioning_api_v1_dispatch.captioning_api_v1_errors import courses_errors as api_error
from captioning.captioning_database.backend_functionality.captioning_api_v1_functions import QueryRequesterTable

def dispatch_requester_verify_get(query_params):

    query_params = query_params.to_dict()

    allowed_queries = ['employee_id', 'student_id']

    query_check = [False for x in query_params if x not in allowed_queries]

    if False not in query_check:

        requester_check = QueryRequesterTable(query_params)
        requester_check.run()

        return requester_check.returned


    else:
        return api_error.InvalidParams("course_instructor_id ,employee_id,student_id ")


