from captioning.captioning_database.backend_functionality.captioning_api_v1_functions import QueryPermission
from flask_site.captioning_api.captioning_api_v1_dispatch.captioning_api_v1_errors import courses_errors as api_error



def dispatch_permission_get(query_params):

    query_params = query_params.to_dict()

    allowed_queries = ['id']

    query_check = [False for x in query_params if x not in allowed_queries]

    if False not in query_check:

        permission_query = QueryPermission(query_params)
        permission_query.run()
        return permission_query.returned

    else:
        return api_error.InvalidParams("Only ID")

