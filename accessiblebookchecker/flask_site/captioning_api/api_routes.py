
from flask import Blueprint, request, jsonify

from captioning.request_dispatch import save_course_videos, \
    id_video_title, \
    update_cap_status, refresh_cap_status, \
    update_show_date, master_cap_dispatch, update_submit_status
import json
from captioning.request_dispatch import update_ast_status



captioning_api_routes = Blueprint('captioning_api', __name__)





@captioning_api_routes.route('/master_cap_router', methods=['POST'])
def master_router():

    if request.method == 'POST':
        service_request = master_cap_dispatch(json.loads(request.data.decode('utf-8')))

        if not service_request["succeeded"]:
            return service_request["error_message"], service_request["response_code"]

        else:
            return jsonify({"data": service_request["response_object"]}), 200


    else:
        ##! add allow header
        return "Route Only Accepts POST", 405


@captioning_api_routes.route('/ilearn-cap', methods=['POST'])
def upload_video_info():
    if request.method == 'POST':
        save_course_videos(request.data)
        return 'YYOYOYOY'


@captioning_api_routes.route('/get_video_info', methods=['GET'])
def get_video_info():
    if request.method == 'GET':
        video_link = request.args.get('video_url')
        print(video_link)
        video_title = id_video_title(video_link)
        response = {'video-title': video_title}
        return jsonify(response)

@captioning_api_routes.route('/update-cap-status', methods=['POST', 'PUT'])
def update_cap_status_func():
    if request.method == 'POST':
        update_cap_status(request.data)
        if update_cap_status:
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
        else:
            return json.dumps({'success':False}), 200, {'ContentType':'application/json'}


@captioning_api_routes.route('/refresh-cap-status', methods=['GET'])
def refresh_cap_status_func():
    if request.method == 'GET':

        request_url = request.args.get('url')
        print(request_url)
        updated_status = refresh_cap_status(request_url)

        if updated_status is True:
            return json.dumps({'cap-state': True}), 200, {'ContentType':'application/json'}
        elif updated_status is False:
            return json.dumps({'cap-state': False}), 200, {'ContentType':'application/json'}
        elif updated_status is None:
            return json.dumps({'cap-state': None}), 200, {'ContentType':'application/json'}
    else:
        return "Bad Request", 400


@captioning_api_routes.route('/update-show-date', methods=['POST'])
def update_show_date_func():
    print(request.data)
    if request.method == 'POST':
        update_show_date(request.data)
        if update_show_date:
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
        else:
            return json.dumps({'success':False}), 200, {'ContentType':'application/json'}


@captioning_api_routes.route('/ast-cap-result-callback', methods=['POST'])
def ast_result():
    if request.method == 'POST':
        print("I GOT HIT, results")
        update_ast_status(request.data)
        return "Good", 200


@captioning_api_routes.route('/ast-cap-status-callback', methods=['POST'])
def ast_status():
    if request.method == 'POST':
        print("I GOT HIT, status")
        update_ast_status(request.data)
        return "Good", 200

@captioning_api_routes.route('/update-submit-status', methods=['POST'])
def update_submit_status_endpoint():

    if request.method == 'POST':
        update_submit = update_submit_status(request.data)
        if update_submit:



            return json.dumps({'success':True, 'status': update_submit[0], 'date': update_submit[1].isoformat()}), 200, {'ContentType':'application/json'}
        else:
            return json.dumps({'success':False}), 200, {'ContentType':'application/json'}

