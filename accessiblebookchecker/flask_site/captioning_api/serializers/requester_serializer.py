from marshmallow import Schema, fields
import toastedmarshmallow
from flask_site.captioning_api.serializers.campus_assignment_serializer import CampusAssignmentSerializer
from flask_site.captioning_api.serializers.courses_serializer import CourseEmployeeSchema
from captioning.captioning_database.backend_functionality.captioning_api_v1_functions import QueryRequesterTable

#
# class RequesterSchema(Schema):
#     class Meta:
#         jit = toastedmarshmallow.Jit
#
#     id = fields.Int(dump_only=True)
#     course = fields.Nested(CourseEmployeeSchema)
#     campus_association_id = fields.Int()
#     campus_association = fields.Nested(CampusAssignmentSerializer)
#
# requester_serializer = RequesterSchema(many=True)


class RequesterSchema(Schema):
    class Meta:
        jit = toastedmarshmallow.Jit

    id = fields.Int(dump_only=True)
    course_id = fields.Str()
    campus_association_id = fields.Int()
    employee_id = fields.Str()
    org_employee_id = fields.Str()
    campus_org_id = fields.Int()
    semester = fields.Str()


# requester_serializerTest = RequesterSchemaTest(many=True)
#
#
#
#
# blork = QueryRequesterTable({'employee_id':'all'})
# blork.run()
#
# print(requester_serializerTest.dump(blork.returned))