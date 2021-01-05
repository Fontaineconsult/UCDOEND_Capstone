from captioning.captioning_database.backend_functionality.captioning_api_v1_functions import QueryMediaTable, AddRecordToMediaTable, WriteMediaToTable
from flask_site.captioning_api.captioning_api_v1_dispatch.captioning_api_v1_errors import courses_errors as api_error
import captioning.captioning_database.backend_functionality.captioning_api_v1_functions as cap_functions

def dispatch_media_get(query_params):

    query_params = query_params.to_dict()

    allowed_queries = ['id', 'url']

    query_check = [False for x in query_params if x not in allowed_queries]

    if False not in query_check:

        media_query = QueryMediaTable(query_params)
        media_query.run()
        return media_query.returned


    else:
        return api_error.InvalidParams("Only ID and URL")


def dispatch_media_post(post_data):


    writable_columns = ["media_type",
                        "title",
                        "length",
                        "source_url",
                        "captioned_url",
                        "at_catalog_number",
                        "comments"]


    if post_data['column'] in writable_columns:


        media_query = WriteMediaToTable(post_data)
        media_query.run()
        return media_query.returned



    else:
        return api_error.InvalidParams("Columns included can't be written to")





def dispatch_media_put(data):


    allowed_columns = [
        "media_type",
        "title",
        "length",
        "source_url",
        "captioned_url",
        "at_catalog_number",
        "comments",
        "date_added"

    ]

    if list(data.keys()).sort() == allowed_columns.sort():

        add_record = AddRecordToMediaTable(data)
        add_record.run()
        return add_record.returned
    else:
        return api_error.InvalidParams("Columns included can't be written to")

