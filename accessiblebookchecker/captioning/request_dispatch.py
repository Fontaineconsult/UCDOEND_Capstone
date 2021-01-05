import sys
sys.path.append("/var/www/books/books/captioning/")
sys.path.append("/var/www/books/books/captioning")
from datetime import datetime

import captioning.captioning_database.backend_functionality.ilearn_scraped_db_functions as cdb
import json

from captioning.utilities.v1.cap_info_router import get_mainstream_video_info
import time


def master_cap_dispatch(post_data):

    approved_methods = ['database', 'service']

    if post_data['method'] not in approved_methods:
        return {"succeeded": False, "error_message": "method not available", "response_code": 400}
    else:
        if post_data['method'] == 'database':

            cap_database = cap_database_router(post_data)

            print(cap_database)

            if not cap_database["succeeded"]:
                return cap_database
            else:
                return cap_database

        if post_data['method'] == 'service':

            cap_service = cap_service_router(post_data)


            return {"succeeded": True, "response_object": None}


def cap_service_router(post_data):

    allowed_services = ["id_video_title"]


def cap_database_router(post_data):

    allowed_services = ["get_courses_videos",
                        "save_course_videos",
                        "get_all_videos",
                        "update_cap_status",
                        "refresh_cap_status",
                        "update_show_date"]

    if post_data["option"] not in allowed_services:

        return {"succeeded": False, "error_message": "database option not available", "response_code": 400}

    else:

        if post_data["option"] == "get_courses_videos":

            get_videos = get_courses_videos(post_data['params']['semester'],
                                            post_data['params']['course_id'])


            if get_videos:

                get_videos = get_videos.make_dict()
                return {"succeeded": True, "response_object": get_videos}
            else:
                return {"succeeded": False, "error_message": "No Videos Found", "response_code": 200}


        if post_data["option"] == "save_course_videos":


            save_course_videos(post_data['params']['video_content'])

            pass

        if post_data["option"] == "get_all_videos":

            get_videos = get_all_videos(post_data['params']['semester'])


            if get_videos:

                dict_vids = [course.make_dict() for course in get_videos]

                return {"succeeded": True, "response_object": dict_vids}

            else:
                return {"succeeded": False, "error_message": "No Videos Found", "response_code": 200}

        if post_data["option"] == "update_cap_status":
            pass
        if post_data["option"] == "refresh_cap_status":
            pass
        if post_data["option"] == "update_show_date":
            pass








def get_courses_videos(semester, course_id):

    videos = cdb.get_videos_by_course_id(semester, course_id)

    if videos:
        return videos
    else:
        return False



def id_video_title(link):
    try:
        video_title = get_mainstream_video_info(link)
        return video_title
    except IndexError:
        pass





def save_course_videos(data):

    captioning_data = json.loads(data.decode('utf-8'))

    course_id = captioning_data['course_id']
    course_name = captioning_data['course_name']
    semester = captioning_data['semester']

    cdb.check_or_commit_course(course_id,
                               course_name,
                               semester)

    for content in captioning_data['content']:
        print(len(content['section_content']))
        print(content)
        if len(content['section_content']) > 0:
            for video in content['section_content']:

                video_title = video['title']
                time.sleep(0.01)

                video_info = get_mainstream_video_info(video['link'])

                if video_info:
                    caption_state = video_info['cap-state']

                    if video_title is None:
                        searched_video_title = video_info['api-provided-title']
                        if searched_video_title:
                            video_title = searched_video_title
                else:
                    caption_state = None

                video_link = video['link']
                scan_date = video['scan_date']

                cdb.commit_ilearn_video_content(video_title, video_link, course_id, scan_date, caption_state)
        else:
            print("no data to manage")


def get_all_videos(semester):

    semester = semester.replace("_", " ")

    all_course_videos = cdb.get_all_videos_from_db_by_course(semester)

    if all_course_videos:
        return all_course_videos
    else:
        return False


def update_cap_status(link):

    request_url = json.loads(link.decode('utf-8'))['link']
    request_status = json.loads(link.decode('utf-8'))['status']
    print("Request in", request_url, request_status)
    if cdb.write_update_caption_status(request_url, request_status):
        return True
    else:
        return False

def update_submit_status(data):
    request_url = json.loads(data.decode('utf-8'))['link']
    status = json.loads(data.decode('utf-8'))['status']
    status = not status
    date = datetime.utcnow()

    print(request_url, status, datetime.utcnow())

    if cdb.write_submit_status(request_url, status, date):
        return status, date
    else:
        return False




def refresh_cap_status(video_url):

    caption_check = get_mainstream_video_info(video_url)
    if caption_check:

        if cdb.write_update_caption_status(video_url, caption_check['cap-state']):
            print("saved to DB")
        else:
            print("didn't save to DB")


        if caption_check['cap-state'] is True:
            return True
        elif caption_check['cap-state'] is False:
            return False
        else:
            return None
    else:
        return None


def update_show_date(payload):
    request_url = json.loads(payload.decode('utf-8'))['link']
    show_date = json.loads(payload.decode('utf-8'))['show_date']
    course_id = str(json.loads(payload.decode('utf-8'))['course_id'])

    if cdb.write_update_showdate(request_url, show_date, course_id):
        return True
    else:
        return False


def update_ast_status(payload):
    print(payload)





