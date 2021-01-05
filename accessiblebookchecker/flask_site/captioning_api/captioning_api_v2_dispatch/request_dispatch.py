from captioning.captioning_database.backend_functionality import captioning_api_v1_functions as queries
from flask_site.captioning_api.captioning_api_v2_dispatch.requests_objects import BaseRequest,\
    GetObject, UpdateObject, AddObject
import flask_site.captioning_api.captioning_api_v2_dispatch.request_errors as error
import traceback
from flask import make_response, jsonify
from flask_site.captioning_api.captioning_api_v2_dispatch.decorators import check_error
from flask_site.captioning_api.captioning_api_v2_dispatch.response_object import ContentResponse, ErrorResponse



query_routes = {
    "permission": {'query': queries.QueryPermission, 'primary_key': 'user_id'},
    "courses": {'query':  queries.QueryCoursesTable, 'primary_key': 'course_gen_id'},
    "ilearn-videos": {'query':  queries.QueryiLearnVideosTable, 'primary_key': 'id'},
    "video-jobs": {'query':  queries.QueryCapJobsTable, 'primary_key': 'id'},
    "employees": {'query':  queries.QueryEmployeesTable, 'primary_key': 'employee_id'},
    "students": {'query':  queries.QueryStudentsTable, 'primary_key': 'student_id'},
    "media": {'query':  queries.QueryMediaTable, 'primary_key': 'id'},
    "requesters": {'query':  queries.QueryRequesterTable, 'primary_key': 'id'},
    "campus-orgs": {'query':  queries.QueryCampusOrganizationTable, 'primary_key': 'id'},
    "campus-org-assignment": {'query':  queries.QueryCampusOrganizationAssignmentTable, 'primary_key': 'id'},
    "captioning-requests": {'query': queries.QueryCapRequestsTable, 'primary_key': 'employee_id'},
    "media-objects": {'query': queries.QueryMediaObjectAssignments, 'primary_key': 'id'},
    "amara": {'query': queries.QueryAmaraTable, 'primary_key': 'id'}
}


add_routes = {

    "video-jobs": {'query': queries.AddRecordToCapJobsTable,'primary_key': 'id'},
    "media": {'query': queries.AddRecordToMediaTable, 'primary_key': 'id'},
    "campus-org-assignment": {'query': queries.AddCampusOrgAssignment, 'primary_key': 'id'},
    "captioning-requests": {'query': queries.AddCaptioningRequestToTable, 'primary_key': 'employee_id'},
    "ast-jobs": {'query': queries.AddAstJobToAstJobTable, 'primary_key': 'id'},
    "amara": {'query': queries.AddAmaraResourceToTable, 'primary_key': 'id'},
    "employees": {'query': queries.AddEmployeeeToEmployeeTable, 'primary_key': "employee_id"}

}


update_routes = {
    "courses": {'query': queries.WriteCourseToTable, 'primary_key': 'course_gen_id'},
    "ilearn-videos": {'query': queries.WriteIlearnVideoToTable, 'primary_key': 'id'},
    "video-jobs": {'query': queries.WriteCapJobsToTable, 'primary_key': 'id'},
    "media": {'query': queries.WriteMediaToTable, 'primary_key': 'id'},
    "ast-jobs": {'query': queries.WriteAstJobsToTable, 'primary_key': 'id'},
    "amara": {'query': queries.WriteAmaraResourcetoTable, 'primary_key': 'id'}
}


class BaseDispatch(object):

    def __init__(self):

        self.request_object = None
        self.routes = None
        self.queryObject = None

    @check_error
    def dispatch(self):

        if self.request_object.error is not None:
            self.error_response()
            return
        self.get_query()
        print("GETTING QUERY")
        if self.request_object.error is not None:
            self.error_response()
            return
        print("EXEC QUERY")
        self.exec_query()
        if self.request_object.error is not None:
            self.error_response()
        else:
            print("PREPPING FOR RESPONSE")
            self.prep_for_response()

    @check_error
    def get_query(self):

        try:
            self.queryObject = self.routes[self.request_object.resource]['query']
            print("ZORBNS", self.queryObject)
        except KeyError:

            print("NO GO YO", self.routes)
            self.request_object.error = error.NoRouteExistsForMethod(
                                                      "Route requested doesn't exist for this request method",
                                                      405,
                                                      None,
                                                      traceback.format_exc())

    @check_error
    def exec_query(self):
        query = self.queryObject(self.request_object.payload)

        query.run()
        if query.error is not None:
            print("THERE WAS AN ERROR", query.error)
            self.request_object.error = query.error
        else:
            self.request_object.assign_request_query(query)




    @check_error
    def prep_for_response(self):

        self.request_object.serialize_query(self.routes[self.request_object.resource]['primary_key'])

        response = ContentResponse(self.request_object.serialized_query)

        self.request_object.return_payload = make_response(
                                                            (jsonify(response()),
                                                            self.request_object.response_code)
                                                            )

    def error_response(self):
        print("ERROR RESPONSE")
        response = ErrorResponse(self.request_object.error, self.request_object.payload)
        print(response)
        self.request_object.response_code = self.request_object.error.status_code
        self.request_object.return_payload = make_response(
                                                            (jsonify(response()),
                                                            self.request_object.response_code)
                                                            )


    def response_object(self):
        return self.request_object.return_payload


    def print(self):
        print(self.request_object.return_payload)


class QueryDispatch(BaseDispatch):

    def __init__(self, request_object, route):
        BaseDispatch.__init__(self)
        self.request_object = GetObject(request_object, route)
        self.routes = query_routes


class AddDispatch(BaseDispatch):

    def __init__(self, request_object, query_params, route):
        BaseDispatch.__init__(self)
        self.request_object = AddObject(request_object, query_params, route)
        self.routes = add_routes



class UpdateDispatch(BaseDispatch):

    def __init__(self, request_object, query_params, route):
        BaseDispatch.__init__(self)
        self.request_object = UpdateObject(request_object, query_params, route)
        self.routes = update_routes








