from flask_site.captioning_api.captioning_api_v1_dispatch import courses_dispatch as courses_dispatch
from flask_site.captioning_api.captioning_api_v1_dispatch import videos_dispatch as video_dispatch
from flask_site.captioning_api.captioning_api_v1_dispatch import ilearn_dispatch
from flask_site.captioning_api.captioning_api_v1_dispatch import media_dispatch as media_dispatch
import flask_site.captioning_api.captioning_api_v1_dispatch.students_dispatch as student_dispatch
import flask_site.captioning_api.captioning_api_v1_dispatch.instructors_dispatch as instructor_dispatch
import flask_site.captioning_api.captioning_api_v1_dispatch.requester_dispatch as requester_dispatch
import flask_site.captioning_api.captioning_api_v1_dispatch.campus_org_assignment_dispatch as assignment_dispatch
import flask_site.captioning_api.captioning_api_v1_dispatch.campus_org_dispatch as org_dispatch
import flask_site.captioning_api.captioning_api_v1_dispatch.permission_dispatch as permission_dispatch

from flask_site.captioning_api.serializers.captioning_media_serializer import media_serializer
from flask_site.captioning_api.serializers.employees_serializer import instructors_query_serializer
from flask_site.captioning_api.serializers.students_serializer import students_query_serializer
from flask_site.captioning_api.serializers.courses_serializer import courses_query_serializer
from flask_site.captioning_api.serializers.iLearn_videos_serializer import ilearn_video_serializer
from flask_site.captioning_api.serializers.caption_job_videos_serializer import caption_job_serializer
from flask_site.captioning_api.serializers import  requester_serializer
from flask_site.captioning_api.serializers import  campus_assignment_serializer
from flask_site.captioning_api.serializers import  campus_organization_serializer
from flask_site.captioning_api.serializers import permission_serializer

import json

from flask import make_response, jsonify

def build_data_object(query, key_value):

    dict_to_return = {}

    for each_dict in query[0]:

        dict_to_return[each_dict[key_value]] = each_dict

    return dict_to_return


class MainDispatcher:

    def __init__(self, request_type, payload):

        self.request_type = request_type
        self.payload = payload if self.request_type == "GET" else json.loads(payload.decode('utf-8'))
        self.database_query = None
        self.prepared_response = None
        self.primary_key = None
        self.serialized_output = None
        self.response_object = None


    def permission(self):
        self.primary_key = "user_id"

        if self.request_type == "GET":

            self.database_query = permission_dispatch.dispatch_permission_get(self.payload)
            self.prep_for_response(permission_serializer)
            return self.prepared_response



    def courses(self):
        self.primary_key = "course_gen_id"

        if self.request_type == "GET":

            self.database_query = courses_dispatch.dispatch_courses_get(self.payload)
            self.prep_for_response(courses_query_serializer)
            return self.prepared_response

        if self.request_type == "POST":

            self.database_query = courses_dispatch.dispatch_courses_post(self.payload)
            self.prep_for_response()
            return self.prepared_response


            pass
        if self.request_type == "PUT":
            pass

    def instructors(self):
        self.primary_key = "instructor_id"

        if self.request_type == "GET":

            self.database_query = instructor_dispatch.dispatch_instructor_get(self.payload)
            self.prep_for_response(instructors_query_serializer)
            return self.prepared_response

        if self.request_type == "POST":
            pass

        if self.request_type == "PUT":
            pass

    def media(self):
        self.primary_key = "id"
        if self.request_type == "GET":

            self.database_query = media_dispatch.dispatch_media_get(self.payload)
            self.prep_for_response(media_serializer)
            return self.prepared_response

        if self.request_type == "POST":

            self.database_query = media_dispatch.dispatch_media_post(self.payload)
            self.prep_for_response()
            return self.prepared_response

        if self.request_type == "PUT":
            self.database_query = media_dispatch.dispatch_media_put(self.payload)
            self.prep_for_response(media_serializer)
            return self.prepared_response

    def students(self):
        self.primary_key = "student_id"

        if self.request_type == "GET":

            self.database_query = student_dispatch.dispatch_student_get(self.payload)
            self.prep_for_response(students_query_serializer)
            return self.prepared_response

        if self.request_type == "POST":
            self.database_query = student_dispatch.dispatch_student_post(self.payload)
            self.prep_for_response()
        if self.request_type == "PUT":
            pass

    def video_jobs(self):
        self.primary_key = "id"

        if self.request_type == "GET":

            self.database_query = video_dispatch.dispatch_videos_query_get(self.payload)
            self.prep_for_response(caption_job_serializer)
            return self.prepared_response

        if self.request_type == "POST":

            self.database_query = video_dispatch.dispatch_videos_post(self.payload)
            self.prep_for_response()
            return self.prepared_response


        if self.request_type == "PUT":

            self.database_query = video_dispatch.dispatch_videos_put(self.payload)
            self.prep_for_response()
            return self.prepared_response

    def ilearn_videos(self):
        self.primary_key = "id"

        if self.request_type == "GET":

            def ilearn_object_prep(serialized):

                return_object = {}
                all_course_ids = list(dict.fromkeys([value['course_gen_id'] for key, value in serialized.items()]))

                for course_id in all_course_ids:

                    video_course_object = {course_id: {} }

                    for key, value in serialized.items():
                        if value['course_gen_id'] == course_id:
                            video_obj = {key : {**serialized[key]}}
                            video_course_object[course_id] = {**video_course_object[course_id], **video_obj}
                    return_object.update(video_course_object)

                return return_object

            self.database_query = ilearn_dispatch.dispatch_ilearn_query_get(self.payload)
            self.prep_for_response(ilearn_video_serializer, ilearn_object_prep)
            return self.prepared_response




        if self.request_type == "POST":

            self.database_query = ilearn_dispatch.dispatch_ilearn_query_post(self.payload)
            self.prep_for_response()
            return self.prepared_response

        if self.request_type == "PUT":
            pass

    def requester_check(self):
        self.primary_key = "id"

        if self.request_type == "GET":
            self.database_query = requester_dispatch.dispatch_requester_verify_get(self.payload)
            self.prep_for_response(requester_serializer)
            return self.prepared_response

    def campus_orgs(self):

        if self.request_type == "GET":

            self.database_query = org_dispatch.dispatch_campus_org_get(self.payload)
            self.prep_for_response(campus_organization_serializer)
            return self.prepared_response

        if self.request_type == "POST":


            pass
        if self.request_type == "PUT":
            pass


    def campus_org_assignment(self):

        if self.request_type == "PUT":

            self.database_query = assignment_dispatch.campus_org_assignment_put(self.payload)
            self.prep_for_response(campus_assignment_serializer)
            return self.prepared_response



    def prep_for_response(self, serializer=None, additional_opps=None):

        if isinstance(self.database_query, Exception):

            self.prepared_response = make_response((jsonify(self.database_query.to_dict()), self.database_query.status_code,))

        elif isinstance(self.database_query, tuple):

            if self.database_query[1] is None:
                self.prepared_response = make_response(("Success", 200,))
            else:

                self.prepared_response = make_response((jsonify({"id": self.database_query[1]}), 201))

        else:
            self.serialized_output = serializer.dump(self.database_query)

            self.response_object = build_data_object(self.serialized_output, self.primary_key)

            if additional_opps is not None:

                self.response_object = additional_opps(self.response_object)

                self.prepared_response = make_response((jsonify(self.response_object), 200,))
            else:

                self.prepared_response = make_response((jsonify(self.response_object), 200,))

