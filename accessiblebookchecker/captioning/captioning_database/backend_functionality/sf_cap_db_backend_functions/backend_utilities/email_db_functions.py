from captioning.captioning_database.sf_cap_database.sf_cap_db_v2 import get_dbase_session,\
    Enrollment, Course, Employee, Student, CaptioningJob, CaptioningRequester, CaptioningMedia,\
    CaptionedResources, AmaraResources

from sqlalchemy.orm import Query
from sqlalchemy import desc
from abc import ABC, abstractmethod
from collections import namedtuple




class EmailSession(ABC):

    def __init__(self, tables):
        self.session = get_dbase_session('E-mail Templates')
        self.query_object = None
        self.tables = tables
        self.semester = None
        self.query_response = []
        self.grouped_query_response = {}
        self.go()

    def go(self):

        self.assign_query()
        self.query()

    @abstractmethod
    def assign_query(self):
        pass

    def query(self):
        query = self.query_object.with_session(self.session).all()
        QueryTuple = namedtuple("Query_Tuple", self.tables)
        for each in query:
            TableQuery = QueryTuple(*each)
            self.query_response.append(TableQuery)


    def grouped_query(self):

        for each in test.query_response:
            if each.Employee.employee_id not in self.grouped_query_response:
                self.grouped_query_response[each.Employee.employee_id] = {"id": each.Employee.employee_id,
                                                      "first_name": each.Employee.employee_first_name,
                                                      "email": each.Employee.employee_email,
                                                      "videos": []}

            self.grouped_query_response[each.Employee.employee_id]['videos'].extend([(each.CaptioningMedia, each.AmaraResources)])

    def commit(self):
        self.session.commit()


class StudentsRequestingCaptioning(EmailSession):

    """
    select * from main_1.enrollment \
                            join main_1.course on main_1.course.course_gen_id = main_1.enrollment.course_id \
                            join main_1.employee on main_1.employee.employee_id = main_1.course.employee_id \
                            where main_1.course.contact_email_sent = false and main_1.enrollment.student_requests_captioning = true;
    """

    def assign_query(self):

        self.query_object = Query([Employee, Course, Enrollment], session=self.session)\
            .join(Course, Enrollment.course_id == Course.course_gen_id) \
            .join(Employee, Course.employee_id == Employee.employee_id) \
            .filter(Course.student_requests_captions_email_sent == False) \
            .filter(Course.semester == 'fa20') \
            .filter(Enrollment.student_requests_captioning == True) \
            .order_by(desc(Enrollment.accomm_added_date))


class ReadyCourseCaptionJobs(EmailSession):

    def assign_query(self):

        self.query_object = Query([CaptioningJob, Course, Employee, CaptioningMedia, AmaraResources], session=self.session) \
            .join(CaptioningRequester, CaptioningJob.requester_id == CaptioningRequester.id) \
            .join(Course, CaptioningRequester.course_id == Course.course_gen_id)\
            .join(Employee, Course.employee_id == Employee.employee_id) \
            .join(CaptioningMedia, CaptioningJob.media_id == CaptioningMedia.id)\
            .join(CaptionedResources, CaptioningMedia.primary_caption_resource_id == CaptionedResources.id) \
            .join(AmaraResources, CaptionedResources.amara_id == AmaraResources.id) \
            .filter(CaptioningJob.job_status == 'Ready') \





test = ReadyCourseCaptionJobs(["CaptioningJob", "Course", "Employee", "CaptioningMedia", "AmaraResources"])
test.grouped_query()






class UncontactedCurrentInstructors(EmailSession):

    def assign_query(self):
        self.query_object = Query([Employee, Course], session=self.session) \
            .join(Course).join(Enrollment)\
            .filter(Course.contact_email_sent == False)

class EachStudentsCourses(EmailSession):

    def assign_query(self):
        self.query_object = Query([Student, Course, Enrollment], session=self.session).join(Course) \
            .join(Enrollment) \
            .filter(Enrollment.student_requests_captioning == True) \

