import captioning.captioning_database.sf_cap_database.sf_cap_db_v2 as sf_cap_db
from captioning.captioning_database.sf_cap_database.sf_cap_db_v2 import get_dbase_session
from sqlalchemy.orm import Query
from sqlalchemy import or_, asc, desc
import sqlalchemy.exc as data_error
import sqlalchemy.orm.exc as db_error
import flask_site.captioning_api.captioning_api_v1_dispatch.captioning_api_v1_errors.courses_errors as course_api_error
from abc import ABC, abstractmethod
import traceback
import time


#
# try:
#     query_session = get_dbase_session('test_server_querier_querier')
# except:
#     print("NO SESSION ESTABLISHED")
#     print(traceback.print_exc())
#
#     query_session = None



class QuerySessionWrapper():

    def __init__(self):
        self.session = get_dbase_session('test_server_querier_querier')


    def refresh_session(self):
        print("Resetting Closing All Sessions")
        self.session.close_all()
        self.session = get_dbase_session('test_server_querier_querier')


    def active_session(self):
        return self.session


session = QuerySessionWrapper()

#
# class DatabaseConnectionPing():
#
#     def __init__(self):
#         self.session = None
#
#     def ping_database(self):
#
#         self.session = get_dbase_session('DB PING')
#
#         while True:
#             try:
#                 self.session.execute("Select 1")
#             except data_error.OperationalError:
#                 session.session.close_all()
#                 self.session = get_dbase_session('DB PING')
#                 self.session.execute("Select 1")
#                 self.session.close()
#                 time.sleep(300)
#
#
#
# session_ping = DatabaseConnectionPing()
# session_ping.ping_database()

"""
Read Operations
"""

class QueryTableMeta(ABC):

    def __init__(self, payload):

        self.session = session.active_session()
        self.payload = payload
        self.error = None
        self.query = None
        self.query_response = None
        self.returned = None
        self.payload_keys = [*payload] #unpacks dict keys to list


    def run(self):

        self.assign_table()
        self.query_table()
        self.return_query()

    @abstractmethod
    def assign_table(self):
        pass

    def query_table(self):
        try:
            print("Entering query block")
            self.query_response = self.query.with_session(self.session).all()
            print("Exiting query block")
            if len(self.query_response) == 0:
                self.error = course_api_error.NoResultsFound("No Results Found")
        except db_error.NoResultFound:
            self.error = course_api_error.NoResultsFound("No Results Found")
        except data_error.InvalidRequestError:
            self.error = course_api_error.NoResultsFound("Something Went Wrong")
            self.session.rollback()
        except data_error.DataError:
            self.error = course_api_error.IntegrityError("Wrong data type {THIS IS A SECURITY FLAW (SQL INJECTION)}")
            self.session.rollback()
        except data_error.OperationalError:
            session.refresh_session()
            self.query_table()
            self.return_query()

        except:
            print(traceback.print_exc())
            self.session.rollback()




    def return_query(self):


        if self.error is None:

            self.returned = self.query_response
        else:
            self.returned = self.error



class QueryMediaObjectAssignments(QueryTableMeta):
    #QueryMediaObjectAssignments({"media_id": 793})

    def assign_table(self):
        self.query = Query([sf_cap_db.MediaObjectAssignments], session=self.session).filter_by(media_id=self.payload['media_id'])


class QueryS3CaptionStorage(QueryTableMeta):

    def assign_table(self):
        self.query = Query([sf_cap_db.S3CaptionStorage], session=self.session).filter_by(key=self.payload['key'])


class QueryPermission(QueryTableMeta):

    def assign_table(self):
        self.query = Query([sf_cap_db.PermissionType], session=self.session).filter_by(user_id=self.payload['id'])


class QueryCapRequestsTable(QueryTableMeta):
    #{"employee_id": "905387124"}
    def assign_table(self):

        if "employee_id" in self.payload_keys:

            self.query = Query([sf_cap_db.CaptioningRequest], session=self.session)\
                .join(sf_cap_db.CaptioningRequester)\
                .join(sf_cap_db.Course, full=True)\
                .join(sf_cap_db.CampusOrganizationAssignment, full=True)\
                .filter(or_(sf_cap_db.Course.employee_id == self.payload['employee_id'],
                        sf_cap_db.CampusOrganizationAssignment.employee_id == self.payload['employee_id']))


