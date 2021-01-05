from marshmallow import Schema, fields


class EnrollmentSchema(Schema):

    id = fields.Int(default=1)
    course_id = fields.Str()
    student_id = fields.Str()
    student_enrolled = fields.Boolean()
    student_requests_captioning = fields.Boolean()
    last_updated = fields.DateTime()
    # student = fields.Nested(StudentsSchema) # removed from output to avoid nesting

