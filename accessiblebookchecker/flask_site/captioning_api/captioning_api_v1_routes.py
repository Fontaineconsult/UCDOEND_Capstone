from flask import Blueprint, request
from flask_site.captioning_api.captioning_api_v1_dispatch.main_dispatch_in import MainDispatcher as Dispatch
from flask_site.captioning_api.captioning_api_v2_dispatch.requests_objects import AddObject

captioning_api_routes_v1 = Blueprint('captioning_api_v1', __name__)



@captioning_api_routes_v1.route("/permission")
def instructors_endpoint():

    if request.method == 'GET':

        query = Dispatch("GET", request.args)
        response = query.permission()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response



@captioning_api_routes_v1.route("/students", methods=['GET', 'POST'])
def students_endpoint():

    if request.method == 'GET':

        query = Dispatch("GET", request.args)
        response = query.students()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response



@captioning_api_routes_v1.route("/courses",  methods=['GET', 'POST'])
def courses_endpoint():
    if request.method == 'GET':

        query = Dispatch("GET", request.args)
        response = query.courses()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    if request.method == 'POST':

        write = Dispatch("POST", request.data)
        response = write.courses()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response



@captioning_api_routes_v1.route("/video-jobs", methods=['GET', 'POST', 'PUT'])
def videos_endpoint():
    if request.method == 'GET':

        query = Dispatch('GET', request.args)
        response = query.video_jobs()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    if request.method == 'POST':


        query = Dispatch('POST', request.data)
        response = query.video_jobs()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    if request.method == 'PUT':

        query = Dispatch('PUT', request.data)
        response = query.video_jobs()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@captioning_api_routes_v1.route("/ilearn-videos", methods=["GET", "POST"])
def ilearn_endpoint():

    if request.method == "GET":

        query = Dispatch("GET", request.args)
        response = query.ilearn_videos()
        print(response)
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    if request.method == "POST":

        query = Dispatch("POST", request.data)
        response = query.ilearn_videos()
        print(response)
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response



@captioning_api_routes_v1.route("/media", methods=['GET', 'POST', 'PUT'])
def media_endpoint():

    if request.method == 'GET':

        query = Dispatch("GET", request.args)
        response = query.media()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    if request.method == "POST":

        write = Dispatch("POST", request.data)
        response = write.media()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


    if request.method == "PUT":

        request_wrapper = AddObject(request.data)
        add = Dispatch("PUT", request_wrapper)
        response = add.media()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@captioning_api_routes_v1.route("/requesters", methods=['GET'])
def verify_requester_endpoint():

    if request.method == 'GET':
        query = Dispatch("GET", request.args)
        response = query.requester_check()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@captioning_api_routes_v1.route("/campus_orgs", methods=['GET', 'POST', 'PUT'])
def campus_orgs_endpoint():

    if request.method == 'GET':
        query = Dispatch("GET", request.args)
        response = query.requester_check()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    if request.method == 'POST':
        return "Not Implemented", 200

    if request.method == 'PUT':
        return "Not Implemented", 200


@captioning_api_routes_v1.route("/campus_org_assignment", methods=['PUT'])
def org_assignment_endpoint():

    if request.method == 'PUT':
        query = Dispatch("PUT", request.args)
        response = query.requester_check()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response