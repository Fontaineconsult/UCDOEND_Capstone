import flask_site.captioning_api.serializers.campus_organization_serializer as orgs_serializer
import flask_site.captioning_api.serializers.caption_job_videos_serializer as video_jobs_serializer
import flask_site.captioning_api.serializers.captioning_media_serializer as media_serializer
import flask_site.captioning_api.serializers.courses_serializer as courses_serializer
import flask_site.captioning_api.serializers.iLearn_videos_serializer as ilearn_serializer
import flask_site.captioning_api.serializers.employees_serializer as employees_serializer
import flask_site.captioning_api.serializers.permission_serializer as permission_serializer
import flask_site.captioning_api.serializers.requester_serializer as requester_serializer
import flask_site.captioning_api.serializers.students_serializer as students_serializer
import flask_site.captioning_api.serializers.captioning_request_serializer as request_serializer
import flask_site.captioning_api.serializers.ast_job_serializer as ast_serializer
import flask_site.captioning_api.serializers.media_objects_serializer as media_objects
import flask_site.captioning_api.serializers.amara_serializer as amara_serializer

serializer_schemas = {


    "permission": permission_serializer.PermissionSchema,
    "courses": courses_serializer.CoursesSchema,
    "ilearn-videos": ilearn_serializer.iLearnVideoSchema,
    "video-jobs": video_jobs_serializer.CaptionJobSchema,
    "employees": employees_serializer.EmployeeSchema,
    "students": students_serializer.StudentsSchema,
    "media": media_serializer.CaptioningMediaSchema,
    "requesters": requester_serializer.RequesterSchema,
    "campus-orgs": orgs_serializer.CampusOrganizationSchema,
    "campus-org-assignment": orgs_serializer.CampusOrganizationAssignmentSchema,
    "captioning-requests": request_serializer.CaptioningRequestSchema,
    "ast-jobs": ast_serializer.AstJobSchema,
    "media-objects": media_objects.CaptioningMediaAssignments,
    "amara": amara_serializer.AmaraSerializerSchema
}


def build_data_object(query, key_value):

    dict_to_return = {}
    for each_dict in query[0]:
        try:
            dict_to_return[each_dict[key_value]] = each_dict
        except KeyError:
            pass
    return dict_to_return


class SerializerMixin(object):

    @staticmethod
    def serialize(resource, query, primary_key):
        serializer_schema = serializer_schemas[resource](many=True)
        results = build_data_object(serializer_schema.dump(query), primary_key)
        return results



