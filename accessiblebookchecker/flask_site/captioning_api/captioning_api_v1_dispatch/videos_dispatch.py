import captioning.captioning_database.backend_functionality.captioning_api_v1_functions as cap_functions
from captioning.captioning_database.backend_functionality.captioning_api_v1_functions import QueryCapJobsTable
from flask_site.captioning_api.captioning_api_v1_dispatch.captioning_api_v1_errors import courses_errors as api_error
from flask_site.captioning_api.serializers.iLearn_videos_serializer import ilearn_video_serializer
from flask_site.captioning_api.serializers.caption_job_videos_serializer import caption_job_serializer

class VideoObject:

    def __init__(self, query_params):

        self.query_type = None
        self.query_params = query_params
        self.IlearnVideos = None
        self.CapJobVideos = None
        self.identify_query_type()

    ##! Needs deeper error handing
    def identify_query_type(self):


        if 'instructor_id' in self.query_params:
            self.IlearnVideos = cap_functions.QueryiLearnVideosTable(self.query_params)
            self.CapJobVideos = cap_functions.QueryCapJobsTable(self.query_params)
            self.query_type = 'instructor_id'


        if 'student_id' in self.query_params:
            self.IlearnVideos = cap_functions.QueryiLearnVideosTable(self.query_params)
            self.CapJobVideos = cap_functions.QueryCapJobsTable(self.query_params)
            self.query_type = 'student_id'


        if 'course_gen_id' in self.query_params:
            self.IlearnVideos = cap_functions.QueryiLearnVideosTable(self.query_params)
            self.CapJobVideos = cap_functions.QueryCapJobsTable(self.query_params)
            self.query_type = 'course_gen_id'

        if 'course_gen_id' and 'student_id' and 'instructor_id' not in self.query_params:
            pass



    def return_query(self):
        print(self.query_params, self.query_type)
        objectType = {"search_type": self.query_type,
                      "search_id": self.query_params[self.query_type],
                      "ilearn_videos": ilearn_video_serializer.dump(self.IlearnVideos),
                      "captioning_jobs": caption_job_serializer.dump(self.CapJobVideos)}

        return objectType


class VideoJobProto:

    """
    Minimally acceptable put object

    {"table": "jobs", "record":
    { "course_id":"fa18AAS35001", "request_date":"2004-10-19 10:23:54",
     "show_date": "2004-10-19 10:23:54", "delivered_date": "2004-10-19 10:23:54",
      "media_id": null, "output_format": null, "comments": null, "delivery_location": null,
       "transcripts_only": null, "job_status": null, "captioning_provider": null, "priority": null,
        "rush_service_used": null, "request_method": null, "ast_job_id": null}}

    """



    def __init__(self, data):
        self.data = data
        self.course = None
        self.request_date = None
        self.show_date = None
        self.delivered_date = None
        self.media_id = None
        self.output_format = None
        self.comments = None
        self.delivery_location = None
        self.transcripts_only = None
        self.job_status = None
        self.captioning_provider = None
        self.priority = None
        self.rush_service_used = None
        self.request_method = None
        self.ast_job_id = None

        self.failed = False
        self.init_data()


    def init_data(self):

        ##! need leway for empty dates

        self.course = self.data['course_id']
        self.request_date = self.data['request_date']
        self.show_date = self.data['show_date']
        self.delivered_date = self.data['delivered_date']
        self.media_id = self.data['media_id']
        self.output_format = self.data['output_format']
        self.comments = self.data['comments']
        self.delivery_location = self.data['delivery_location']
        self.transcripts_only = self.data['transcripts_only']
        self.job_status = self.data['job_status']
        self.captioning_provider = self.data['captioning_provider']
        self.priority = self.data['priority']
        self.rush_service_used = self.data['rush_service_used']
        self.request_method = self.data['request_method']
        self.ast_job_id = self.data['ast_job_id']



    def return_job(self):

        if self.failed == False:

            return {'course_id': self.course,
                       'request_date': self.request_date,
                       'show_date': self.show_date,
                       'delivered_date': self.delivered_date,
                       'media_id': self.media_id,
                       'output_format': self.output_format,
                       'comments': self.comments,
                       'delivery_location': self.delivery_location,
                       'transcripts_only': self.transcripts_only,
                       'job_status': self.job_status,
                       'captioning_provider': self.captioning_provider,
                       'priority': self.priority,
                       'rush_service_used': self.rush_service_used,
                       'request_method': self.request_method,
                       'ast_job_id': self.ast_job_id}
        else:
            return api_error.InvalidDataTypes("Wrong")


def dispatch_videos_query_get(query_params):



    query_params = query_params.to_dict()

    allowed_queries = ["instructor_id", "course_gen_id", "semester", "student_id"]

    query_check = [False for x in query_params if x not in allowed_queries]


    if False not in query_check:

        query = QueryCapJobsTable(query_params)
        query.run()
        return query.returned


    else:
        return api_error.InvalidParams("Allowed queries are: instructor_id, course_gen_id, semester, student_id")








    #
    # query_params = query_params.to_dict()
    #
    # allowed_queries = ["instructor_id", "course_gen_id", "semester", "student_id"]
    #
    # query_check = [False for x in query_params if x not in allowed_queries]
    #
    #
    # if False not in query_check:
    #
    #     VideoQuery = VideoObject(query_params)
    #
    #     return VideoQuery.return_query()
    #
    # else:
    #     return api_error.InvalidParams("Allowed queries are: Instructor_ID,  Course_Gen_ID", "Semester", "Student_Id")


def dispatch_videos_post(data):



    writable_columns = ["request_date",
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
                        "ast_job_id"]


    if data['column'] in writable_columns:

        write = cap_functions.WriteCapJobsToTable(data)
        write.run()
        return write.returned

    else:
        return api_error.InvalidParams("Can't Write to that column")




def dispatch_videos_put(data):



    required_columns = ['course_id',
                        'request_date',
                        'delivered_date',
                        'media_id',
                        'output_format',
                        'comments',
                        'delivery_location',
                        'transcripts_only',
                        'job_status',
                        'captioning_provider',
                        'priority',
                        'rush_service_used',
                        'request_method',
                        'ast_job_id']

    if list(data.keys()).sort() == required_columns.sort():


        add = cap_functions.AddRecordToCapJobsTable(data)
        add.run()
        return add.returned


    return api_error.InvalidDataTypes("Incomplete Put Object")
