from abc import ABC, abstractmethod

class BaseVerifier(ABC):

    def __init__(self, passed_keys):
        self.passed_keys = passed_keys
        self.query_keys = None
        self.post_keys = None
        self.put_keys = None
        self.query_valid = None
        self.post_valid = None
        self.put_valid = None

        self.assign_variables(passed_keys)
        self.check_keys()


    @abstractmethod
    def assign_variables(self, passed_keys):
        pass


    def check_keys(self):
        print("SDFDS", set(self.passed_keys))
        self.query_valid = len(set(self.passed_keys).difference(self.query_keys)) == 0
        self.post_valid = len(set(self.passed_keys).difference(self.post_keys)) == 0
        if 'column' in self.passed_keys:
            self.put_valid = self.passed_keys['column'] in self.put_keys



class StudentsVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):


        self.passed_keys = passed_keys
        self.query_keys = ['student_id', 'captioning_active']
        self.post_keys = []
        self.put_keys = ['captioning_active']


class PermissionVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.query_keys = ['id']
        self.passed_keys = passed_keys
        self.post_keys = []
        self.put_keys = []


class CoursesVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.query_keys = ["instructor_id", "course_gen_id", "semester"]
        self.passed_keys = passed_keys
        self.post_keys = []
        self.put_keys = ["ilearn_video_service_requested", "ignore_course_ilearn_videos", "course_comments"]


class IlearnVideosVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.query_keys = ["course_gen_id", "semester", "student_id", "instructor_id"]
        self.passed_keys = passed_keys
        self.post_keys = []
        self.put_keys = ["id",
                         "submitted_for_processing",
                         "indicated_due_date",
                         "captioned",
                         "title",
                         "ignore_video",
                         "invalid_link",
                         "auto_caption_passed"]


class CaptioningRequestsVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.query_keys = ['employee_id']
        self.post_keys = ['delivery_format', 'media_id', 'requester_id', 'employee_id']


class EmployeesVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.query_keys = ['semester', 'employee_id']
        self.passed_keys = passed_keys
        self.post_keys = ['employee_id',
                          'employee_first_name',
                          'employee_last_name',
                          'employee_email',
                          'employee_phone',
                          'permission_type']
        self.put_keys = []



class MediaVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.passed_keys = passed_keys
        self.query_keys = ["media_type",
                           "title",
                           "length",
                           "source_url",
                           "captioned_url",
                           "at_catalog_number",
                           "comments",
                           "id",
                           "sha_256_hash"]

        self.post_keys = ["title", "source_url", "media_type", "caption_location", "sha_256_hash"]
        self.put_keys = ["primary_caption_resource_id"]


class CampusOrgsVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.passed_keys = passed_keys
        self.query_keys = ['id', 'organization_name']
        self.post_keys = []
        self.put_keys = []


class CampusOrgsAssignmentVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.passed_keys = passed_keys
        self.query_keys = ['employee_id', 'campus_org_id']
        self.post_keys = ['employee_id', 'campus_org_id']
        self.put_keys = []


class VideoJobsVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.passed_keys = passed_keys
        self.query_keys = ["requester_id", "semester"]

        self.post_keys = ['requester_id',
                          'show_date',
                          'media_id',
                          'comments',
                          'output_format',
                          'semester']

        self.put_keys = ["request_date",
                         "show_date",
                         "delivered_date",
                         "media_id",
                         "output_format",
                         "comments",
                         "delivery_location",
                         "transcripts_only",
                         "job_status",
                         "captioning_provider",
                         "priority",
                         "rush_service_used",
                         "request_method",
                         "ast_job_id",
                         "deleted"]


class RequestersVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.passed_keys = passed_keys
        self.query_keys = ['employee_id', 'student_id', 'semester']
        self.post_keys = []
        self.put_keys = []

class AstJobsVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.passed_keys = passed_keys
        self.query_keys = []
        self.post_keys = ['caption_job_id',
                          'ast_description',
                          'ast_language',
                          'ast_rush',
                          'ast_have_trans',
                          'ast_notes',
                          'ast_basename',
                          'ast_purchase_order',
                          'ast_callback',
                          'ast_status_url',
                          'media_file_id',
                          'id']
        self.put_keys = ['ast_id',
                         "captioning_status"]

class MediaObjectsVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.passed_keys = passed_keys
        self.query_keys = ['media_id']
        self.post_keys = []
        self.put_keys = []

class AmaraVerifier(BaseVerifier):

    def assign_variables(self, passed_keys):
        self.passed_keys = passed_keys
        self.query_keys = ['url', 'video_id']
        self.post_keys = ['url', 'title', 'video_id']



verifier = {

    "permission": PermissionVerifier,
    "courses": CoursesVerifier,
    "ilearn-videos": IlearnVideosVerifier,
    "video-jobs": VideoJobsVerifier,
    "employees": EmployeesVerifier,
    "students": StudentsVerifier,
    "media": MediaVerifier,
    "requesters": RequestersVerifier,
    "campus-orgs": CampusOrgsVerifier,
    "campus-org-assignment": CampusOrgsAssignmentVerifier,
    "captioning-requests": CaptioningRequestsVerifier,
    "ast-jobs": AstJobsVerifier,
    "media-objects": MediaObjectsVerifier,
    "amara": AmaraVerifier
}
