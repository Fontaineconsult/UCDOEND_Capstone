from captioning.captioning_database.backend_functionality.captioning_api_v1_functions import AddCampusOrganization, QueryCampusOrganizationTable
from flask_site.captioning_api.captioning_api_v1_dispatch.captioning_api_v1_errors import courses_errors as api_error



def dispatch_campus_org_get(query_params):

    query_params = query_params.to_dict()

    allowed_queries = ['id', 'url']

    query_check = [False for x in query_params if x not in allowed_queries]

    if False not in query_check:

        media_query = QueryCampusOrganizationTable(query_params)
        media_query.run()
        return media_query.returned


    else:
        return api_error.InvalidParams("Only ID and URL")


def dispatch_campus_org_put(data):


    allowed_columns = [
        'employee_id',
        'campus_org_id'

    ]

    if list(data.keys()).sort() == allowed_columns.sort():

        add_record = AddCampusOrganization(data)
        add_record.run()

        return add_record.returned
    else:
        return api_error.InvalidParams("Columns included can't be written to")