class QueryCoursesTable(QueryTableMeta):

    #{"course_instructor_id":"910484411"}

    def assign_table(self):
        if "course_instructor_id" in self.payload_keys:
            self.query = Query([sf_cap_db.Course], session=self.session).filter_by(employee_id=self.payload["course_instructor_id"])
        if "course_gen_id" in self.payload_keys:
            self.query = Query([sf_cap_db.Course], session=self.session).filter_by(course_gen_id=self.payload["course_gen_id"])
        if "semester" in self.payload_keys:
            self.query = Query([sf_cap_db.Course], session=self.session).filter_by(semester=self.payload["semester"])


class QueryiLearnVideosTable(QueryTableMeta):

    def assign_table(self):

        #{"student_id":"901666420", "semester":"sp19"}
        if 'student_id' in self.payload_keys:
            self.query = Query([sf_cap_db.ScrapediLearnVideos]).join(sf_cap_db.Course).join(sf_cap_db.Enrollment).filter(
                sf_cap_db.Enrollment.student_id == self.payload['student_id'],
                sf_cap_db.Course.semester == self.payload['semester']
            )

        if 'instructor_id' in self.payload_keys:

            #{"instructor_id":"910484411", "semester":"sp19"}
            self.query = Query([sf_cap_db.ScrapediLearnVideos]).join(sf_cap_db.Course).filter(
                sf_cap_db.Course.employee_id == self.payload['instructor_id'],
                sf_cap_db.Course.semester == self.payload['semester']
            )
        if "course_gen_id" in self.payload_keys:
            #{"course_gen_id": "sp19LTNS45501"}
            self.query = Query([sf_cap_db.ScrapediLearnVideos]).filter_by(course_gen_id=self.payload['course_gen_id'])

        if "semester" in self.payload_keys and len(self.payload_keys) == 1:

            self.query = Query([sf_cap_db.ScrapediLearnVideos]).filter(sf_cap_db.ScrapediLearnVideos.semester==self.payload['semester'],
                                                                       sf_cap_db.ScrapediLearnVideos.invalid_link != True)
            print(self.payload_keys, self.payload, "QUERY", self.query)

# test = query_session.query(sf_cap_db.ScrapediLearnVideos).filter(sf_cap_db.ScrapediLearnVideos.semester=='su20').all()
# print(test)


class QueryCapJobsTable(QueryTableMeta):


    def assign_table(self):

        if 'student_id' in self.payload_keys:

            self.query = Query([sf_cap_db.CaptioningJob]) \
                        .join(sf_cap_db.Course).join(sf_cap_db.Enrollment) \
                        .filter(sf_cap_db.Enrollment.student_id == self.payload['student_id'],
                                sf_cap_db.Course.semester == self.payload['semester']
                                )

        if 'instructor_id' in self.payload_keys:
            #{"instructor_id": "907384821", "semester": "fa18"}
            self.query = Query([sf_cap_db.CaptioningJob])\
                .join(sf_cap_db.Course)\
                .filter(
                sf_cap_db.Course.employee_id == self.payload['instructor_id'],
                sf_cap_db.Course.semester == self.payload['semester']
                    )

        if 'course_gen_id' in self.payload_keys:
            #{"course_gen_id": "fa18AAS35001"}
            self.query = Query([sf_cap_db.CaptioningJob]).filter_by(course_id=self.payload['course_gen_id'])

        if 'requester_id' in self.payload_keys:

            if self.payload['requester_id'] == 'all':
                self.query = Query([sf_cap_db.CaptioningJob]).filter(sf_cap_db.CaptioningJob.semester == self.payload['semester'],
                                                                     sf_cap_db.CaptioningJob.deleted == False)
            else:
                self.query = Query([sf_cap_db.CaptioningJob]).filter_by(requester_id=self.payload['requester_id'])


class QueryEmployeesTable(QueryTableMeta):

    def assign_table(self):
        # gets all instructors for semester
        if 'employee_id' in self.payload_keys:
            if self.payload['employee_id'] == 'all':
                self.query = Query([sf_cap_db.Employee])


class QueryStudentsTable(QueryTableMeta):

    def assign_table(self):
        self.query = Query([sf_cap_db.Student]).filter_by(captioning_active=self.payload['captioning_active'])


class QueryMediaTable(QueryTableMeta):

    def assign_table(self):
        print(self.payload_keys)
        if 'id' in self.payload_keys:
            self.query = Query([sf_cap_db.CaptioningMedia]).filter_by(id=self.payload['id'])
        if 'source_url' in self.payload_keys:
            self.query = Query([sf_cap_db.CaptioningMedia]).filter_by(source_url=self.payload['source_url'])
        if 'sha_256_hash' in self.payload_keys:
            self.query = Query([sf_cap_db.CaptioningMedia]).filter_by(sha_256_hash=self.payload['sha_256_hash'])


