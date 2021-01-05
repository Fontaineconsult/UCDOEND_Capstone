from captioning.captioning_database.backend_functionality.captioning_api_v1_functions import AddCampusOrgAssignment
from flask_site.captioning_api.captioning_api_v1_dispatch.captioning_api_v1_errors import courses_errors as api_error


def campus_org_assignment_put(data):


    allowed_columns = [
        'employee_id',
        'campus_org_id'

    ]

    if list(data.keys()).sort() == allowed_columns.sort():

        add_record = AddCampusOrgAssignment(data)
        add_record.run()
        return add_record.returned
    else:
        return api_error.InvalidParams("Columns included can't be written to")

