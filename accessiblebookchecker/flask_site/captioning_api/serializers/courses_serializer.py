from marshmallow import Schema, fields
import toastedmarshmallow
from flask_site.captioning_api.serializers.enrollement_serializer import EnrollmentSchema
from flask_site.captioning_api.serializers.ilearn_id_serializer import IlearnIdSchema
from flask_site.captioning_api.serializers.employees_serializer import EmployeeSchema


class CourseEmployeeSchema(Schema):

    class Meta:
        jit = toastedmarshmallow.Jit

    id = fields.Int(dump_only=True)
    course_gen_id = fields.Str()
    employee_id = fields.Str()



class CoursesSchema(Schema):


    class Meta:
        jit = toastedmarshmallow.Jit

    id = fields.Int(dump_only=True)
    course_gen_id = fields.Str()
    course_name = fields.Str()
    course_section = fields.Str()
    course_location = fields.Str()
    employee_id = fields.Str()
    course_instructor = fields.Nested(EmployeeSchema())
    students_enrolled = fields.Nested(EnrollmentSchema(), many=True)
    ilearn_page_id = fields.Nested(IlearnIdSchema())
    semester = fields.Str()
    course_online = fields.Boolean()
    no_students_enrolled = fields.Boolean()
    contact_email_sent = fields.Boolean()
    no_student_enrolled_email_sent = fields.Boolean()
    course_comments = fields.Str()
    ilearn_video_service_requested = fields.Boolean()
    import_date = fields.DateTime()
    course_regestration_number = fields.Str()
    instructor_requests_captioning = fields.Boolean()
    ignore_course_ilearn_videos = fields.Boolean()

#


course_query_serializer = CoursesSchema()

courses_query_serializer = CoursesSchema(many=True)