class QueryRequesterTable(QueryTableMeta):

    def assign_table(self):

        if 'employee_id' in self.payload_keys:

            if 'semester' in self.payload_keys:

                if self.payload['employee_id'] == 'all':
                    self.query = Query([sf_cap_db.CaptioningRequesterOptimizedView])\
                        .filter(or_(sf_cap_db.CaptioningRequesterOptimizedView.semester == self.payload['semester'],
                         sf_cap_db.CaptioningRequesterOptimizedView.semester == None))
                else:
                    self.query = Query([sf_cap_db.CaptioningRequesterOptimizedView])\
                        .filter(sf_cap_db.CaptioningRequesterOptimizedView.employee_id == self.payload['employee_id']) \
                        .filter(or_(sf_cap_db.CaptioningRequesterOptimizedView.semester == self.payload['semester'],
                                    sf_cap_db.CaptioningRequesterOptimizedView.semester == None))
            else:

                if self.payload['employee_id'] == 'all':
                    self.query = Query([sf_cap_db.CaptioningRequesterOptimizedView])
                else:
                    self.query = Query([sf_cap_db.CaptioningRequesterOptimizedView])\
                        .filter_by(employee_id=self.payload['employee_id'])




        if 'student_id' in self.payload_keys:

            self.query = Query([sf_cap_db.CaptioningRequester])\
                .join(sf_cap_db.Course)\
                .join(sf_cap_db.Enrollment)\
                .filter_by(student_id=self.payload['student_id'])


class QueryCampusOrganizationTable(QueryTableMeta):

    def assign_table(self):
        self.query = Query([sf_cap_db.CampusOrganization])


class QueryCampusOrganizationAssignmentTable(QueryTableMeta):

    def assign_table(self):
        if 'employee_id' in self.payload_keys:
            self.query = Query([sf_cap_db.CampusOrganizationAssignment]).filter_by(employee_id=self.payload['employee_id'])


class QueryAmaraTable(QueryTableMeta):

    def assign_table(self):
        if 'url' in self.payload_keys:
            self.query = Query([sf_cap_db.AmaraResources]).filter_by(url=self.payload['url'])
        if 'video_id' in self.payload_keys:
            self.query = Query(sf_cap_db.AmaraResources).filter_by(url=self.payload['video_id'])


"""
Write Operations
"""

class WriteToTableMeta(ABC):

    def __init__(self, payload):

        self.session = get_dbase_session('test_server_post_querier')
        self.error = None
        self.table = None
        self.column = None
        self.query_response = None
        self.payload = payload
        self.returned = None

    def run(self):

        self.assign_table()
        self.query_table()
        self.commit_query()
        self.return_query()


    @abstractmethod
    def assign_table(self):
        pass

    def query_table(self):

        try:
            self.query_response = self.session.query(self.table).filter_by(**{self.column: self.payload[self.column]}).one()
        except db_error.NoResultFound:

            self.error = course_api_error.NoResultsFound("ID doesn't exist")
        except data_error.InvalidRequestError:
            self.error = course_api_error.InvalidDataTypes("Column wrong")
        except data_error.DataError:
            self.error = course_api_error.InvalidDataTypes("Invalid Input Type")
            self.session.rollback()
        except:
            raise


    def commit_query(self):

        if self.error is None:
            try:
                setattr(self.query_response, self.payload['column'], self.payload['value'])
                self.session.commit()
            except:
                self.session.rollback()
                raise
            finally:
                self.session.close()

    def return_query(self):
        if self.error is None:
            self.returned = True, None, self.payload['value']
        else:
            self.returned = self.error


class WriteCourseToTable(WriteToTableMeta):

    # { "course_gen_id": "sp19HTM56001", "column": "contact_email_sent", "value": True }

    def assign_table(self):

        self.table = sf_cap_db.Course
        self.column = "course_gen_id"


class WriteIlearnVideoToTable(WriteToTableMeta):

    def assign_table(self):

        self.table = sf_cap_db.ScrapediLearnVideos
        self.column = "id"


class WriteCapJobsToTable(WriteToTableMeta):

    #{"id": 48, "column": "comments", "value": "Farrtss"}

    def assign_table(self):
        self.table = sf_cap_db.CaptioningJob
        self.column = "id"


class WriteMediaToTable(WriteToTableMeta):
    #{"id": 44, "column": "captioned_url", "value": "Farrtss"}
    def assign_table(self):
        self.table = sf_cap_db.CaptioningMedia
        self.column = "id"

