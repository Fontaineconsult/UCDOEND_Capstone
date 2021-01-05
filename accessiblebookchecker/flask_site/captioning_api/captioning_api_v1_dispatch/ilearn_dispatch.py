from captioning.captioning_database.backend_functionality.captioning_api_v1_functions import QueryiLearnVideosTable, WriteIlearnVideoToTable
from flask_site.captioning_api.captioning_api_v1_dispatch.captioning_api_v1_errors import courses_errors as api_error

def dispatch_ilearn_query_get(query_params):

    query_params = query_params.to_dict()

    allowed_queries = ["course_gen_id", "semester", "student_id", "instructor_id"]

    query_check = [False for x in query_params if x not in allowed_queries]


    if False not in query_check:

        query = QueryiLearnVideosTable(query_params)
        query.run()
        return query.returned


    else:
        return api_error.InvalidParams("Allowed queries are: Course_Gen_ID, semester, student_id, instructor_id")




def dispatch_ilearn_query_post(post_data):



    writable_columns = ["id",
                        "submitted_for_processing",
                        "indicated_due_date",
                        "captioned"]


    if post_data['column'] in writable_columns:


        media_query = WriteIlearnVideoToTable(post_data)
        media_query.run()
        return media_query.returned



    else:
        return api_error.InvalidParams("Columns included can't be written to")
