from flask import Blueprint, request, make_response
from flask_site.captioning_api.captioning_api_v2_dispatch.request_dispatch import QueryDispatch,\
    AddDispatch,\
    UpdateDispatch
import json
from captioning.ast.ast_methods import pre_create_ast_job, submit_ast_job_update_job, upload_media_to_ast
from flask_login import login_required
from captioning.amara.amara_tools import check_record_for_amara_resource

captioning_api_routes_v2 = Blueprint('captioning_api_v2', __name__)



@captioning_api_routes_v2.route("/permission",  methods=['GET'])
@login_required
def permission_endpoint():

    if request.method == 'GET':
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response



@captioning_api_routes_v2.route("/students", methods=['GET', 'POST'])
@login_required
def students_endpoint():

    if request.method == 'GET':
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response



@captioning_api_routes_v2.route("/employees", methods=['GET', 'POST'])
@login_required
def employees_endpoint():

    if request.method == 'GET':
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response

    if request.method == 'POST':
        dispatcher = AddDispatch(json.loads(request.data.decode('utf-8')), request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response




@captioning_api_routes_v2.route("/captioning-requests",  methods=['GET', 'POST'])
@login_required
def captioning_requests_endpoint():
    if request.method == 'GET':
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response


    if request.method == 'POST':
        dispatcher = AddDispatch(json.loads(request.data.decode('utf-8')), request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response




@captioning_api_routes_v2.route("/courses",  methods=['GET', 'PUT'])
@login_required
def courses_endpoint():
    if request.method == 'GET':
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response

    if request.method == 'PUT':

        dispatcher = UpdateDispatch(json.loads(request.data.decode('utf-8')), request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response


@captioning_api_routes_v2.route("/video-jobs", methods=['GET', 'POST', 'PUT'])
@login_required
def videos_endpoint():
    if request.method == 'GET':
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        response.headers['Access-Control-Expose-Headers'] = "Content-Disposition"
        return response

    if request.method == 'POST':

        dispatcher = AddDispatch(json.loads(request.data.decode('utf-8')), request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response

    if request.method == 'PUT':

        dispatcher = UpdateDispatch(json.loads(request.data.decode('utf-8')), request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response





@captioning_api_routes_v2.route("/ilearn-videos", methods=["GET", "PUT"])
@login_required
def ilearn_endpoint():

    if request.method == "GET":
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response

    if request.method == "PUT":

        dispatcher = UpdateDispatch(json.loads(request.data.decode('utf-8')), request.args,  request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response




@captioning_api_routes_v2.route("/media", methods=['GET', 'POST', 'PUT'])
@login_required
def media_endpoint():

    if request.method == 'GET':
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()

        return response

    if request.method == "POST":
        dispatcher = AddDispatch(json.loads(request.data.decode('utf-8')), request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()

        ## Add Amara Resource
        if 'source_url' in request.data.decode('utf-8'):
            check_record_for_amara_resource(json.loads(request.data.decode('utf-8'))['source_url'])

        return response

    if request.method == "PUT":
        dispatcher = UpdateDispatch(json.loads(request.data.decode('utf-8')), request.args,  request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response


@captioning_api_routes_v2.route("/requesters", methods=['GET'])
@login_required
def verify_requester_endpoint():

    if request.method == 'GET':
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response


@captioning_api_routes_v2.route("/campus-orgs", methods=['GET'])
@login_required
def campus_orgs_endpoint():

    if request.method == 'GET':
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response


@captioning_api_routes_v2.route("/campus-org-assignment", methods=['GET', 'POST'])
@login_required
def org_assignment_endpoint():

    if request.method == 'GET':
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response

    if request.method == 'POST':
        dispatcher = AddDispatch(json.loads(request.data.decode('utf-8')), request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response



@captioning_api_routes_v2.route("/media-objects", methods=['POST', 'GET'])
@login_required
def media_objects_endpoint():
    if request.method == 'GET':
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response



    if request.method == 'POST':
        dispatcher = AddDispatch(json.loads(request.data.decode('utf-8')), request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response


@captioning_api_routes_v2.route("/ast-jobs", methods=['POST', 'PUT'])
@login_required
def ast_jobs_endpoint():
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))

        pre_created_ast_job = pre_create_ast_job(data["jobid"], data['file_id'], data['ast_notes'], data['ast_rush'],)
        dispatcher = AddDispatch(pre_created_ast_job['data_to_commit'], request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response

    if request.method == 'PUT':
        data = json.loads(request.data.decode('utf-8'))
        new_ast_job_id = submit_ast_job_update_job( int(data['ast-job-id']), )
        if new_ast_job_id:

            upload_attempt = upload_media_to_ast(new_ast_job_id)
            if upload_attempt:
                update_ast_init_stat = {"id": (int(data['ast-job-id'])),
                                        "column": "captioning_status",
                                        "value": "submitted" }
                dispatcher = UpdateDispatch(update_ast_init_stat, request.args, request.path)
                dispatcher.dispatch()

                update_ast_job_id = {"id": (int(data['ast-job-id'])), "column": "ast_id", "value": new_ast_job_id }
                dispatcher = UpdateDispatch(update_ast_job_id, request.args, request.path)
                dispatcher.dispatch()
                response = dispatcher.response_object()
                return response
            else:
                return make_response("File Upload Failed", 401)

        else:
            return make_response("AST Authentication failed", 401)


@captioning_api_routes_v2.route("/amara", methods=['GET', 'POST'])
@login_required
def amara_endpoint():
    if request.method == 'GET':
        dispatcher = QueryDispatch(request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response

    if request.method == 'POST':
        dispatcher = AddDispatch(json.loads(request.data.decode('utf-8')), request.args, request.path)
        dispatcher.dispatch()
        response = dispatcher.response_object()
        return response