class WriteAstJobsToTable(WriteToTableMeta):

    def assign_table(self):
        self.table = sf_cap_db.AstJob
        self.column = "id"

class WriteAmaraResourcetoTable(WriteToTableMeta):
    def assign_table(self):
        self.table = sf_cap_db.AmaraResources
        self.column = "id"


"""
Add Operataions
"""


class AddToTableMeta(ABC):

    def __init__(self, payload, query_params=None):

        self.session = get_dbase_session('test_server_add_querier')
        self.primary_key = 'id'
        self.error = None
        self.table = None
        self.column = None
        self.headers = None
        self.query_response = None
        self.payload = payload
        self.query_params = query_params
        self.returned = None
        self.record_to_commit = None
        self.query_columns = None
        self.pre_check_dict = {}
        self.already_exists = False
        self.new_commit_id = None


    def run(self):

        self.assign_table()
        if self.query_columns is not None:
            self.construct_query_dict()
            self.check_for_record()

        if self.already_exists is False:
            self.add_record()
            self.commit_query()
            self.return_query()

        if self.already_exists is True:
            self.return_query()

    @abstractmethod
    def assign_table(self):
        pass


    def construct_query_dict(self):

        for each in self.query_columns:
            self.pre_check_dict[each] = self.payload[each]


    def check_for_record(self):

        try:
            self.query_response = self.session.query(self.table).filter_by(**self.pre_check_dict).one()
            self.already_exists = True
        except db_error.NoResultFound:
            print("No Results Found")


    def add_record(self):

        try:
            self.record_to_commit = self.table(**self.payload)
            self.session.add(self.record_to_commit)
            self.session.flush()
            self.new_commit_id = getattr(self.record_to_commit, self.primary_key) # default is set to "id".
        except TypeError:
            raise


    def commit_query(self):
        try:
            self.session.commit()
        except data_error.IntegrityError:
            self.session.rollback()
            self.error = course_api_error.IntegrityError("Media ID Associated with this does not exist")
            raise
        except:
            raise
        finally:
            self.session.close()

    def return_query(self):

        if self.error is None:  # If it errored, just return error.

            if self.already_exists is True:  # if it exists return the query object
                if self.query_response is not None:
                    self.returned = [self.query_response] # wrap in list so serializer schema can iterate

            if self.already_exists is False:  # after created query new record and return it
                self.query_response = self.session.query(self.table).filter(getattr(self.table, self.primary_key)==self.new_commit_id).first()
                self.returned = [self.query_response]
        else:
            self.returned = self.error


class AddRecordToMediaTable(AddToTableMeta):
    #{"media_type": "link", "title": "Flubbb", "source_url": "www.ur.ur.com"}
    def assign_table(self):
        self.table = sf_cap_db.CaptioningMedia
        if "source_url" in self.payload:
            self.query_columns = ["source_url"]
        if "sha_256_hash" in self.payload:
            self.query_columns = ["sha_256_hash"]



class AddMediaObjectToMediaObjectAssignmentsTable(AddToTableMeta):
    #{"media_id": 794, "s3_file_key":9}
    def assign_table(self):
        self.table = sf_cap_db.MediaObjectAssignments

class AddEmployeeeToEmployeeTable(AddToTableMeta):

    def assign_table(self):
        self.table = sf_cap_db.Employee
        self.query_columns = ['employee_id']
        self.primary_key = 'employee_id'

class AddCaptioningRequestToTable(AddToTableMeta):

    def assign_table(self):
        self.table = sf_cap_db.CaptioningRequest
        self.query_columns = ["media_id", "employee_id"]


class AddAstJobToAstJobTable(AddToTableMeta):

    def assign_table(self):
        self.table = sf_cap_db.AstJob



class AddRecordToCapJobsTable(AddToTableMeta):
    def assign_table(self):
        #{"requester_id: 000xxx000, show_date: none, media_id, none, output_format: none, comments: none}
        self.table = sf_cap_db.CaptioningJob
        self.query_columns = ["requester_id", "media_id"]


class AddCampusOrgAssignment(AddToTableMeta):

    def assign_table(self):
        self.table = sf_cap_db.CampusOrganizationAssignment
        self.query_columns = ["campus_org_id", "employee_id"]



class AddCampusOrganization(AddToTableMeta):
    def assign_table(self):
        self.table = sf_cap_db.CampusOrganization


class AddAmaraResourceToTable(AddToTableMeta):
    def assign_table(self):
        self.table = sf_cap_db.AmaraResources
        self.query_columns = ["video_id"]

